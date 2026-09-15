from pipeline.business_state import project_business_state
from pipeline.state import Decision, PipelineState, Stage


def test_projection_uses_gate_not_task_count():
    state = PipelineState(stage=Stage.PAIN, decision=Decision.PASS)
    projected = project_business_state(
        state,
        bottleneck="verified consumer pain/opportunity evidence",
        capital_required=0.0,
        next_action="Run PAIN evidence workflow",
    )
    assert projected.progress_percent == 15
    assert projected.current_gate == "PAIN"
    assert projected.last_decision == "PASS"
    assert projected.bottleneck == "verified consumer pain/opportunity evidence"
    assert projected.next_action == "Run PAIN evidence workflow"


def test_projection_reaches_full_progress_only_at_scale():
    projected = project_business_state(PipelineState(stage=Stage.SCALE, decision=Decision.PASS))
    assert projected.progress_percent == 100


def test_projection_marks_stop_without_inventing_progress():
    projected = project_business_state(PipelineState(stage=Stage.STOP, decision=Decision.FAIL))
    assert projected.progress_percent == 0
    assert projected.status == "STOPPED"
