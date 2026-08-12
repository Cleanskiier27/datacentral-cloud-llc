// Popup script for CRT Mod controls
document.addEventListener("DOMContentLoaded", () => {
    const shaderToggle = document.getElementById("shader-toggle");
    const shaderType = document.getElementById("shader-type");
    const intensitySlider = document.getElementById("intensity-slider");
    const intensityValue = document.getElementById("intensity-value");
    const soundToggle = document.getElementById("sound-toggle");

    // Load current state
    chrome.runtime.sendMessage({ type: "GET_STATE" }, (response) => {
        if (chrome.runtime.lastError || !response) return;
        if (response) {
            shaderToggle.checked = response.shaderEnabled;
            shaderType.value = response.shaderType || "crt";
            intensitySlider.value = (response.intensity || 0.5) * 100;
            intensityValue.textContent = Math.round((response.intensity || 0.5) * 100) + "%";
            soundToggle.checked = response.soundsEnabled;
        }
    });

    function saveState() {
        const newState = {
            shaderEnabled: shaderToggle.checked,
            shaderType: shaderType.value,
            intensity: intensitySlider.value / 100,
            soundsEnabled: soundToggle.checked
        };

        chrome.runtime.sendMessage({ type: "SET_STATE", state: newState });
    }

    shaderToggle.addEventListener("change", saveState);
    shaderType.addEventListener("change", saveState);
    soundToggle.addEventListener("change", saveState);

    intensitySlider.addEventListener("input", () => {
        intensityValue.textContent = intensitySlider.value + "%";
    });

    intensitySlider.addEventListener("change", saveState);
});
