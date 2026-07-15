#include <iostream>
#include <iomanip>
#include <vector>

#include "../../engine/neural/NeuralNetwork.h"

// Print a vector of doubles to stdout.
static void printOutput(const std::vector<double>& v)
{
    std::cout << "[ ";
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
    // Network architecture: 3 inputs -> 4 hidden neurons -> 2 outputs
    std::vector<int> layers = {3, 4, 2};

    // Sample input used for all demonstrations
    std::vector<double> input = {0.5, -0.3, 0.8};

    std::cout << "=== Neural Network Reproducibility Demo ===" << std::endl;
    std::cout << "Architecture: 3 -> 4 -> 2" << std::endl;
    std::cout << "Input: ";
    printOutput(input);
    std::cout << std::endl;

    // --- Demonstration 1: Same seed produces identical results ---
    std::cout << "--- Demonstration 1: Two networks with seed 42 ---" << std::endl;

    NeuralNetwork net1(layers, 42);
    NeuralNetwork net2(layers, 42);

    std::vector<double> out1 = net1.forward(input);
    std::vector<double> out2 = net2.forward(input);

    std::cout << "Network 1 (seed 42) output: ";
    printOutput(out1);
    std::cout << "Network 2 (seed 42) output: ";
    printOutput(out2);

    bool identical = (out1 == out2);
    std::cout << "Outputs identical: " << (identical ? "YES" : "NO") << std::endl;
    std::cout << std::endl;

    // --- Demonstration 2: Different seed produces different results ---
    std::cout << "--- Demonstration 2: Network with seed 123 ---" << std::endl;

    NeuralNetwork net3(layers, 123);
    std::vector<double> out3 = net3.forward(input);

    std::cout << "Network 3 (seed 123) output: ";
    printOutput(out3);

    bool different = (out1 != out3);
    std::cout << "Output differs from seed-42 network: " << (different ? "YES" : "NO") << std::endl;
    std::cout << std::endl;

    // --- Summary ---
    std::cout << "=== Summary ===" << std::endl;
    std::cout << "Seed-based initialization ensures that networks with the same seed" << std::endl;
    std::cout << "always produce identical weights and therefore identical outputs," << std::endl;
    std::cout << "while different seeds yield different networks." << std::endl;

    return 0;
}
