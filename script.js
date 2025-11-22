// static/script.js
document.getElementById('analyzeBtn').addEventListener('click', analyze);

function analyze() {
    const link = document.getElementById("videoLink").value.trim();
    const resultDiv = document.getElementById("result");
    const commentsEl = document.getElementById("comments");
    commentsEl.innerHTML = "";

    if (!link) {
        resultDiv.textContent = "⚠ Please paste a YouTube link";
        resultDiv.style.color = "red";
        return;
    }

    resultDiv.textContent = "Analyzing… please wait ⏳";
    resultDiv.style.color = "orange";

    fetch("/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url: link})
    })
    .then(async (resp) => {
        if (!resp.ok) {
            const err = await resp.json().catch(()=> ({}));
            throw new Error(err.error || 'Server error');
        }
        return resp.json();
    })
    .then(data => {
        if (data.error) throw new Error(data.error);
        resultDiv.textContent = "Sentiment: " + data.sentiment + " (score: " + (data.score||0).toFixed(3) + ")";
        resultDiv.style.color = data.sentiment === "Positive" ? "green" : (data.sentiment === "Negative" ? "red" : "blue");

        if (data.sample_comments && data.sample_comments.length) {
            data.sample_comments.forEach(c => {
                const li = document.createElement('li');
                li.textContent = c;
                commentsEl.appendChild(li);
            });
        }
    })
    .catch(err => {
        resultDiv.textContent = "❌ " + err.message;
        resultDiv.style.color = "red";
    });
}
