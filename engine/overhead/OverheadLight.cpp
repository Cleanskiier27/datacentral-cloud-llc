#include "OverheadLight.h"

#include <iostream>
#include <iomanip>
#include <algorithm>

OverheadLight::OverheadLight(int cols, double threshold)
    : cols_(cols > 0 ? cols : 1), threshold_(threshold)
{}

void OverheadLight::printRowBorder(int count) const
{
    std::cout << "+";
    for (int i = 0; i < count; ++i) {
        std::cout << "======+";
    }
    std::cout << std::endl;
}

void OverheadLight::printLightRow(const std::vector<double>& outputs,
                                  int start, int count) const
{
    // Top half of the bulb
    std::cout << "|";
    for (int i = start; i < start + count; ++i) {
        bool on = outputs[static_cast<size_t>(i)] > threshold_;
        std::cout << (on ? " /~~\\ |" : "      |");
    }
    std::cout << std::endl;

    // Bottom half of the bulb (value indicator)
    std::cout << "|";
    for (int i = start; i < start + count; ++i) {
        bool on = outputs[static_cast<size_t>(i)] > threshold_;
        std::cout << (on ? " \\**/ |" : "      |");
    }
    std::cout << std::endl;
}

void OverheadLight::printValueRow(const std::vector<double>& outputs,
                                  int start, int count) const
{
    std::cout << "|";
    for (int i = start; i < start + count; ++i) {
        std::cout << std::fixed << std::setprecision(2)
                  << std::setw(5) << outputs[static_cast<size_t>(i)] << " |";
    }
    std::cout << std::endl;
}

void OverheadLight::display(const std::string& label,
                             const std::vector<double>& outputs) const
{
    if (!label.empty()) {
        std::cout << label << std::endl;
    }

    int total = static_cast<int>(outputs.size());
    int start = 0;

    while (start < total) {
        int count = std::min(cols_, total - start);
        printRowBorder(count);
        printLightRow(outputs, start, count);
        printValueRow(outputs, start, count);
        printRowBorder(count);
        start += count;
    }
}
