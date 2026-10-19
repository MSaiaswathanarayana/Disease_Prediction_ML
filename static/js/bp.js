(function () {
  "use strict";
  const form = document.getElementById("bp-form");
  const el = {
    error: document.getElementById("bp-error"),
    btn: document.getElementById("bp-btn"),
    placeholder: document.getElementById("bp-placeholder"),
    output: document.getElementById("bp-output"),
    category: document.getElementById("bp-category"),
    meaning: document.getElementById("bp-meaning"),
    steps: document.getElementById("bp-steps"),
    notes: document.getElementById("bp-notes"),
    emergency: document.getElementById("bp-emergency"),
    info: document.getElementById("bp-info"),
  };
  const esc = DP.escapeHtml;

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    el.error.hidden = true;
    el.btn.disabled = true;
    try {
      const response = await fetch("/api/bp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          systolic: document.getElementById("bp-sys").value,
          diastolic: document.getElementById("bp-dia").value,
          on_medication: document.getElementById("bp-med").value === "1",
        }),
      });
      const data = await response.json();
      if (!response.ok) {
        el.error.innerHTML = (data.errors || [data.error]).map(esc).join("<br>");
        el.error.hidden = false;
        return;
      }
      const level = data.risk_level.toLowerCase();
      el.category.textContent = data.category;
      el.category.className = "risk-badge risk-" + level;
      el.meaning.textContent = data.meaning;
      el.steps.innerHTML = data.steps.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("");
      el.notes.innerHTML = data.notes.map(function (n) {
        return '<div class="notice">' + esc(n) + "</div>";
      }).join("");
      el.emergency.hidden = data.risk_level !== "Higher" || data.category !== "Hypertensive crisis";
      el.info.innerHTML = DP.renderInfo(data.info, true);
      el.placeholder.hidden = true;
      el.output.hidden = false;
    } catch (err) {
      el.error.textContent = "We could not reach the service. Please try again.";
      el.error.hidden = false;
    } finally {
      el.btn.disabled = false;
    }
  });
})();
