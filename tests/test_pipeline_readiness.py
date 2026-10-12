"""Prevent missing adapters and synthetic evaluation results in live runs."""
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from src import m4_eval
import config


@pytest.mark.parametrize("score", [True, False, None, float("nan"), float("inf"), -.01, 1.01])
def test_invalid_ragas_scores_are_rejected(score):
    with pytest.raises(ValueError):
        m4_eval._safe_float(score)


def test_live_evaluation_requires_key(monkeypatch):
    monkeypatch.setattr(m4_eval, "OPENAI_API_KEY", "")
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        m4_eval.evaluate_ragas(["q"], ["a"], [["c"]], ["r"])


def test_provider_error_is_not_replaced_by_offline_scores(monkeypatch):
    monkeypatch.setattr(m4_eval, "OPENAI_API_KEY", "test-not-key")
    evaluate = Mock(side_effect=RuntimeError("provider unavailable"))
    monkeypatch.setitem(sys.modules, "ragas", SimpleNamespace(evaluate=evaluate))
    monkeypatch.setitem(sys.modules, "ragas.metrics", SimpleNamespace(
        faithfulness=object(), answer_relevancy=object(),
        context_precision=object(), context_recall=object()))
    monkeypatch.setitem(sys.modules, "datasets", SimpleNamespace(
        Dataset=SimpleNamespace(from_dict=lambda payload: payload)))
    llm, embeddings = Mock(), Mock()
    monkeypatch.setitem(sys.modules, "langchain_openai", SimpleNamespace(ChatOpenAI=llm))
    monkeypatch.setitem(sys.modules, "langchain_community.embeddings", SimpleNamespace(HuggingFaceEmbeddings=embeddings))
    with pytest.raises(RuntimeError, match="provider unavailable"):
        m4_eval.evaluate_ragas(["q"], ["a"], [["c"]], ["r"])
    assert evaluate.call_args.kwargs["raise_exceptions"] is True
    assert llm.call_args.kwargs["model"] == m4_eval.JUDGE_MODEL
    assert embeddings.call_args.kwargs["model_name"] == m4_eval.EMBEDDING_MODEL


def test_enrichment_adapter_uses_generation_model(monkeypatch, openai_client):
    monkeypatch.setattr(config, "OPENAI_API_KEY", "test-not-key")
    client, model = config.get_llm_client()
    assert client is openai_client and model == config.GENERATION_MODEL


def test_enrichment_adapter_without_key(monkeypatch):
    monkeypatch.setattr(config, "OPENAI_API_KEY", "")
    assert config.get_llm_client() == (None, config.GENERATION_MODEL)
