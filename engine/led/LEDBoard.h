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

private:
    double threshold_;
};

#endif // LED_BOARD_H
