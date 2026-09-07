#include "NeuralNetwork.h"

#include <cmath>
#include <stdexcept>

NeuralNetwork::NeuralNetwork(const std::vector<int>& layerSizes, unsigned int seed)
    : seed_(seed), layerSizes_(layerSizes)
{
    if (layerSizes.size() < 2) {
        throw std::invalid_argument("Network must have at least 2 layers (input and output).");
    }
    initialize();
}

void NeuralNetwork::initialize()
{
    // Use a simple linear congruential generator seeded with seed_ so that
    // initialization is fully reproducible given the same seed.
    // LCG parameters from Numerical Recipes.
    uint64_t state = seed_;
    auto nextDouble = [&]() -> double {
        state = state * 6364136223846793005ULL + 1442695040888963407ULL;
        // Map to (0, 1)
        return static_cast<double>((state >> 11) & 0x1FFFFFFFFFFFFFULL) /
               static_cast<double>(0x1FFFFFFFFFFFFFULL);
    };

    int numLayers = static_cast<int>(layerSizes_.size());
    weights_.resize(numLayers - 1);
    biases_.resize(numLayers - 1);

    for (int l = 0; l < numLayers - 1; ++l) {
        int fanIn  = layerSizes_[l];
        int fanOut = layerSizes_[l + 1];

        // He initialization: scale = sqrt(2 / fanIn), suitable for ReLU networks
        double scale = std::sqrt(2.0 / fanIn);

        weights_[l].resize(fanOut * fanIn);
        for (double& w : weights_[l]) {
            // Map uniform sample to [-1, 1] then scale
            w = (nextDouble() * 2.0 - 1.0) * scale;
        }

        biases_[l].resize(fanOut, 0.0);
    }
}

std::vector<double> NeuralNetwork::relu(const std::vector<double>& v)
{
    std::vector<double> out(v.size());
    for (size_t i = 0; i < v.size(); ++i) {
        out[i] = v[i] > 0.0 ? v[i] : 0.0;
    }
    return out;
}

std::vector<double> NeuralNetwork::forward(const std::vector<double>& input) const
{
    if (static_cast<int>(input.size()) != layerSizes_[0]) {
        throw std::invalid_argument("Input size does not match network input layer size.");
    }

    std::vector<double> activation = input;
    int numLayers = static_cast<int>(layerSizes_.size());

    for (int l = 0; l < numLayers - 1; ++l) {
        int fanIn  = layerSizes_[l];
        int fanOut = layerSizes_[l + 1];

        std::vector<double> next(fanOut);
        for (int i = 0; i < fanOut; ++i) {
            double sum = biases_[l][i];
            for (int j = 0; j < fanIn; ++j) {
                sum += weights_[l][i * fanIn + j] * activation[j];
            }
            next[i] = sum;
        }

        // Apply ReLU to all but the last layer
        if (l < numLayers - 2) {
            activation = relu(next);
        } else {
            activation = next;
        }
    }

    return activation;
}

unsigned int NeuralNetwork::getSeed() const
{
    return seed_;
}
