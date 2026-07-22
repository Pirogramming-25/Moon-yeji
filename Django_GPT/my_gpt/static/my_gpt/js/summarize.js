(function () {
    const input = document.getElementById("summarize-input");
    const btn = document.getElementById("summarize-btn");
    const loading = document.getElementById("summarize-loading");
    const errorBox = document.getElementById("summarize-error");
    const resultBox = document.getElementById("summarize-result");

    function showError(message) {
        errorBox.textContent = message;
        errorBox.style.display = "block";
    }

    function hideError() {
        errorBox.style.display = "none";
        errorBox.textContent = "";
    }

    function setLoading(isLoading) {
        loading.style.display = isLoading ? "block" : "none";
        btn.disabled = isLoading;
        input.disabled = isLoading;
    }

    btn.addEventListener("click", async function () {
        const text = input.value.trim();
        hideError();
        resultBox.style.display = "none";

        if (text.length < 100) {
            showError("요약할 문서는 100자 이상 입력해주세요.");
            return;
        }

        if (text.length > 5000) {
            showError("문서는 5,000자 이하로 입력해주세요.");
            return;
        }

        setLoading(true);

        try {
            const response = await fetch("/summarize/run/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({ text: text }),
            });

            const data = await response.json();

            if (!response.ok) {
                showError(data.error || "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.");
                return;
            }

            resultBox.textContent =
                `원문 길이: ${data.original_length}자\n` +
                `요약문 길이: ${data.summary_length}자\n` +
                `요약 비율: ${data.summary_ratio}%\n\n` +
                `요약 결과:\n${data.summary}`;
            resultBox.style.display = "block";
        } catch (err) {
            showError("모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.");
        } finally {
            setLoading(false);
        }
    });
})();