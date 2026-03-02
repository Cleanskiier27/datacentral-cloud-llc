#include "LEDBoard.h"

#include <iostream>
#include <iomanip>

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
