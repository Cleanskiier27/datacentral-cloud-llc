// Background service worker for Cross Browser CRT Mod
// Manages extension state and communicates with content scripts

const DEFAULT_STATE = {
    shaderEnabled: false,
    shaderType: "crt",
    soundsEnabled: false,
    intensity: 0.5
};

// Initialize state on install
chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.local.set({ modState: DEFAULT_STATE });
});

// Listen for messages from popup and content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "GET_STATE") {
        chrome.storage.local.get("modState", (result) => {
            sendResponse(result.modState || DEFAULT_STATE);
        });
        return true;
    }

    if (message.type === "SET_STATE") {
        chrome.storage.local.set({ modState: message.state }, () => {
            // Notify all tabs of state change
            chrome.tabs.query({}, (tabs) => {
                for (const tab of tabs) {
                    chrome.tabs.sendMessage(tab.id, {
                        type: "STATE_CHANGED",
                        state: message.state
                    }, () => {
                        // Ignore errors for tabs without content script
                        void chrome.runtime.lastError;
                    });
                }
            });
            sendResponse({ success: true });
        });
        return true;
    }
});
