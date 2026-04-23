/* R_eff interactive explorer
 *
 * R_eff = β · (1 − ρ) · (1 − τ) · (1 + γ ρ τ)
 *
 * Reads sliders #slider-beta, #slider-rho, #slider-tau, #slider-gamma.
 * Writes computed value and regime label to #reff-result.
 */
(function () {
  'use strict';

  function reff(beta, rho, tau, gamma) {
    return beta * (1 - rho) * (1 - tau) * (1 + gamma * rho * tau);
  }

  function update() {
    var beta  = parseFloat(document.getElementById('slider-beta').value);
    var rho   = parseFloat(document.getElementById('slider-rho').value);
    var tau   = parseFloat(document.getElementById('slider-tau').value);
    var gamma = parseFloat(document.getElementById('slider-gamma').value);

    document.getElementById('val-beta').textContent  = beta.toFixed(1);
    document.getElementById('val-rho').textContent   = rho.toFixed(2);
    document.getElementById('val-tau').textContent   = tau.toFixed(2);
    document.getElementById('val-gamma').textContent = gamma.toFixed(2);

    var r = reff(beta, rho, tau, gamma);
    var el = document.getElementById('reff-result');
    el.textContent = 'Rₛᵉᶠᶠ = ' + r.toFixed(3);

    if (Math.abs(r - 1) < 0.02) {
      el.className = 'critical';
      el.textContent += '  — critical boundary';
    } else if (r < 1) {
      el.className = 'damped';
      el.textContent += '  — damped (self-healing)';
    } else {
      el.className = 'turbulent';
      el.textContent += '  — turbulent (self-destabilizing)';
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    var ids = ['slider-beta', 'slider-rho', 'slider-tau', 'slider-gamma'];
    ids.forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.addEventListener('input', update);
    });
    update();
  });
})();
