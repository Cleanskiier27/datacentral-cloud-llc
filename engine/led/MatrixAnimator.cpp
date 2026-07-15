#include "MatrixAnimator.h"

#include <algorithm>
#include <cstring>
#include <sstream>
#include <stdexcept>

// ---------------------------------------------------------------------------
// Character set definitions
// ---------------------------------------------------------------------------

// Half-width katakana (U+FF65..U+FF9F) rendered as printable ASCII proxies,
// interspersed with digits to match the classic Matrix visual.
static const char MATRIX_CHARSET[] =
    "0123456789"
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "!@#$%^&*()_+-=[]{}|;:,./<>?";

static const char BINARY_CHARSET[] = "01";

static const char HEX_CHARSET[] = "0123456789ABCDEF";

// ---------------------------------------------------------------------------
// Construction
// ---------------------------------------------------------------------------

MatrixAnimator::MatrixAnimator(int rows, int cols, unsigned int seed)
    : rows_(rows)
    , cols_(cols)
    , seed_(seed)
    , rngState_(static_cast<uint32_t>(seed))
    , frameCount_(0)
    , charSet_(MATRIX_CHARS)
    , hasOverlay_(false)
    , overlayStrength_(0.6)
{
    if (rows_ < 1 || cols_ < 1) {
        throw std::invalid_argument("MatrixAnimator: rows and cols must be >= 1");
    }

    // Allocate grid.
    grid_.assign(rows_, std::vector<Cell>(cols_, {' ', 0.0, false}));
    overlay_.assign(rows_, std::vector<char>(cols_, ' '));

    streams_.resize(cols_);
    initStreams();
}

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

void MatrixAnimator::setCharSet(CharSet cs, const std::string& custom)
{
    charSet_ = cs;
    if (cs == CUSTOM_CHARS) {
        if (custom.empty()) {
            throw std::invalid_argument("MatrixAnimator::setCharSet: custom char set must not be empty");
        }
        customChars_ = custom;
    }
}

void MatrixAnimator::loadScreenplay(const std::string& art)
{
    // Clear existing overlay.
    for (auto& row : overlay_) {
        std::fill(row.begin(), row.end(), ' ');
    }

    std::istringstream iss(art);
    std::string line;
    int row = 0;
    while (std::getline(iss, line) && row < rows_) {
        for (int col = 0; col < cols_ && col < static_cast<int>(line.size()); ++col) {
            overlay_[row][col] = line[col];
        }
        ++row;
    }
    hasOverlay_ = true;
}

void MatrixAnimator::setOverlayStrength(double strength)
{
    overlayStrength_ = std::max(0.0, std::min(1.0, strength));
}

// ---------------------------------------------------------------------------
// Animation
// ---------------------------------------------------------------------------

void MatrixAnimator::tick()
{
    // Decay all brightnesses by a fixed factor each frame.
    const double DECAY = 0.15;
    for (int r = 0; r < rows_; ++r) {
        for (int c = 0; c < cols_; ++c) {
            grid_[r][c].brightness = std::max(0.0, grid_[r][c].brightness - DECAY);
            // Randomise trail characters occasionally to create the "shimmer" effect.
            if (grid_[r][c].brightness > 0.05 && (nextRand() % 8 == 0)) {
                grid_[r][c].ch = randomChar();
            }
        }
    }

    // Advance each column stream.
    for (int c = 0; c < cols_; ++c) {
        advanceStream(c);
    }

    // Apply overlay if loaded.
    if (hasOverlay_) {
        for (int r = 0; r < rows_; ++r) {
            for (int c = 0; c < cols_; ++c) {
                char ov = overlay_[r][c];
                if (ov != ' ') {
                    // Blend: overlay characters appear with overlayStrength_ brightness boost.
                    grid_[r][c].ch       = ov;
                    grid_[r][c].brightness = std::min(1.0,
                        grid_[r][c].brightness * (1.0 - overlayStrength_) + overlayStrength_);
                    grid_[r][c].overlay  = true;
                } else {
                    grid_[r][c].overlay = false;
                }
            }
        }
    }

    ++frameCount_;
}

void MatrixAnimator::reset()
{
    rngState_ = static_cast<uint32_t>(seed_);
    frameCount_ = 0;
    for (auto& row : grid_) {
        for (auto& cell : row) {
            cell = {' ', 0.0, false};
        }
    }
    initStreams();
}

// ---------------------------------------------------------------------------
// Frame accessors
// ---------------------------------------------------------------------------

char MatrixAnimator::charAt(int row, int col) const
{
    return grid_.at(row).at(col).ch;
}

double MatrixAnimator::brightnessAt(int row, int col) const
{
    return grid_.at(row).at(col).brightness;
}

