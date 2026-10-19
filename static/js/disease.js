(function () {
  "use strict";
  const spec = JSON.parse(document.getElementById("disease-spec").textContent);
  const esc = DP.escapeHtml;
  const form = document.getElementById("predict-form");
  const fieldsEl = document.getElementById("fields");
  const formError = document.getElementById("form-error");
  const submitBtn = document.getElementById("submit-btn");
  const el = {
    placeholder: document.getElementById("placeholder"),
    loading: document.getElementById("loading"),
    error: document.getElementById("error"),
    output: document.getElementById("output"),
    wrap: document.querySelector(".gauge-wrap"),
    fill: document.getElementById("gauge-fill"),
    value: document.getElementById("gauge-value"),
    badge: document.getElementById("risk-badge"),
    riskText: document.getElementById("risk-text"),
    modelLine: document.getElementById("model-line"),
    emergency: document.getElementById("emergency-note"),
    infoSlot: document.getElementById("info-slot"),
    restart: document.getElementById("restart-btn"),
  };
  const GAUGE_LENGTH = 2 * Math.PI * 54;

  function buildForm() {
    fieldsEl.innerHTML = "";
    let lastGroup = null;
    spec.features.forEach(function (f) {
      if (f.group && f.group !== lastGroup) {
        const heading = document.createElement("h3");
        heading.className = "group-title";
        heading.textContent = f.group;
        fieldsEl.appendChild(heading);
        lastGroup = f.group;
      }
      const id = "f-" + f.name;
      const wrap = document.createElement("div");
      wrap.className = "field";
      const unit = f.unit ? ' <span class="unit">(' + esc(f.unit) + ")</span>" : "";
      let control;
      if (f.type === "select") {
        const opts = f.options.map(function (o) {
          const selectedAttr = String(o[0]) === String(f.default) ? " selected" : "";
          return '<option value="' + esc(o[0]) + '"' + selectedAttr + ">" + esc(o[1]) + "</option>";
        }).join("");
        control = '<select id="' + id + '" name="' + esc(f.name) + '">' + opts + "</select>";
      } else {
        control = '<input id="' + id + '" name="' + esc(f.name) + '" type="number" inputmode="decimal"' +
          ' min="' + f.min + '" max="' + f.max + '" step="' + f.step + '" value="' + f.default + '" required>';
      }
      wrap.innerHTML = '<label for="' + id + '">' + esc(f.label) + unit + "</label>" + control +
        (f.help ? '<small class="help">' + esc(f.help) + "</small>" : "");
      fieldsEl.appendChild(wrap);
    });
  }

  function collectValues() {
    const values = {};
    const errors = [];
    spec.features.forEach(function (f) {
      const input = document.getElementById("f-" + f.name);
      const raw = input.value.trim();
      if (raw === "") { errors.push(f.label + " is required."); return; }
      const num = Number(raw);
      if (Number.isNaN(num)) { errors.push(f.label + " must be a number."); return; }
      if (f.type === "number" && (num < f.min || num > f.max)) {
        errors.push(f.label + " should be between " + f.min + " and " + f.max + ".");
        return;
      }
      values[f.name] = num;
    });
    return { values: values, errors: errors };
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

  function renderResult(data) {
    const p = data.probability;
    const level = data.risk_level.toLowerCase();
    el.fill.setAttribute("stroke-dasharray", (p / 100 * GAUGE_LENGTH).toFixed(2) + " " + GAUGE_LENGTH.toFixed(2));
    el.value.textContent = p.toFixed(1) + "%";
    el.wrap.className = "gauge-wrap risk-" + level;
    el.badge.textContent = data.risk_level + " likelihood";
    el.badge.className = "risk-badge risk-" + level;
    el.riskText.textContent = data.risk_text;
    el.modelLine.textContent = "Model: " + spec.best_model + " · Test accuracy " + spec.accuracy + "%";
    el.emergency.hidden = !(spec.key === "heart" && level === "higher");
    el.infoSlot.innerHTML = DP.renderInfo(data.info, true);
    showState("results");
    el.output.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    const collected = collectValues();
    if (collected.errors.length) {
      formError.textContent = collected.errors[0];
      formError.hidden = false;
      return;
    }
    formError.hidden = true;
    showState("loading");
    submitBtn.disabled = true;
    try {
      const response = await fetch("/api/predict/" + spec.key, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ values: collected.values }),
      });
      const data = await response.json();
      if (!response.ok) showError(data.error || "Something went wrong. Please check the values and try again.");
      else renderResult(data);
    } catch (err) {
      showError("We could not reach the service. Please check the connection and try again.");
    } finally {
      submitBtn.disabled = false;
    }
  });

  el.restart.addEventListener("click", function () {
    buildForm();
    showState("idle");
    document.getElementById("predict-form").scrollIntoView({ behavior: "smooth", block: "start" });
  });

  buildForm();
})();
