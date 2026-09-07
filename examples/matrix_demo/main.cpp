// matrix_demo/main.cpp
//
// Demonstrates the MatrixAnimator driving the LEDBoard in three modes:
//
//   Mode 1 – Snapshot frames (plain text, no ANSI)
//     Renders a fixed number of frames of the digital rain and prints each
//     frame's brightness grid via LEDBoard::displayMatrix().  This mode
//     works in any terminal and in CI pipelines.
//
//   Mode 2 – Screenplay overlay
//     Loads assets/matrix_screenplay.txt as a foreground overlay and shows
//     how the screenplay text is blended with the falling rain, printed via
//     LEDBoard::displayCharMatrix().
//
//   Mode 3 – Continuous ANSI animation (optional, enabled by --ansi flag)
//     Prints full-colour ANSI frames in a loop.  Requires a colour terminal.
//     Press Ctrl+C to exit.
//
// Usage:
//   matrix_demo               # run modes 1 and 2 (CI-safe)
//   matrix_demo --ansi        # add continuous ANSI animation loop
//   matrix_demo --ansi --fps <n>   # set frames-per-second (default 10)
//   matrix_demo --rows <r> --cols <c>   # grid dimensions (default 20x60)
//   matrix_demo --seed <n>    # PRNG seed (default 42)
//   matrix_demo --screenplay <path>     # custom screenplay file
//   matrix_demo --frames <n>  # frames to render in mode 1 (default 5)

#include <chrono>
#include <cstring>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

#include "../../engine/led/LEDBoard.h"
#include "../../engine/led/MatrixAnimator.h"

// ---------------------------------------------------------------------------
// Utility: read a whole file into a string.
// ---------------------------------------------------------------------------
static bool readFile(const std::string& path, std::string& out)
{
    std::ifstream f(path);
    if (!f.is_open()) return false;
    std::ostringstream ss;
    ss << f.rdbuf();
    out = ss.str();
    return true;
}

// ---------------------------------------------------------------------------
// Utility: clear terminal screen (ANSI).
// ---------------------------------------------------------------------------
static void clearScreen()
{
    std::cout << "\033[2J\033[H" << std::flush;
}

// ---------------------------------------------------------------------------
// Utility: print a section header.
// ---------------------------------------------------------------------------
static void printHeader(const std::string& title)
{
    const int WIDTH = 72;
    std::cout << '\n';
    std::cout << std::string(WIDTH, '=') << '\n';
    int pad = (WIDTH - static_cast<int>(title.size())) / 2;
    if (pad > 0) std::cout << std::string(static_cast<size_t>(pad), ' ');
    std::cout << title << '\n';
    std::cout << std::string(WIDTH, '=') << '\n';
}

// ---------------------------------------------------------------------------
// Mode 1: snapshot frames via LEDBoard::displayMatrix
// ---------------------------------------------------------------------------
static void runSnapshotFrames(int rows, int cols, unsigned int seed,
                               int numFrames)
{
    printHeader("MODE 1 – Digital Rain Snapshot Frames (LEDBoard::displayMatrix)");

    MatrixAnimator anim(rows, cols, seed);
    LEDBoard board(0.0);

    for (int f = 0; f < numFrames; ++f) {
        anim.tick();

        std::string frameLabel = "Frame " + std::to_string(f + 1) +
                                 " / " + std::to_string(numFrames) +
                                 "  (seed=" + std::to_string(seed) + ")";
        board.displayMatrix(frameLabel, anim.flatBrightness(), rows, cols);

        // Show per-frame stats.
        std::cout << "  Active cells with brightness > 0.5: ";
        int active = 0;
        for (double b : anim.flatBrightness()) {
            if (b > 0.5) ++active;
        }
        std::cout << active << " / " << (rows * cols) << '\n';
        std::cout << '\n';
    }
}

// ---------------------------------------------------------------------------
// Mode 2: screenplay overlay via LEDBoard::displayCharMatrix
// ---------------------------------------------------------------------------
static void runScreenplayMode(int rows, int cols, unsigned int seed,
                               int numFrames, const std::string& screenplayPath)
{
    printHeader("MODE 2 – Screenplay Overlay (LEDBoard::displayCharMatrix)");

    MatrixAnimator anim(rows, cols, seed);
    anim.setCharSet(MatrixAnimator::BINARY_CHARS);

    // Load screenplay.
    std::string play;
    if (!screenplayPath.empty() && readFile(screenplayPath, play)) {
        anim.loadScreenplay(play);
        std::cout << "Loaded screenplay from: " << screenplayPath << '\n';
    } else {
        // Fallback: inline mini-screenplay.
        std::ostringstream mini;
        mini << "  NETWORK BUSTER :: MATRIX INITIALIZED\n";
        mini << "  >> LED BOARD ONLINE\n";
        mini << "  >> DATACENTRAL CLOUD LLC\n";
        mini << '\n';
        mini << "   ██████╗  █████╗ ████████╗ █████╗ \n";
        mini << "   ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗\n";
        mini << "   ██║  ██║███████║   ██║   ███████║\n";
        mini << "   ██║  ██║██╔══██║   ██║   ██╔══██║\n";
        mini << "   ██████╔╝██║  ██║   ██║   ██║  ██║\n";
        mini << "   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝\n";
        mini << '\n';
        mini << "  >> INITIATING ANIMATION SEQUENCE\n";
        anim.loadScreenplay(mini.str());
        std::cout << "(using inline mini-screenplay)\n";
    }
    anim.setOverlayStrength(0.7);

    LEDBoard board(0.1);  // threshold > 0 so very dim cells disappear

    // Collect all characters into a flat string for displayCharMatrix.
    for (int f = 0; f < numFrames; ++f) {
        anim.tick();

        // Build char string row-major.
        std::string chars;
        chars.reserve(static_cast<size_t>(rows * cols));
        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < cols; ++c) {
                chars += anim.charAt(r, c);
            }
        }

        std::string frameLabel = "Screenplay frame " + std::to_string(f + 1) +
                                 " (overlay_strength=0.70)";
        board.displayCharMatrix(frameLabel, chars, anim.flatBrightness(),
                                rows, cols);
        std::cout << '\n';
    }
}

