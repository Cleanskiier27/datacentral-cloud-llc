// Background service worker for Cross Browser CRT Mod
// Manages extension state and communicates with content scripts

// Cross-browser WebExtension API shim: Firefox exposes the promise-based
// `browser` namespace, while Chromium-based browsers expose `chrome`.
// Both accept the callback-style calls used below, so a single alias
// is enough to run unmodified on either family.
const browserAPI = typeof browser !== "undefined" ? browser : chrome;

const DEFAULT_STATE = {
    shaderEnabled: false,
    shaderType: "crt",
    soundsEnabled: false,
    intensity: 0.5
};

// Initialize state on install
browserAPI.runtime.onInstalled.addListener(() => {
    browserAPI.storage.local.set({ modState: DEFAULT_STATE });
});

// Listen for messages from popup and content scripts
browserAPI.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "GET_STATE") {
        browserAPI.storage.local.get("modState", (result) => {
            sendResponse(result.modState || DEFAULT_STATE);
        });
        return true;
    }

    if (message.type === "SET_STATE") {
        browserAPI.storage.local.set({ modState: message.state }, () => {
            // Notify all tabs of state change
            browserAPI.tabs.query({}, (tabs) => {
                for (const tab of tabs) {
                    browserAPI.tabs.sendMessage(tab.id, {
                        type: "STATE_CHANGED",
                        state: message.state
                    }, () => {
                        // Ignore errors for tabs without content script
                        void browserAPI.runtime.lastError;
                    });
                }
            });
            sendResponse({ success: true });
        });
        return true;
    }
});
