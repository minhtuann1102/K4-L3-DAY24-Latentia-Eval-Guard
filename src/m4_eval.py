from __future__ import annotations

"""Module 4: RAGAS Evaluation — 4 metrics + failure analysis."""

import os, sys, json, re
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TEST_SET_PATH, OPENAI_API_KEY, JUDGE_MODEL, EMBEDDING_MODEL


@dataclass
class EvalResult:
    question: str
    answer: str
    contexts: list[str]
    ground_truth: str
    faithfulness: float
    answer_relevancy: float
    context_precision: float
    context_recall: float


def load_test_set(path: str = TEST_SET_PATH) -> list[dict]:
    """Load test set from JSON. (Đã implement sẵn)"""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _safe_float(val) -> float:
    import math
    if isinstance(val, bool):
        raise ValueError("RAGAS score cannot be boolean")
    try:
        value = float(val)
    except (TypeError, ValueError) as error:
        raise ValueError("RAGAS score must be numeric") from error
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError("RAGAS score must be finite and in [0,1]")
    return value


def evaluate_ragas(questions: list[str], answers: list[str],
                   contexts: list[list[str]], ground_truths: list[str]) -> dict:
    """Run real RAGAS only; propagate failures rather than inventing scores."""
    if not questions or len({len(questions), len(answers), len(contexts), len(ground_truths)}) != 1:
        raise ValueError("RAGAS inputs must have the same nonzero length")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required for live RAGAS")
    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
    from datasets import Dataset
    from langchain_openai import ChatOpenAI
    from langchain_community.embeddings import HuggingFaceEmbeddings

    dataset = Dataset.from_dict(dict(question=questions, answer=answers,
                                    contexts=contexts, ground_truth=ground_truths))
    llm = ChatOpenAI(model=JUDGE_MODEL, temperature=0, api_key=OPENAI_API_KEY)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    result = evaluate(dataset, metrics=[faithfulness, answer_relevancy,
                      context_precision, context_recall], llm=llm,
                      embeddings=embeddings, raise_exceptions=True)
    names = ("faithfulness", "answer_relevancy", "context_precision", "context_recall")
    rows = []
    for row in result.to_pandas().to_dict(orient="records"):
        rows.append(EvalResult(question=str(row["question"]), answer=str(row["answer"]),
                               contexts=list(row["contexts"]), ground_truth=str(row["ground_truth"]),
                               **{name: _safe_float(row[name]) for name in names}))
    if len(rows) != len(questions):
        raise ValueError("RAGAS returned the wrong number of rows")
    return {**{name: _safe_float(result[name]) for name in names},
            "per_question": rows,
            "metadata": {"evaluator_models": [JUDGE_MODEL, EMBEDDING_MODEL]}}


def failure_analysis(eval_results: list[EvalResult], bottom_n: int = 10) -> list[dict]:
    """Analyze bottom-N worst questions using Diagnostic Tree."""
    if not eval_results:
        return []

    diagnostic_tree = {
        "faithfulness": ("LLM hallucinating", "Tighten prompt, lower temperature"),
        "context_recall": ("Missing relevant chunks", "Improve chunking or add BM25"),
        "context_precision": ("Too many irrelevant chunks", "Add reranking or metadata filter"),
        "answer_relevancy": ("Answer doesn't match question", "Improve prompt template"),
    }

    scored_items = []
    for res in eval_results:
        metrics = {
            "faithfulness": res.faithfulness,
            "answer_relevancy": res.answer_relevancy,
            "context_precision": res.context_precision,
            "context_recall": res.context_recall,
        }
        avg_score = sum(metrics.values()) / max(len(metrics), 1)
        worst_metric = min(metrics, key=metrics.get)
        worst_score = metrics[worst_metric]
        diagnosis, suggested_fix = diagnostic_tree.get(
            worst_metric, ("Unknown failure", "Review query and context")
        )

        scored_items.append({
            "question": res.question,
            "worst_metric": worst_metric,
            "score": worst_score,
            "avg_score": round(avg_score, 4),
            "diagnosis": diagnosis,
            "suggested_fix": suggested_fix,
        })

    scored_items.sort(key=lambda x: x["avg_score"])
    return scored_items[:bottom_n]


def save_report(results: dict, failures: list[dict], path: str = "reports/ragas_report.json"):
    """Save evaluation report to JSON. (Đã implement sẵn)"""
    parent_dir = os.path.dirname(path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    report = {
        "aggregate": {k: v for k, v in results.items() if k != "per_question"},
        "num_questions": len(results.get("per_question", [])),
        "failures": failures,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Report saved to {path}")


if __name__ == "__main__":
    test_set = load_test_set()
    print(f"Loaded {len(test_set)} test questions")
    print("Run pipeline.py first to generate answers, then call evaluate_ragas().")
