#ifndef LED_BOARD_H
#define LED_BOARD_H

#include <string>
#include <vector>

// LEDBoard renders a row of LEDs driven by neural-network output values.
// Each element of the output vector maps to one LED.  An LED is considered
// ON when its value exceeds the threshold (default 0.0) and OFF otherwise.
class LEDBoard {
public:
    // Construct a board with an optional activation threshold.
    explicit LEDBoard(double threshold = 0.0);

    // Render the board to stdout.
    // label   : descriptive title printed above the board (may be empty)
    // outputs : neural-network output activations (one value per LED)
    void display(const std::string& label, const std::vector<double>& outputs) const;

    // ---------------------------------------------------------------------------
    // 2-D matrix display
    // ---------------------------------------------------------------------------

    // Render a 2D LED matrix (rows × cols) driven by a flat, row-major brightness
    // vector produced by MatrixAnimator::flatBrightness().
    // label      : descriptive title (may be empty)
    // brightness : row-major brightness values in [0.0, 1.0] (size == rows*cols)
    // rows, cols : grid dimensions
    // Each cell is drawn as one of four visual levels:
    //   brightness >= 0.75  ->  "##"  (maximum / head glyph)
    //   brightness >= 0.50  ->  "++"  (bright trail)
    //   brightness >= 0.25  ->  ".."  (dim trail)
    //   brightness <  0.25  ->  "  "  (off / background)
    void displayMatrix(const std::string& label,
                       const std::vector<double>& brightness,
                       int rows, int cols) const;

    // Render a 2D matrix where each cell carries an explicit character and a
    // brightness value.  `chars` and `brightness` are both row-major, size rows*cols.
    // The character is printed verbatim; brightness controls whether it shows at all
    // (cells below threshold_ * 0.25 are rendered as spaces).
    void displayCharMatrix(const std::string& label,
                           const std::string& chars,
                           const std::vector<double>& brightness,
                           int rows, int cols) const;

private:
    double threshold_;
};

#endif // LED_BOARD_H
