from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device


MODEL_ID = "sshleifer/distilbart-cnn-6-6"


@lru_cache(maxsize=1)
def get_summarizer_pipeline():
    return pipeline(
        task="summarization",
        model=MODEL_ID,
        device=get_pipeline_device(),
    )


def summarize_text(text: str, do_sample: bool = False) -> dict:
    summarizer = get_summarizer_pipeline()

    kwargs = {
        "max_length": 180,
        "min_length": 40,
    }

    if do_sample:
        kwargs.update({
            "do_sample": True,
            "top_p": 0.9,
            "temperature": 0.8,
        })

    result = summarizer(text, **kwargs)
    summary = result[0]["summary_text"]

    summary_ratio = (len(summary) / len(text)) * 100

    return {
        "summary": summary,
        "original_length": len(text),
        "summary_length": len(summary),
        "summary_ratio": round(summary_ratio, 2),
    }