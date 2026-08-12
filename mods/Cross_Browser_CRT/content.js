// Content script for Cross Browser CRT Mod
// Applies shader effects and keyboard sounds to web pages

(function () {
    "use strict";

    let state = {
        shaderEnabled: false,
        shaderType: "crt",
        soundsEnabled: false,
        intensity: 0.5
    };

    let audioContext = null;
    let shaderCanvas = null;
    let animationFrameId = null;

    // --- Shader Effect Implementation ---

    const SHADER_PROGRAMS = {
        crt: {
            vertexShader: `
                attribute vec2 a_position;
                attribute vec2 a_texCoord;
                varying vec2 v_texCoord;
                void main() {
                    gl_Position = vec4(a_position, 0.0, 1.0);
                    v_texCoord = a_texCoord;
                }
            `,
            fragmentShader: `
                precision mediump float;
                varying vec2 v_texCoord;
                uniform sampler2D u_image;
                uniform vec2 u_resolution;
                uniform float u_intensity;
                uniform float u_time;

                void main() {
                    vec2 uv = v_texCoord;
                    vec4 color = texture2D(u_image, uv);

                    // Scanline effect
                    float scanline = sin(uv.y * u_resolution.y * 3.14159) * 0.5 + 0.5;
                    scanline = pow(scanline, 1.0 - u_intensity * 0.5);
                    float scanlineEffect = mix(1.0, scanline, u_intensity * 0.3);

                    // RGB mask (shadow mask)
                    float maskScale = 3.0;
                    float col = mod(gl_FragCoord.x, maskScale * 3.0);
                    vec3 mask = vec3(1.0);
                    if (col < maskScale) mask = vec3(1.0, 0.7, 0.7);
                    else if (col < maskScale * 2.0) mask = vec3(0.7, 1.0, 0.7);
                    else mask = vec3(0.7, 0.7, 1.0);
                    mask = mix(vec3(1.0), mask, u_intensity * 0.4);

                    // Chromatic aberration
                    float aberration = u_intensity * 0.002;
                    float r = texture2D(u_image, uv + vec2(aberration, 0.0)).r;
                    float g = color.g;
                    float b = texture2D(u_image, uv - vec2(aberration, 0.0)).b;
                    color = vec4(r, g, b, color.a);

                    // Vignette
                    vec2 vignetteUV = uv * (1.0 - uv);
                    float vignette = vignetteUV.x * vignetteUV.y * 15.0;
                    vignette = pow(vignette, u_intensity * 0.3);

                    color.rgb *= scanlineEffect * mask * vignette;
                    gl_FragColor = color;
                }
            `
        },
        crt_curved: {
            vertexShader: `
                attribute vec2 a_position;
                attribute vec2 a_texCoord;
                varying vec2 v_texCoord;
                void main() {
                    gl_Position = vec4(a_position, 0.0, 1.0);
                    v_texCoord = a_texCoord;
                }
            `,
            fragmentShader: `
                precision mediump float;
                varying vec2 v_texCoord;
                uniform sampler2D u_image;
                uniform vec2 u_resolution;
                uniform float u_intensity;
                uniform float u_time;

                vec2 curveUV(vec2 uv) {
                    uv = uv * 2.0 - 1.0;
                    float curvature = u_intensity * 0.15;
                    uv.x *= 1.0 + pow(abs(uv.y), 2.0) * curvature;
                    uv.y *= 1.0 + pow(abs(uv.x), 2.0) * curvature;
                    uv = uv * 0.5 + 0.5;
                    return uv;
                }

                void main() {
                    vec2 uv = curveUV(v_texCoord);

                    // Out of bounds check for curved screen
                    if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
                        gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
                        return;
                    }

                    vec4 color = texture2D(u_image, uv);

                    // Scanlines
                    float scanline = sin(uv.y * u_resolution.y * 3.14159) * 0.5 + 0.5;
                    scanline = pow(scanline, 1.0 - u_intensity * 0.5);
                    float scanlineEffect = mix(1.0, scanline, u_intensity * 0.3);

                    // RGB shadow mask
                    float maskScale = 3.0;
                    float col = mod(gl_FragCoord.x, maskScale * 3.0);
                    vec3 mask = vec3(1.0);
                    if (col < maskScale) mask = vec3(1.0, 0.7, 0.7);
                    else if (col < maskScale * 2.0) mask = vec3(0.7, 1.0, 0.7);
                    else mask = vec3(0.7, 0.7, 1.0);
                    mask = mix(vec3(1.0), mask, u_intensity * 0.4);

                    // Chromatic aberration
                    float aberration = u_intensity * 0.003;
                    float r = texture2D(u_image, uv + vec2(aberration, 0.0)).r;
                    float g = color.g;
                    float b = texture2D(u_image, uv - vec2(aberration, 0.0)).b;
                    color = vec4(r, g, b, color.a);

                    // Vignette (stronger for curved)
                    vec2 vignetteUV = uv * (1.0 - uv);
                    float vignette = vignetteUV.x * vignetteUV.y * 15.0;
                    vignette = pow(vignette, u_intensity * 0.5);

                    color.rgb *= scanlineEffect * mask * vignette;
                    gl_FragColor = color;
                }
            `
        }
    };

    function createShaderOverlay() {
        if (shaderCanvas) return;

        shaderCanvas = document.createElement("canvas");
        shaderCanvas.id = "crt-mod-shader-canvas";
        shaderCanvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 2147483647;
            mix-blend-mode: multiply;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        document.documentElement.appendChild(shaderCanvas);
    }

    function initWebGL() {
        if (!shaderCanvas) createShaderOverlay();

        const gl = shaderCanvas.getContext("webgl", {
            premultipliedAlpha: false,
            alpha: true
        });

        if (!gl) {
            // Fallback to CSS filter if WebGL unavailable
            applyCSSFallback();
            return null;
        }

        return gl;
    }

    function compileShader(gl, source, type) {
        const shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
            console.error("CRT Mod: Shader compile error:", gl.getShaderInfoLog(shader));
            gl.deleteShader(shader);
            return null;
        }
        return shader;
    }

    function createProgram(gl, vertexSource, fragmentSource) {
        const vertexShader = compileShader(gl, vertexSource, gl.VERTEX_SHADER);
        const fragmentShader = compileShader(gl, fragmentSource, gl.FRAGMENT_SHADER);
        if (!vertexShader || !fragmentShader) return null;

        const program = gl.createProgram();
        gl.attachShader(program, vertexShader);
        gl.attachShader(program, fragmentShader);
        gl.linkProgram(program);

        if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
            console.error("CRT Mod: Program link error:", gl.getProgramInfoLog(program));
            return null;
        }

        return program;
    }

    function startShaderEffect() {
        createShaderOverlay();
        const gl = initWebGL();

        if (!gl) return;

        const shaderDef = SHADER_PROGRAMS[state.shaderType] || SHADER_PROGRAMS.crt;
        const program = createProgram(gl, shaderDef.vertexShader, shaderDef.fragmentShader);
        if (!program) return;

        // Set up geometry (full-screen quad)
        const positions = new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]);
        const texCoords = new Float32Array([0, 1, 1, 1, 0, 0, 1, 0]);

        const posBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, posBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);

        const texBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, texBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, texCoords, gl.STATIC_DRAW);

        // Create a 1x1 transparent texture (overlay effect only)
        const texture = gl.createTexture();
        gl.bindTexture(gl.TEXTURE_2D, texture);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE,
            new Uint8Array([255, 255, 255, 255]));

        gl.useProgram(program);

        const posLoc = gl.getAttribLocation(program, "a_position");
        const texLoc = gl.getAttribLocation(program, "a_texCoord");
        const resLoc = gl.getUniformLocation(program, "u_resolution");
        const intensityLoc = gl.getUniformLocation(program, "u_intensity");
        const timeLoc = gl.getUniformLocation(program, "u_time");

        shaderCanvas.style.opacity = "1";

        function render(time) {
            if (!state.shaderEnabled) {
                stopShaderEffect();
                return;
            }

            const width = window.innerWidth;
            const height = window.innerHeight;

            if (shaderCanvas.width !== width || shaderCanvas.height !== height) {
                shaderCanvas.width = width;
                shaderCanvas.height = height;
                gl.viewport(0, 0, width, height);
            }

            gl.clear(gl.COLOR_BUFFER_BIT);

            gl.bindBuffer(gl.ARRAY_BUFFER, posBuffer);
            gl.enableVertexAttribArray(posLoc);
            gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

            gl.bindBuffer(gl.ARRAY_BUFFER, texBuffer);
            gl.enableVertexAttribArray(texLoc);
            gl.vertexAttribPointer(texLoc, 2, gl.FLOAT, false, 0, 0);

            gl.uniform2f(resLoc, width, height);
            gl.uniform1f(intensityLoc, state.intensity);
            gl.uniform1f(timeLoc, time * 0.001);

            gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);

            animationFrameId = requestAnimationFrame(render);
        }

        animationFrameId = requestAnimationFrame(render);
    }

    function stopShaderEffect() {
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
        if (shaderCanvas) {
            shaderCanvas.style.opacity = "0";
        }
    }

    function applyCSSFallback() {
        // CSS-only fallback for browsers without WebGL
        const style = document.createElement("style");
        style.id = "crt-mod-css-fallback";
        style.textContent = `
            html.crt-mod-active::after {
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                pointer-events: none;
                z-index: 2147483647;
                background: repeating-linear-gradient(
                    0deg,
                    rgba(0, 0, 0, 0.1) 0px,
                    rgba(0, 0, 0, 0.1) 1px,
                    transparent 1px,
                    transparent 3px
                );
                animation: crt-flicker 0.05s infinite;
            }
            @keyframes crt-flicker {
                0% { opacity: 0.97; }
                50% { opacity: 1.0; }
                100% { opacity: 0.98; }
            }
        `;
        document.head.appendChild(style);
        document.documentElement.classList.add("crt-mod-active");
    }

    function removeCSSFallback() {
        const style = document.getElementById("crt-mod-css-fallback");
        if (style) style.remove();
        document.documentElement.classList.remove("crt-mod-active");
    }

    // --- Keyboard Sound Implementation ---

    const KEY_SOUNDS = {
        letter: { frequency: 800, duration: 0.03, type: "square" },
        space: { frequency: 400, duration: 0.05, type: "square" },
        enter: { frequency: 600, duration: 0.06, type: "sawtooth" },
        backspace: { frequency: 500, duration: 0.04, type: "triangle" }
    };

    function getAudioContext() {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        return audioContext;
    }

    function playKeySound(keyType) {
        if (!state.soundsEnabled) return;

        try {
            const ctx = getAudioContext();
            if (ctx.state === "suspended") {
                ctx.resume();
            }

            const soundDef = KEY_SOUNDS[keyType] || KEY_SOUNDS.letter;

            const oscillator = ctx.createOscillator();
            const gainNode = ctx.createGain();

            oscillator.type = soundDef.type;
            oscillator.frequency.setValueAtTime(soundDef.frequency, ctx.currentTime);

            // Quick attack and decay for mechanical key feel
            gainNode.gain.setValueAtTime(0, ctx.currentTime);
            gainNode.gain.linearRampToValueAtTime(0.15 * state.intensity, ctx.currentTime + 0.005);
            gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + soundDef.duration);

            oscillator.connect(gainNode);
            gainNode.connect(ctx.destination);

            oscillator.start(ctx.currentTime);
            oscillator.stop(ctx.currentTime + soundDef.duration + 0.01);
        } catch (e) {
            // Audio may not be available
        }
    }

    function handleKeyDown(event) {
        if (!state.soundsEnabled) return;

        if (event.key === " ") {
            playKeySound("space");
        } else if (event.key === "Enter") {
            playKeySound("enter");
        } else if (event.key === "Backspace") {
            playKeySound("backspace");
        } else if (event.key.length === 1) {
            playKeySound("letter");
        }
    }

    // --- State Management ---

    function applyState() {
        if (state.shaderEnabled) {
            startShaderEffect();
        } else {
            stopShaderEffect();
            removeCSSFallback();
        }

        if (state.soundsEnabled) {
            document.addEventListener("keydown", handleKeyDown, true);
        } else {
            document.removeEventListener("keydown", handleKeyDown, true);
        }
    }

    // Listen for state changes from background/popup
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.type === "STATE_CHANGED") {
            state = message.state;
            applyState();
        }
        if (message.type === "PING") {
            sendResponse({ active: true });
        }
    });

    // Load initial state
    chrome.runtime.sendMessage({ type: "GET_STATE" }, (response) => {
        if (chrome.runtime.lastError || !response) return;
        state = response;
        applyState();
    });
})();
