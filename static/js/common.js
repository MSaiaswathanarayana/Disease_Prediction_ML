/* Shared helpers used by every page. */
window.DP = (function () {
  "use strict";

  function escapeHtml(text) {
    return String(text).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function renderInfo(info, open) {
    if (!info) return "";
    const list = function (items) {
      return "<ul>" + items.map(function (t) { return "<li>" + escapeHtml(t) + "</li>"; }).join("") + "</ul>";
    };
    return (
      '<details class="info"' + (open ? " open" : "") + ">" +
        "<summary>About this condition, precautions and diet</summary>" +
        '<div class="info-body">' +
          "<h4>What it is</h4><p>" + escapeHtml(info.about) + "</p>" +
          "<h4>How it occurs</h4><p>" + escapeHtml(info.how_it_occurs) + "</p>" +
          "<h4>Precautions to take</h4>" + list(info.precautions) +
          "<h4>Foods to eat</h4>" + list(info.diet_follow) +
          "<h4>Foods and habits to avoid</h4>" + list(info.diet_avoid) +
          '<p class="info-note">This is general information, not medical advice. ' +
          "Please speak with a doctor about your own situation.</p>" +
        "</div>" +
      "</details>"
    );
  }

  return { escapeHtml: escapeHtml, renderInfo: renderInfo };
})();
