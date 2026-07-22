(function () {
    const input = document.getElementById("moderate-input");
    const btn = document.getElementById("moderate-btn");
    const loading = document.getElementById("moderate-loading");
    const errorBox = document.getElementById("moderate-error");
    const resultBox = document.getElementById("moderate-result");

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

        if (!text) {
            showError("분석할 문장을 입력해주세요.");
            return;
        }

        if (text.length > 1000) {
            showError("문장은 1,000자 이하로 입력해주세요.");
            return;
        }

        setLoading(true);

        try {
            const response = await fetch("/moderate/run/", {
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

            let resultText = `최고 위험 레이블: ${data.highest_label}\n위험 점수: ${(data.highest_score * 100).toFixed(2)}%\n\n`;
            data.all_scores.forEach((s) => {
                resultText += `${s.label}: ${(s.score * 100).toFixed(2)}%\n`;
            });

            resultBox.textContent = resultText;
            resultBox.style.display = "block";
        } catch (err) {
            showError("모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.");
        } finally {
            setLoading(false);
        }
    });
})();