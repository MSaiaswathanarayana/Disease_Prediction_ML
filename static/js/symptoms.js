(function () {
  "use strict";
  const symptoms = JSON.parse(document.getElementById("symptom-data").textContent);
  const minSymptoms = window.DP_CONFIG.minSymptoms;
  const selected = new Set();
  const escapeHtml = DP.escapeHtml;

  const el = {
    search: document.getElementById("symptom-search"),
    grid: document.getElementById("chip-grid"),
    noMatch: document.getElementById("no-match"),
    selectedBlock: document.getElementById("selected-block"),
    selectedList: document.getElementById("selected-list"),
    clearAll: document.getElementById("clear-all"),
    hint: document.getElementById("hint"),
    checkBtn: document.getElementById("check-btn"),
    placeholder: document.getElementById("placeholder"),
    loading: document.getElementById("loading"),
    error: document.getElementById("error"),
    output: document.getElementById("output"),
    usedLine: document.getElementById("used-line"),
    resultList: document.getElementById("result-list"),
    restart: document.getElementById("restart-btn"),
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
    el.noMatch.hidden = matches.length > 0;
  }

  function renderSelected() {
    el.selectedList.innerHTML = "";
    selected.forEach(function (key) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "chip chip-remove";
      btn.setAttribute("aria-label", "Remove " + labelFor(key));
      btn.innerHTML = escapeHtml(labelFor(key)) + ' <span aria-hidden="true">&times;</span>';
      btn.addEventListener("click", function () { toggle(key); });
      el.selectedList.appendChild(btn);
    });
    el.selectedBlock.hidden = selected.size === 0;

    const count = selected.size;
    const ready = count >= minSymptoms;
    el.checkBtn.disabled = !ready;
    if (count === 0) {
      el.hint.textContent = "Select at least " + minSymptoms + " symptoms to continue.";
    } else if (!ready) {
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

  function showState(state) {
    el.placeholder.hidden = state !== "idle";
    el.loading.hidden = state !== "loading";
    el.output.hidden = state !== "results";
    if (state !== "error") el.error.hidden = true;
  }

  function showError(message) {
    showState("error");
    el.error.textContent = message;
    el.error.hidden = false;
    el.placeholder.hidden = false;
  }

  function renderResults(data) {
    el.usedLine.textContent = "Based on: " + data.symptoms_used.join(", ") + ".";
    el.resultList.innerHTML = "";
    data.results.forEach(function (r, i) {
      const li = document.createElement("li");
      li.className = "result-item" + (i === 0 ? " top" : "");
      li.innerHTML =
        '<div class="result-row">' +
          '<span class="result-name"><span class="rank">' + (i + 1) + "</span>" + escapeHtml(r.disease) + "</span>" +
          '<span class="result-pct">' + r.probability.toFixed(1) + "%</span>" +
        "</div>" +
        '<div class="bar" role="presentation"><div class="bar-fill" style="width:0%"></div></div>' +
        DP.renderInfo(r.info, i === 0);
      el.resultList.appendChild(li);
      requestAnimationFrame(function () {
        li.querySelector(".bar-fill").style.width = Math.max(r.probability, 2) + "%";
      });
    });
    showState("results");
  }

  async function checkSymptoms() {
    if (selected.size < minSymptoms) return;
    showState("loading");
    el.checkBtn.disabled = true;
    try {
      const response = await fetch("/api/symptoms/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: Array.from(selected) }),
      });
      const data = await response.json();
      if (!response.ok) showError(data.error || "Something went wrong. Please try again.");
      else renderResults(data);
    } catch (err) {
      showError("We could not reach the service. Please check the connection and try again.");
    } finally {
      renderSelected();
    }
  }

  el.search.addEventListener("input", renderChips);
  el.clearAll.addEventListener("click", function () {
    selected.clear(); renderChips(); renderSelected(); showState("idle");
  });
  el.checkBtn.addEventListener("click", checkSymptoms);
  el.restart.addEventListener("click", function () {
    selected.clear(); el.search.value = ""; renderChips(); renderSelected(); showState("idle");
    document.getElementById("symptom-card").scrollIntoView({ behavior: "smooth", block: "start" });
  });

  renderChips();
  renderSelected();
})();
