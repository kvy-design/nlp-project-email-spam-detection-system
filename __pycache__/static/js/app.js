// Load sample email into textarea
function loadSample(type) {
    const textarea = document.getElementById("emailInput");
    if (SAMPLE_TEXTS && SAMPLE_TEXTS[type]) {
        textarea.value = SAMPLE_TEXTS[type];
        submitAnalysis();
    }
}

// Clear textarea
function clearInput() {
    document.getElementById("emailInput").value = "";
    document.getElementById("resultsCard").style.display = "none";
    document.getElementById("emptyStateCard").style.display = "flex";
}

// Submit message for NLP analysis
async function submitAnalysis() {
    const text = document.getElementById("emailInput").value.trim();
    if (!text) {
        alert("Please enter or paste an email message to analyze.");
        return;
    }

    const btn = document.getElementById("analyzeBtn");
    const btnText = document.getElementById("btnText");
    const btnIcon = document.getElementById("btnIcon");

    btn.disabled = true;
    btnText.innerText = "Analyzing...";
    btnIcon.innerText = "⏳";

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        if (response.ok) {
            renderResults(data);
        } else {
            alert(data.error || "An error occurred during analysis.");
        }
    } catch (err) {
        console.error("Analysis error:", err);
        alert("Failed to connect to backend service.");
    } finally {
        btn.disabled = false;
        btnText.innerText = "Scan & Classify Message";
        btnIcon.innerText = "🔍";
    }
}

// Render analysis results to UI
function renderResults(data) {
    const emptyState = document.getElementById("emptyStateCard");
    const resultsCard = document.getElementById("resultsCard");

    emptyState.style.display = "none";
    resultsCard.style.display = "block";

    // Category title & badge
    const categoryEl = document.getElementById("resultCategory");
    categoryEl.innerText = data.prediction;

    const badgeEl = document.getElementById("threatBadge");
    badgeEl.innerText = data.threat_level;
    badgeEl.className = "threat-badge " + (
        data.status_color === "danger" ? "threat-danger" :
        data.status_color === "warning" ? "threat-warning" : "threat-success"
    );

    // Risk Meter Fill & Score
    const scoreVal = data.risk_score;
    document.getElementById("riskScoreText").innerText = `${scoreVal} / 100`;

    const progressFill = document.getElementById("progressBarFill");
    progressFill.style.width = `${scoreVal}%`;
    progressFill.className = "progress-bar-fill " + (
        scoreVal >= 70 ? "fill-danger" :
        scoreVal >= 35 ? "fill-warning" : "fill-success"
    );

    // Probability Bars
    const probs = data.probabilities || {};
    const legitPct = probs["legitimate"] !== undefined ? probs["legitimate"] : 0;
    const spamPct = probs["spam"] !== undefined ? probs["spam"] : 0;
    const phishPct = probs["phishing"] !== undefined ? probs["phishing"] : 0;

    document.getElementById("probLegit").style.width = `${legitPct}%`;
    document.getElementById("probLegitVal").innerText = `${legitPct}%`;

    document.getElementById("probSpam").style.width = `${spamPct}%`;
    document.getElementById("probSpamVal").innerText = `${spamPct}%`;

    document.getElementById("probPhishing").style.width = `${phishPct}%`;
    document.getElementById("probPhishingVal").innerText = `${phishPct}%`;

    // Detected Signals
    const flagsList = document.getElementById("flagsList");
    flagsList.innerHTML = "";

    if (data.flags && data.flags.length > 0) {
        data.flags.forEach(flag => {
            const li = document.createElement("li");
            li.innerText = flag;
            flagsList.appendChild(li);
        });
    } else {
        const li = document.createElement("li");
        li.className = "safe-signal";
        li.innerText = "No prominent phishing or spam indicators detected. Linguistic patterns align with legitimate communication.";
        flagsList.appendChild(li);
    }

    // Engine info
    document.getElementById("bestModelName").innerText = data.best_model_used || "Trained Pipeline";
}

// Modal handling
const metricsModal = document.getElementById("metricsModal");
const viewMetricsBtn = document.getElementById("viewMetricsBtn");

viewMetricsBtn.addEventListener("click", async () => {
    metricsModal.style.display = "flex";
    await loadMetrics();
});

function closeMetricsModal() {
    metricsModal.style.display = "none";
}

// Close modal when clicking outside of card
window.addEventListener("click", (e) => {
    if (e.target === metricsModal) {
        closeMetricsModal();
    }
});

// Fetch and render benchmark metrics
async function loadMetrics() {
    const tbody = document.getElementById("metricsTableBody");
    try {
        const res = await fetch("/api/metrics");
        const data = await res.json();
        
        if (!res.ok) {
            tbody.innerHTML = `<tr><td colspan="5">${data.error || 'Failed to load metrics.'}</td></tr>`;
            return;
        }

        const models = data.models;
        tbody.innerHTML = "";

        for (const [name, info] of Object.entries(models)) {
            const isBest = name === data.best_model;
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>${name}</strong> ${isBest ? '<span class="badge badge-nlp" style="font-size: 0.65rem;">Best</span>' : ''}</td>
                <td>${(info.test_accuracy * 100).toFixed(1)}%</td>
                <td>${(info.macro_f1 * 100).toFixed(1)}%</td>
                <td>${(info.weighted_f1 * 100).toFixed(1)}%</td>
                <td>${(info.cv_macro_f1_mean * 100).toFixed(1)}% (±${(info.cv_macro_f1_std * 100).toFixed(1)}%)</td>
            `;
            tbody.appendChild(tr);
        }

        // Render Confusion Matrix for Best Model
        const bestModelInfo = models[data.best_model];
        if (bestModelInfo && bestModelInfo.confusion_matrix) {
            renderConfusionMatrix(bestModelInfo.confusion_matrix, bestModelInfo.classes);
        }
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="5">Error loading benchmark data.</td></tr>`;
    }
}

function renderConfusionMatrix(matrix, classes) {
    const container = document.getElementById("cmContainer");
    const numClasses = classes.length;
    container.style.gridTemplateColumns = `repeat(${numClasses + 1}, 1fr)`;
    container.innerHTML = "";

    // Top-left blank header
    const blank = document.createElement("div");
    blank.className = "cm-cell cm-header";
    blank.innerText = "Actual \\ Pred";
    container.appendChild(blank);

    // Column headers (Predicted)
    classes.forEach(c => {
        const th = document.createElement("div");
        th.className = "cm-cell cm-header";
        th.innerText = c.toUpperCase();
        container.appendChild(th);
    });

    // Rows
    for (let i = 0; i < numClasses; i++) {
        // Row label (Actual)
        const rowHeader = document.createElement("div");
        rowHeader.className = "cm-cell cm-header";
        rowHeader.innerText = classes[i].toUpperCase();
        container.appendChild(rowHeader);

        for (let j = 0; j < numClasses; j++) {
            const cell = document.createElement("div");
            cell.className = "cm-cell";
            const val = matrix[i][j];
            cell.innerText = val;
            if (i === j && val > 0) {
                cell.style.background = "rgba(16, 185, 129, 0.25)";
                cell.style.color = "#34d399";
                cell.style.fontWeight = "700";
            } else if (val > 0) {
                cell.style.background = "rgba(239, 68, 68, 0.25)";
                cell.style.color = "#f87171";
            }
            container.appendChild(cell);
        }
    }
}
