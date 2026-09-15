# Business State Projection

The pipeline state is the canonical engineering truth. Business State is a read-only projection for the Notion control plane.

Flow:

`AgentResult → Gate transition → PipelineState → BusinessState → Notion`

Rules:

- Gate decisions remain the authority for commercial progress.
- Progress is derived from the current gate, not task count.
- Projection does not create evidence or make PASS/FAIL/PIVOT decisions.
- Notion displays business state; it does not become the execution engine.
- Paid data is not required for this layer.

Current mapping is defined in `pipeline/business_state.py` and can be changed only as an explicit pipeline-policy decision.
