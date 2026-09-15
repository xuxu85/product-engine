from pathlib import Path
import subprocess
import sys


def test_venture_core_pain_shov_contract():
    """Verify the pinned Venture Core PAIN seam can be loaded and returns AgentRequest."""
    core = Path('/tmp/product-venture-core')
    subprocess.run(
        ['git', 'clone', '--depth', '1', 'https://github.com/xuxu85/product-venture-core.git', str(core)],
        check=True,
        capture_output=True,
        text=True,
    )
    sys.path.insert(0, str(core))
    from agents.pain.interface import build_request
    from core.state import Stage

    evidence = [{
        'source': 'amazon',
        'marketplace': 'US',
        'product': 'electrolyte water',
        'text': 'fixture evidence',
    }]
    request = build_request(evidence, task_id='shov-contract-test')

    assert request.stage == Stage.PAIN
    assert request.agent_id == 'pain'
    assert request.agent_version == '0.1.0'
    assert request.evidence == evidence
    assert request.input == {'evidence': evidence}
