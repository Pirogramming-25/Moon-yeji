(function () {
    const input = document.getElementById("sentiment-input");
    const btn = document.getElementById("sentiment-btn");
    const loading = document.getElementById("sentiment-loading");
    const errorBox = document.getElementById("sentiment-error");
    const resultBox = document.getElementById("sentiment-result");
    const historyBox = document.getElementById("sentiment-history");

    let history = [];

    function renderHistory() {
        historyBox.innerHTML = "";
        history.slice(0, 5).forEach((item, idx) => {
            const div = document.createElement("div");
            div.className = "history-item";
            div.textContent = `${idx + 1}. "${item.text}" → ${item.label} (${item.score}%)`;
            historyBox.appendChild(div);
        });
    }

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
            const response = await fetch("/sentiment/run/", {
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

            const scorePercent = (data.score * 100).toFixed(2);

            let resultText = `감정: ${data.label}\n신뢰도: ${scorePercent}%\n\n`;
            data.all_scores.forEach((s) => {
                resultText += `${s.label}: ${(s.score * 100).toFixed(2)}%\n`;
            });

            resultBox.textContent = resultText;
            resultBox.style.display = "block";

            history.unshift({ text: text, label: data.label, score: scorePercent });
            history = history.slice(0, 5);
            renderHistory();
        } catch (err) {
            showError("모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.");
        } finally {
            setLoading(false);
        }
    });
})();