// ---------------------------------------------------------------------------
// Mode 3: continuous ANSI animation loop
// ---------------------------------------------------------------------------
static void runAnsiLoop(int rows, int cols, unsigned int seed, int fps,
                         const std::string& screenplayPath)
{
    printHeader("MODE 3 – Continuous ANSI Animation (Ctrl+C to exit)");
    std::cout << "Grid: " << rows << "x" << cols
              << "  FPS: " << fps
              << "  Seed: " << seed << '\n';
    std::cout << "Press Ctrl+C to stop.\n";

    MatrixAnimator anim(rows, cols, seed);

    // Optionally load screenplay overlay.
    std::string play;
    if (!screenplayPath.empty() && readFile(screenplayPath, play)) {
        anim.loadScreenplay(play);
        anim.setOverlayStrength(0.65);
    }

    // Use hex characters for variety in the continuous mode.
    anim.setCharSet(MatrixAnimator::HEX_CHARS);

    // Minimum frame delay used when fps <= 0 (defensive fallback: 10 FPS).
    const int DEFAULT_FRAME_DELAY_MS = 100;
    const int frameDelayMs = (fps > 0) ? 1000 / fps : DEFAULT_FRAME_DELAY_MS;

    while (true) {
        anim.tick();
        clearScreen();
        std::cout << "\033[32m";   // set global green base colour
        std::cout << anim.renderAnsi();
        std::cout << "\033[0m";
        std::cout << " Frame " << anim.frameCount()
                  << " | Grid " << rows << 'x' << cols
                  << " | FPS target " << fps
                  << " | Seed " << seed << std::flush;
        std::this_thread::sleep_for(std::chrono::milliseconds(frameDelayMs));
    }
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------
int main(int argc, char* argv[])
{
    // --- Default parameters ---
    int         rows           = 20;
    int         cols           = 60;
    unsigned int seed          = 42;
    int         snapshotFrames = 5;
    int         fps            = 10;
    bool        ansiMode       = false;
    std::string screenplayPath = "assets/matrix_screenplay.txt";

    // --- Parse arguments ---
    for (int i = 1; i < argc; ++i) {
        if (std::strcmp(argv[i], "--ansi") == 0) {
            ansiMode = true;
        } else if (std::strcmp(argv[i], "--rows") == 0 && i + 1 < argc) {
            rows = std::atoi(argv[++i]);
        } else if (std::strcmp(argv[i], "--cols") == 0 && i + 1 < argc) {
            cols = std::atoi(argv[++i]);
        } else if (std::strcmp(argv[i], "--seed") == 0 && i + 1 < argc) {
            seed = static_cast<unsigned int>(std::atoi(argv[++i]));
        } else if (std::strcmp(argv[i], "--frames") == 0 && i + 1 < argc) {
            snapshotFrames = std::atoi(argv[++i]);
        } else if (std::strcmp(argv[i], "--fps") == 0 && i + 1 < argc) {
            fps = std::atoi(argv[++i]);
        } else if (std::strcmp(argv[i], "--screenplay") == 0 && i + 1 < argc) {
            screenplayPath = argv[++i];
        } else if (std::strcmp(argv[i], "--help") == 0 ||
                   std::strcmp(argv[i], "-h") == 0) {
            std::cout <<
                "Usage: matrix_demo [options]\n"
                "  --rows <n>          grid height (default 20)\n"
                "  --cols <n>          grid width  (default 60)\n"
                "  --seed <n>          PRNG seed   (default 42)\n"
                "  --frames <n>        snapshot frames in mode 1 (default 5)\n"
                "  --ansi              enable continuous ANSI mode 3\n"
                "  --fps <n>           frames per second for ANSI mode (default 10)\n"
                "  --screenplay <path> screenplay file (default assets/matrix_screenplay.txt)\n";
            return 0;
        }
    }

    // Clamp reasonable values.
    if (rows < 2) rows = 2;
    if (cols < 4) cols = 4;
    if (snapshotFrames < 1) snapshotFrames = 1;
    if (fps < 1) fps = 1;

    std::cout << "=== Network Buster :: Matrix LED Board Demo ===\n";
    std::cout << "Grid " << rows << "x" << cols
              << " | seed " << seed << '\n';

    // Mode 1 – always run (CI-safe).
    runSnapshotFrames(rows, cols, seed, snapshotFrames);

    // Mode 2 – always run.
    runScreenplayMode(rows, cols, seed, snapshotFrames, screenplayPath);

    // Mode 3 – only when --ansi is passed (requires an interactive terminal).
    if (ansiMode) {
        runAnsiLoop(rows, cols, seed, fps, screenplayPath);
    }

    std::cout << "\nDone.\n";
    return 0;
}
