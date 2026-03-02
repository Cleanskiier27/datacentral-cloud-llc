#include <iostream>
#include <iomanip>
#include <vector>
#include <string>

#include "../../engine/neural/NeuralNetwork.h"
#include "../../engine/led/LEDBoard.h"

// Print a labeled vector of doubles to stdout.
static void printVector(const std::string& label, const std::vector<double>& v)
{
    std::cout << label << "[ ";
    for (size_t i = 0; i < v.size(); ++i) {
        std::cout << std::fixed << std::setprecision(6) << v[i];
        if (i + 1 < v.size()) {
            std::cout << ", ";
        }
    }
    std::cout << " ]" << std::endl;
}

int main()
{
    // Artemis network: 4 sensor inputs -> 8 hidden -> 8 hidden -> 3 outputs
    // Represents a mission-control style classifier with a fixed seed for
    // fully reproducible results across runs.
    const std::vector<int> artemisLayers = {4, 8, 8, 3};
    const unsigned int artemisSeed = 2024;

    std::cout << "=== Artemis Neural Network Demo ===" << std::endl;
    std::cout << "Architecture : 4 -> 8 -> 8 -> 3" << std::endl;
    std::cout << "Seed         : " << artemisSeed << std::endl;
    std::cout << std::endl;

    NeuralNetwork artemis(artemisLayers, artemisSeed);

    // LED board with one LED per output neuron (threshold = 0.0)
    LEDBoard board;

    // --- Sample inputs representing four sensor readings ---
    std::vector<std::vector<double>> inputs = {
        { 1.0,  0.0,  0.0,  0.0},
        { 0.0,  1.0, -1.0,  0.5},
        {-0.5,  0.3,  0.7, -0.2},
        { 0.8, -0.6,  0.4,  0.9},
    };

    std::cout << "--- Forward pass results ---" << std::endl;
    for (size_t i = 0; i < inputs.size(); ++i) {
        std::cout << "Input  " << i + 1 << ": ";
        printVector("", inputs[i]);

        std::vector<double> output = artemis.forward(inputs[i]);
        std::cout << "Output " << i + 1 << ": ";
        printVector("", output);

        // Show the output on the LED board
        std::string boardLabel = "LED board (pass " + std::to_string(i + 1) + "):";
        board.display(boardLabel, output);

        std::cout << std::endl;
    }

    // --- Reproducibility check ---
    std::cout << "--- Reproducibility check ---" << std::endl;
    NeuralNetwork artemis2(artemisLayers, artemisSeed);
    std::vector<double> ref    = artemis.forward(inputs[0]);
    std::vector<double> check  = artemis2.forward(inputs[0]);
    bool reproducible = (ref == check);
    std::cout << "Two Artemis networks with seed " << artemisSeed
              << " produce identical outputs: "
              << (reproducible ? "YES" : "NO") << std::endl;

    return 0;
}
