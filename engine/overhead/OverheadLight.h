#ifndef OVERHEAD_LIGHT_H
#define OVERHEAD_LIGHT_H

#include <string>
#include <vector>

// OverheadLight renders a multi-row ceiling-panel style ASCII display driven
// by neural-network output values.  Each output value maps to one light cell.
// The panel is arranged as a grid with a configurable number of columns.
// A cell is ON when its value exceeds the threshold (default 0.0).
class OverheadLight {
public:
    // cols      : number of light cells per row in the panel
    // threshold : activation threshold; cells above this value are lit
    explicit OverheadLight(int cols = 4, double threshold = 0.0);

    // Render the ceiling panel to stdout.
    // label   : optional title printed above the panel
    // outputs : neural-network output activations (one value per cell)
    void display(const std::string& label, const std::vector<double>& outputs) const;

private:
    int    cols_;
    double threshold_;

    void printRowBorder(int count) const;
    void printLightRow(const std::vector<double>& outputs, int start, int count) const;
    void printValueRow(const std::vector<double>& outputs, int start, int count) const;
};

#endif // OVERHEAD_LIGHT_H
