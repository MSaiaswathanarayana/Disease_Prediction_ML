(function () {
  "use strict";
  const symptoms = JSON.parse(document.getElementById("symptom-data").textContent);
  const minSymptoms = window.ASSESS_CONFIG.minSymptoms;
  const selected = new Set();
  const esc = DP.escapeHtml;
  const GAUGE_LENGTH = 2 * Math.PI * 54;

  const el = {
    form: document.getElementById("assess-form"),
    search: document.getElementById("sym-search"),
    grid: document.getElementById("sym-grid"),
    none: document.getElementById("sym-none"),
    selBlock: document.getElementById("sym-selected-block"),
    selList: document.getElementById("sym-selected-list"),
    clear: document.getElementById("sym-clear"),
    hint: document.getElementById("sym-hint"),
    btn: document.getElementById("assess-btn"),
    error: document.getElementById("form-error"),
    results: document.getElementById("results"),
    summary: document.getElementById("summary"),
    symResults: document.getElementById("sym-results"),
    heartCard: document.getElementById("heart-card"),
    diabetesCard: document.getElementById("diabetes-card"),
    flagRows: document.getElementById("flag-rows"),
    emergency: document.getElementById("emergency-note"),
    newCheck: document.getElementById("new-check"),
  };

  function labelFor(key) {
    const item = symptoms.find(function (s) { return s.key === key; });
    return item ? item.label : key;
  }

  function renderChips() {
    const query = el.search.value.trim().toLowerCase();
    const matches = symptoms.filter(function (s) { return s.label.toLowerCase().indexOf(query) !== -1; });
    el.grid.innerHTML = "";
    matches.forEach(function (s) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "chip";
      btn.textContent = s.label;
      btn.setAttribute("aria-pressed", selected.has(s.key) ? "true" : "false");
      btn.addEventListener("click", function () { toggle(s.key); });
      el.grid.appendChild(btn);
    });
    el.none.hidden = matches.length > 0;
  }

  function renderSelected() {
    el.selList.innerHTML = "";
    selected.forEach(function (key) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "chip chip-remove";
      btn.setAttribute("aria-label", "Remove " + labelFor(key));
      btn.innerHTML = esc(labelFor(key)) + ' <span aria-hidden="true">&times;</span>';
      btn.addEventListener("click", function () { toggle(key); });
      el.selList.appendChild(btn);
    });
    el.selBlock.hidden = selected.size === 0;
    const count = selected.size;
    el.btn.disabled = count < minSymptoms;
    if (count === 0) {
      el.hint.textContent = "Select at least " + minSymptoms + " symptoms to continue.";
    } else if (count < minSymptoms) {
      el.hint.textContent = count + " selected. Add " + (minSymptoms - count) + " more to continue.";
    } else {
      el.hint.textContent = count + " symptom" + (count === 1 ? "" : "s") + " selected. Ready when you are.";
    }
  }

  function toggle(key) {
    if (selected.has(key)) selected.delete(key); else selected.add(key);
    renderChips();
    renderSelected();
  }

  function collectValues() {
    const values = {};
    el.form.querySelectorAll("[name]").forEach(function (input) {
      values[input.name] = input.value.trim();
    });
    return values;
  }

  function gauge(percent, level) {
    const len = (percent / 100 * GAUGE_LENGTH).toFixed(2) + " " + GAUGE_LENGTH.toFixed(2);
    return '<div class="gauge-wrap small risk-' + level.toLowerCase() + '">' +
      '<svg class="gauge" viewBox="0 0 120 120" aria-hidden="true">' +
        '<circle class="gauge-track" cx="60" cy="60" r="54"></circle>' +
        '<circle class="gauge-fill" cx="60" cy="60" r="54" stroke-dasharray="' + len + '"></circle>' +
      "</svg>" +
      '<div class="gauge-label"><span class="gauge-value">' + percent.toFixed(1) + '%</span>' +
      '<span class="gauge-caption">estimated</span></div></div>';
  }

  function riskCard(item) {
    let html = gauge(item.probability, item.risk_level) +
      '<div class="risk-row"><span class="risk-badge risk-' + item.risk_level.toLowerCase() + '">' +
      esc(item.risk_level) + " likelihood</span></div>" +
      '<p class="risk-text">' + esc(item.risk_text) + "</p>";
    if (item.note) html += '<p class="muted small note-box">' + esc(item.note) + "</p>";
    return html + DP.renderInfo(item.info, true);
  }

  function renderResults(data) {
    el.summary.className = "summary tone-" + data.summary.tone;
    el.summary.innerHTML = "<strong>" + esc(data.summary.title) + "</strong> " + esc(data.summary.text);

    el.symResults.innerHTML = "";
    data.symptoms.results.forEach(function (r, i) {
      const li = document.createElement("li");
      li.className = "result-item" + (i === 0 ? " top" : "");
      li.innerHTML =
        '<div class="result-row"><span class="result-name"><span class="rank">' + (i + 1) + "</span>" +
        esc(r.disease) + '</span><span class="result-pct">' + r.probability.toFixed(1) + "%</span></div>" +
        '<div class="bar"><div class="bar-fill" style="width:' + Math.max(r.probability, 2) + '%"></div></div>' +
        (i === 0 ? DP.renderInfo(r.info, true) : "");
      el.symResults.appendChild(li);
    });

    el.heartCard.innerHTML = riskCard(data.heart);
    el.diabetesCard.innerHTML = riskCard(data.diabetes);

    el.flagRows.innerHTML = data.flags.map(function (f) {
      return "<tr><td>" + esc(f.test) + "</td><td>" + esc(f.value) + '</td><td><span class="flag flag-' +
        f.status + '">' + esc(f.label) + "</span></td><td>" + esc(f.message) + "</td></tr>";
    }).join("");

    el.emergency.hidden = data.heart.risk_level !== "Higher";
    el.results.hidden = false;
    el.results.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function showError(messages) {
    el.error.innerHTML = messages.map(function (m) { return esc(m); }).join("<br>");
    el.error.hidden = false;
    el.error.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  el.form.addEventListener("submit", async function (event) {
    event.preventDefault();
    el.error.hidden = true;
    if (selected.size < minSymptoms) {
      showError(["Please select at least " + minSymptoms + " symptoms."]);
      return;
    }
    el.btn.disabled = true;
    el.btn.textContent = "Generating...";
    try {
      const response = await fetch("/api/assess", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: Array.from(selected), values: collectValues() }),
      });
      const data = await response.json();
      if (!response.ok) showError(data.errors || [data.error || "Please check the form and try again."]);
      else renderResults(data);
    } catch (err) {
      showError(["We could not reach the service. Please check the connection and try again."]);
    } finally {
      el.btn.textContent = "Generate assessment";
      renderSelected();
    }
  });

  el.search.addEventListener("input", renderChips);
  el.clear.addEventListener("click", function () { selected.clear(); renderChips(); renderSelected(); });
  el.newCheck.addEventListener("click", function () {
    selected.clear();
    el.search.value = "";
    renderChips();
    renderSelected();
    el.results.hidden = true;
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  renderChips();
  renderSelected();
})();
