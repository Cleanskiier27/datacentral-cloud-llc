#include "LEDBoard.h"

#include <iostream>
#include <iomanip>
#include <stdexcept>

LEDBoard::LEDBoard(double threshold)
    : threshold_(threshold)
{}

void LEDBoard::display(const std::string& label, const std::vector<double>& outputs) const
{
    if (!label.empty()) {
        std::cout << label << std::endl;
    }

    // Top border
    std::cout << "+";
    for (size_t i = 0; i < outputs.size(); ++i) {
        std::cout << "----+";
    }
    std::cout << std::endl;

    // LED row: [**] = ON, [  ] = OFF
    std::cout << "|";
    for (size_t i = 0; i < outputs.size(); ++i) {
        bool on = outputs[i] > threshold_;
        std::cout << (on ? " ** |" : "    |");
    }
    std::cout << std::endl;

    // Bottom border
    std::cout << "+";
    for (size_t i = 0; i < outputs.size(); ++i) {
        std::cout << "----+";
    }
    std::cout << std::endl;

    // Value row
    std::cout << "|";
    for (size_t i = 0; i < outputs.size(); ++i) {
        std::cout << std::fixed << std::setprecision(2)
                  << std::setw(4) << outputs[i] << "|";
    }
    std::cout << std::endl;

    // Label row (LED index)
    std::cout << "|";
    for (size_t i = 0; i < outputs.size(); ++i) {
        std::string lbl = "L" + std::to_string(i);
        std::cout << std::setw(3) << lbl << " |";
    }
    std::cout << std::endl;

    // Final border
    std::cout << "+";
    for (size_t i = 0; i < outputs.size(); ++i) {
        std::cout << "----+";
    }
    std::cout << std::endl;
}

// ---------------------------------------------------------------------------
// 2-D matrix display helpers
// ---------------------------------------------------------------------------

void LEDBoard::displayMatrix(const std::string& label,
                             const std::vector<double>& brightness,
                             int rows, int cols) const
{
    if (rows < 1 || cols < 1) {
        throw std::invalid_argument("LEDBoard::displayMatrix: rows and cols must be >= 1");
    }
    if (static_cast<int>(brightness.size()) != rows * cols) {
        throw std::invalid_argument("LEDBoard::displayMatrix: brightness size must equal rows*cols");
    }

    if (!label.empty()) {
        std::cout << label << std::endl;
    }

    // Top border: each cell is 2 chars wide, separated by a single '+'.
    std::cout << '+';
    for (int c = 0; c < cols; ++c) {
        std::cout << "--+";
    }
    std::cout << '\n';

    for (int r = 0; r < rows; ++r) {
        std::cout << '|';
        for (int c = 0; c < cols; ++c) {
            double b = brightness[static_cast<size_t>(r * cols + c)];
            const char* cell;
            if      (b >= 0.75) cell = "##";
            else if (b >= 0.50) cell = "++";
            else if (b >= 0.25) cell = "..";
            else                cell = "  ";
            std::cout << cell << '|';
        }
        std::cout << '\n';

        // Row separator.
        std::cout << '+';
        for (int c = 0; c < cols; ++c) {
            std::cout << "--+";
        }
        std::cout << '\n';
    }
}

void LEDBoard::displayCharMatrix(const std::string& label,
                                 const std::string& chars,
                                 const std::vector<double>& brightness,
                                 int rows, int cols) const
{
    if (rows < 1 || cols < 1) {
        throw std::invalid_argument("LEDBoard::displayCharMatrix: rows and cols must be >= 1");
    }
    if (static_cast<int>(brightness.size()) != rows * cols) {
        throw std::invalid_argument("LEDBoard::displayCharMatrix: brightness size must equal rows*cols");
    }
    if (static_cast<int>(chars.size()) < rows * cols) {
        throw std::invalid_argument("LEDBoard::displayCharMatrix: chars size must be >= rows*cols");
    }

    if (!label.empty()) {
        std::cout << label << std::endl;
    }

    // Dim threshold – cells below this fraction of threshold_ appear as spaces.
    const double dimThreshold = threshold_ * 0.25;

    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < cols; ++c) {
            size_t idx = static_cast<size_t>(r * cols + c);
            if (brightness[idx] <= dimThreshold) {
                std::cout << ' ';
            } else {
                std::cout << chars[idx];
            }
        }
        std::cout << '\n';
    }
}
