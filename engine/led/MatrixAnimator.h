#ifndef MATRIX_ANIMATOR_H
#define MATRIX_ANIMATOR_H

#include <string>
#include <vector>
#include <cstdint>

// ---------------------------------------------------------------------------
// MatrixAnimator
//
// Renders a "digital rain" ASCII matrix on a 2D LED grid, with support for
// overlaying screenplay text and exporting each frame as an LED brightness
// map (values in [0.0, 1.0]) that can be fed directly into LEDBoard.
//
// Terminology
//   column  – one vertical "rain streak" driven by a ColumnStream
//   cell    – one character position in the rows×cols grid
//   frame   – the full grid state at one point in time; produced by tick()
// ---------------------------------------------------------------------------
class MatrixAnimator {
public:
    // Character sets used for the falling rain glyphs.
    // MATRIX_CHARS – half-width katakana + digits (classic Matrix look)
    // BINARY_CHARS  – binary digits only
    // HEX_CHARS     – hexadecimal digits
    // CUSTOM_CHARS  – user-supplied via setCharSet()
    enum CharSet { MATRIX_CHARS, BINARY_CHARS, HEX_CHARS, CUSTOM_CHARS };

    // -----------------------------------------------------------------------
    // Construction / configuration
    // -----------------------------------------------------------------------

    // Construct an animator for a grid of `rows` rows and `cols` columns.
    // `seed` controls the PRNG so that simulations are reproducible.
    MatrixAnimator(int rows, int cols, unsigned int seed = 42);

    // Set the character set used for rain glyphs.
    void setCharSet(CharSet cs, const std::string& custom = "");

    // Load a multi-line screenplay / ASCII-art that will be blended as a
    // static foreground overlay on top of the rain.  Each '\n'-separated line
    // of `art` maps to one row; lines are left-padded/clipped to fit `cols`.
    void loadScreenplay(const std::string& art);

    // Control how strongly the foreground overlay overrides the rain.
    // 0.0 = pure rain, 1.0 = pure overlay (default 0.6).
    void setOverlayStrength(double strength);

    // -----------------------------------------------------------------------
    // Animation control
    // -----------------------------------------------------------------------

    // Advance the simulation by one frame.
    // Call this in your rendering loop; each call updates every ColumnStream.
    void tick();

    // Reset all streams to a freshly seeded state and clear the frame.
    void reset();

    // -----------------------------------------------------------------------
    // Frame accessors
    // -----------------------------------------------------------------------

    // Return the character at grid position (row, col) in the current frame.
    char charAt(int row, int col) const;

    // Return the brightness of cell (row, col) in [0.0, 1.0].
    // Head glyphs are brightest (1.0), trailing glyphs fade toward 0.0.
    double brightnessAt(int row, int col) const;

    // Flatten the 2D brightness grid into a 1D vector (row-major order).
    // Convenient for passing directly to LEDBoard::displayMatrix().
    std::vector<double> flatBrightness() const;

    // Return a rendered frame as a printable multi-line string.
    // Each cell is represented by its character; brightness is lost.
    std::string renderText() const;

    // Return a rendered frame as a multi-line string with ANSI green shading.
    // Cells are coloured according to their brightness using 256-colour codes.
    std::string renderAnsi() const;

    // -----------------------------------------------------------------------
    // Getters
    // -----------------------------------------------------------------------
    int rows() const { return rows_; }
    int cols() const { return cols_; }
    int frameCount() const { return frameCount_; }

private:
    // -----------------------------------------------------------------------
    // Internal types
    // -----------------------------------------------------------------------

    // One vertical "rain streak" in a single column.
    struct ColumnStream {
        int  headRow;      // current row of the leading (brightest) glyph
        int  length;       // number of glyphs in the trail
        int  speed;        // rows advanced per tick (1 or 2)
        int  delay;        // ticks remaining before this stream starts/restarts
        bool active;       // whether the stream is currently falling
    };

    // One cell in the display grid.
    struct Cell {
        char   ch;         // character currently displayed
        double brightness; // [0.0, 1.0] – brightness driven by ColumnStream
        bool   overlay;    // true when overridden by the screenplay foreground
    };

    // -----------------------------------------------------------------------
    // Helpers
    // -----------------------------------------------------------------------
    void   initStreams();
    void   advanceStream(int col);
    char   randomChar();

    // Simple linear-congruential PRNG (reproducible across platforms).
    uint32_t nextRand();

    // -----------------------------------------------------------------------
    // Data members
    // -----------------------------------------------------------------------
    int rows_;
    int cols_;
    unsigned int seed_;
    uint32_t     rngState_;
    int          frameCount_;

    CharSet     charSet_;
    std::string customChars_;

    std::vector<ColumnStream> streams_;          // one per column
    std::vector<std::vector<Cell>> grid_;        // [row][col]
    std::vector<std::vector<char>> overlay_;     // [row][col] – screenplay text
    bool   hasOverlay_;
    double overlayStrength_;
};

#endif // MATRIX_ANIMATOR_H
