#ifndef ENGINEERING_MODULE_H
#define ENGINEERING_MODULE_H

#include <string>
#include <vector>

// EngineeringReading holds one set of raw engineering measurements.
struct EngineeringReading {
    double voltage;      // Volts
    double current;      // Amperes
    double temperature;  // Degrees Celsius
    double pressure;     // kPa (kilopascals)

    // Human-readable label for this reading (e.g. "sensor-A")
    std::string label;
};

// EngineeringModule normalises raw engineering measurements into the [-1, 1]
// range expected by the neural network and optionally prints a diagnostics
// summary.  It understands the physical meaning of each channel and applies
// per-channel clamping before normalisation so that sensor noise and
// out-of-range hardware faults don't saturate the network inputs.
//
// Default operating ranges (adjustable via setRanges):
//   voltage     :   0 V  – 240 V
//   current     :   0 A  –  30 A
//   temperature : -40 °C – 150 °C
//   pressure    :   0 kPa – 500 kPa
class EngineeringModule {
public:
    EngineeringModule();

    // Override the default operating ranges.
    void setVoltageRange(double minV, double maxV);
    void setCurrentRange(double minA, double maxA);
    void setTemperatureRange(double minC, double maxC);
    void setPressureRange(double minKpa, double maxKpa);

    // Normalise a reading to a 4-element vector in [-1, 1]:
    //   [0] voltage, [1] current, [2] temperature, [3] pressure
    std::vector<double> normalise(const EngineeringReading& reading) const;

    // Print a formatted diagnostics panel to stdout.
    void printDiagnostics(const EngineeringReading& reading,
                          const std::vector<double>& normalised) const;

private:
    double minV_, maxV_;
    double minA_, maxA_;
    double minC_, maxC_;
    double minKpa_, maxKpa_;

    // Clamp x to [lo, hi] then map linearly to [-1, 1].
    static double normaliseChannel(double x, double lo, double hi);
};

#endif // ENGINEERING_MODULE_H
