#include <iostream>
#include <vector>
#include <string>

#include "../../engine/neural/NeuralNetwork.h"
#include "../../engine/overhead/OverheadLight.h"
#include "../../engine/engineering/EngineeringModule.h"

int main()
{
    std::cout << "=== Overhead Light + Engineering Module Demo ===" << std::endl;
    std::cout << std::endl;

    // Network: 4 engineering inputs -> 6 hidden -> 6 hidden -> 4 outputs
    // Four output LEDs map to four overhead lights on the panel.
    const std::vector<int> layers = {4, 6, 6, 4};
    const unsigned int seed = 42;
    NeuralNetwork net(layers, seed);

    // Overhead panel: 4 cells per row, threshold 0.0
    OverheadLight panel(4, 0.0);

    // Engineering module (default operating ranges)
    EngineeringModule eng;

    // Sample engineering readings from four different sensor stations
    std::vector<EngineeringReading> stations = {
        {120.0,  5.5,  25.0, 101.3, "Station-A"},
        {230.0, 15.0,  80.0, 250.0, "Station-B"},
        {  0.0,  0.0, -20.0,   0.5, "Station-C"},
        {240.0, 29.5, 145.0, 495.0, "Station-D"},
    };

    for (size_t i = 0; i < stations.size(); ++i) {
        const EngineeringReading& station = stations[i];
        std::vector<double> normalised = eng.normalise(station);

        // Print engineering diagnostics
        eng.printDiagnostics(station, normalised);
        std::cout << std::endl;

        // Run the neural network
        std::vector<double> output = net.forward(normalised);

        // Render the overhead light panel
        std::string panelLabel = "Overhead panel (" + station.label + "):";
        panel.display(panelLabel, output);
        std::cout << std::endl;
    }

    return 0;
}
