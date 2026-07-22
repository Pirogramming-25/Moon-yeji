from .services.moderator import analyze_toxicity
import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .decorators import model_login_required
from .models import InferenceHistory
from .services.sentiment import analyze_sentiment
from .services.summarizer import summarize_text

logger = logging.getLogger(__name__)


# ---------------------------
# 감정 분석 (비로그인 허용)
# ---------------------------

def sentiment_page(request):
    return render(request, "my_gpt/sentiment.html")


@require_http_methods(["POST"])
def sentiment_run(request):
    try:
        data = json.loads(request.body)
        text = data.get("text", "")
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

    if not text or not text.strip():
        return JsonResponse({"error": "분석할 문장을 입력해주세요."}, status=400)

    text = text.strip()

    if len(text) > 1000:
        return JsonResponse({"error": "문장은 1,000자 이하로 입력해주세요."}, status=400)

    try:
        result = analyze_sentiment(text)
    except Exception:
        logger.exception("Sentiment model inference failed.")
        return JsonResponse({"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."}, status=502)

    return JsonResponse({
        "label": result["label"],
        "score": result["score"],
        "all_scores": result["all_scores"],
    })


# ---------------------------
# 문서 요약 (로그인 필요)
# ---------------------------

@model_login_required
def summarize_page(request):
    histories = (
        InferenceHistory.objects
        .filter(user=request.user, task=InferenceHistory.Task.SUMMARIZE)
        .order_by("-created_at")[:5]
    )
    return render(request, "my_gpt/summarize.html", {"histories": histories})


@model_login_required
@require_http_methods(["POST"])
def summarize_run(request):
    try:
        data = json.loads(request.body)
        text = data.get("text", "")
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

    text = text.strip() if text else ""

    if len(text) < 100:
        return JsonResponse({"error": "요약할 문서는 100자 이상 입력해주세요."}, status=400)

    if len(text) > 5000:
        return JsonResponse({"error": "문서는 5,000자 이하로 입력해주세요."}, status=400)

    try:
        result = summarize_text(text)
    except Exception:
        logger.exception("Summarizer model inference failed.")
        return JsonResponse({"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."}, status=502)

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.SUMMARIZE,
        input_text=text,
        output_text=result["summary"],
        result_data=result,
    )

    return JsonResponse(result)
# ---------------------------
# 유해 표현 분석 (로그인 필요)
# ---------------------------

@model_login_required
def moderate_page(request):
    histories = (
        InferenceHistory.objects
        .filter(user=request.user, task=InferenceHistory.Task.MODERATE)
        .order_by("-created_at")[:5]
    )
    return render(request, "my_gpt/moderate.html", {"histories": histories})


@model_login_required
@require_http_methods(["POST"])
def moderate_run(request):
    try:
        data = json.loads(request.body)
        text = data.get("text", "")
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

    if not text or not text.strip():
        return JsonResponse({"error": "분석할 문장을 입력해주세요."}, status=400)

    text = text.strip()

    if len(text) > 1000:
        return JsonResponse({"error": "문장은 1,000자 이하로 입력해주세요."}, status=400)

    try:
        result = analyze_toxicity(text)
    except Exception:
        logger.exception("Moderator model inference failed.")
        return JsonResponse({"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."}, status=502)

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.MODERATE,
        input_text=text,
        output_text=result["highest_label"],
        result_data=result,
    )

    return JsonResponse(result)    