std::vector<double> MatrixAnimator::flatBrightness() const
{
    std::vector<double> flat;
    flat.reserve(static_cast<size_t>(rows_) * static_cast<size_t>(cols_));
    for (const auto& row : grid_) {
        for (const auto& cell : row) {
            flat.push_back(cell.brightness);
        }
    }
    return flat;
}

std::string MatrixAnimator::renderText() const
{
    std::string out;
    out.reserve(static_cast<size_t>((cols_ + 1) * rows_));
    for (int r = 0; r < rows_; ++r) {
        for (int c = 0; c < cols_; ++c) {
            out += grid_[r][c].ch;
        }
        out += '\n';
    }
    return out;
}

std::string MatrixAnimator::renderAnsi() const
{
    // Map brightness [0,1] -> one of four 256-colour green shades.
    // ANSI: \033[38;5;<n>m
    static const int GREEN_SHADES[] = {
        22,   // very dark green  (brightness 0.00 – 0.25)
        34,   // dark green       (brightness 0.25 – 0.50)
        40,   // medium green     (brightness 0.50 – 0.75)
        46,   // bright green     (brightness 0.75 – 1.00)
    };
    static const char RESET[] = "\033[0m";

    std::string out;
    out.reserve(static_cast<size_t>((cols_ * 14 + 5) * rows_));

    for (int r = 0; r < rows_; ++r) {
        for (int c = 0; c < cols_; ++c) {
            const Cell& cell = grid_[r][c];
            if (cell.brightness < 0.01) {
                out += ' ';
                continue;
            }
            int shade_idx = static_cast<int>(cell.brightness * 3.99);
            shade_idx = std::max(0, std::min(3, shade_idx));

            // Head glyph: bold white for maximum contrast.
            if (cell.brightness > 0.95) {
                out += "\033[1;97m";
            } else {
                out += "\033[38;5;";
                out += std::to_string(GREEN_SHADES[shade_idx]);
                out += 'm';
            }
            out += cell.ch;
            out += RESET;
        }
        out += '\n';
    }
    return out;
}

// ---------------------------------------------------------------------------
// Private helpers
// ---------------------------------------------------------------------------

void MatrixAnimator::initStreams()
{
    for (int c = 0; c < cols_; ++c) {
        ColumnStream& s = streams_[c];
        s.headRow = -1;
        s.length  = 3 + static_cast<int>(nextRand() % static_cast<uint32_t>(rows_ / 2 + 1));
        s.speed   = 1 + static_cast<int>(nextRand() % 2);   // 1 or 2
        s.delay   = static_cast<int>(nextRand() % static_cast<uint32_t>(rows_));
        s.active  = false;
    }
}

void MatrixAnimator::advanceStream(int col)
{
    ColumnStream& s = streams_[col];

    if (!s.active) {
        if (s.delay > 0) {
            --s.delay;
            return;
        }
        s.active  = true;
        s.headRow = 0;
    }

    // Advance by stream speed.
    for (int step = 0; step < s.speed; ++step) {
        if (s.headRow < rows_) {
            // Paint the head glyph at full brightness.
            grid_[s.headRow][col].ch         = randomChar();
            grid_[s.headRow][col].brightness = 1.0;
        }
        ++s.headRow;
    }

    // When the tail of the stream has passed the bottom, restart.
    if (s.headRow - s.length > rows_) {
        s.active  = false;
        s.headRow = -1;
        s.length  = 3 + static_cast<int>(nextRand() % static_cast<uint32_t>(rows_ / 2 + 1));
        s.speed   = 1 + static_cast<int>(nextRand() % 2);
        s.delay   = 2 + static_cast<int>(nextRand() % static_cast<uint32_t>(rows_));
    }
}

char MatrixAnimator::randomChar()
{
    const char* chars = nullptr;
    size_t      len   = 0;

    switch (charSet_) {
        case BINARY_CHARS:
            chars = BINARY_CHARSET;
            len   = sizeof(BINARY_CHARSET) - 1;
            break;
        case HEX_CHARS:
            chars = HEX_CHARSET;
            len   = sizeof(HEX_CHARSET) - 1;
            break;
        case CUSTOM_CHARS:
            chars = customChars_.c_str();
            len   = customChars_.size();
            break;
        case MATRIX_CHARS:
        default:
            chars = MATRIX_CHARSET;
            len   = sizeof(MATRIX_CHARSET) - 1;
            break;
    }

    return chars[nextRand() % static_cast<uint32_t>(len)];
}

// Linear-congruential generator (Knuth's constants, 32-bit).
uint32_t MatrixAnimator::nextRand()
{
    rngState_ = rngState_ * 1664525u + 1013904223u;
    return rngState_;
}
