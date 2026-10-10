"""Tests for the evaluation set schema validity."""

import json
from pathlib import Path

from google.adk.evaluation.eval_set import EvalSet


def test_assistant_evalset_validity() -> None:
    evalset_path = Path("agents/assistant/evals/assistant.evalset.json")
    assert evalset_path.is_file()

    with evalset_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    eval_set = EvalSet.model_validate(data)
    assert eval_set.eval_set_id == "assistant_basic_eval"
    assert len(eval_set.eval_cases) >= 2
