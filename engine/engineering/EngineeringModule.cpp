#include "EngineeringModule.h"

#include <iostream>
#include <iomanip>
#include <algorithm>
#include <stdexcept>

// ---------------------------------------------------------------------------
// Construction
// ---------------------------------------------------------------------------

EngineeringModule::EngineeringModule()
    : minV_(0.0),   maxV_(240.0)
    , minA_(0.0),   maxA_(30.0)
    , minC_(-40.0), maxC_(150.0)
    , minKpa_(0.0), maxKpa_(500.0)
{}

// ---------------------------------------------------------------------------
// Range setters
// ---------------------------------------------------------------------------

void EngineeringModule::setVoltageRange(double minV, double maxV)
{
    if (minV >= maxV) throw std::invalid_argument("voltage range: min must be < max");
    minV_ = minV; maxV_ = maxV;
}

void EngineeringModule::setCurrentRange(double minA, double maxA)
{
    if (minA >= maxA) throw std::invalid_argument("current range: min must be < max");
    minA_ = minA; maxA_ = maxA;
}

void EngineeringModule::setTemperatureRange(double minC, double maxC)
{
    if (minC >= maxC) throw std::invalid_argument("temperature range: min must be < max");
    minC_ = minC; maxC_ = maxC;
}

void EngineeringModule::setPressureRange(double minKpa, double maxKpa)
{
    if (minKpa >= maxKpa) throw std::invalid_argument("pressure range: min must be < max");
    minKpa_ = minKpa; maxKpa_ = maxKpa;
}

// ---------------------------------------------------------------------------
// Normalisation
// ---------------------------------------------------------------------------

double EngineeringModule::normaliseChannel(double x, double lo, double hi)
{
    // Clamp to physical range, then map [lo, hi] -> [-1, 1].
    double clamped = std::max(lo, std::min(hi, x));
    return 2.0 * (clamped - lo) / (hi - lo) - 1.0;
}

std::vector<double> EngineeringModule::normalise(const EngineeringReading& r) const
{
    return {
        normaliseChannel(r.voltage,     minV_,   maxV_),
        normaliseChannel(r.current,     minA_,   maxA_),
        normaliseChannel(r.temperature, minC_,   maxC_),
        normaliseChannel(r.pressure,    minKpa_, maxKpa_)
    };
}

// ---------------------------------------------------------------------------
// Diagnostics
// ---------------------------------------------------------------------------

void EngineeringModule::printDiagnostics(const EngineeringReading& r,
                                          const std::vector<double>& n) const
{
    std::cout << "+-----------------------------------------+" << std::endl;
    if (!r.label.empty()) {
        std::cout << "| Engineering Diagnostics: "
                  << std::left << std::setw(15) << r.label << "     |" << std::endl;
    } else {
        std::cout << "| Engineering Diagnostics                 |" << std::endl;
    }
    std::cout << "+-----------------------------------------+" << std::endl;
    std::cout << std::fixed << std::setprecision(3);
    std::cout << "| Voltage     : " << std::setw(8) << r.voltage
              << " V    -> " << std::setw(7) << n[0] << " |" << std::endl;
    std::cout << "| Current     : " << std::setw(8) << r.current
              << " A    -> " << std::setw(7) << n[1] << " |" << std::endl;
    std::cout << "| Temperature : " << std::setw(8) << r.temperature
              << " C    -> " << std::setw(7) << n[2] << " |" << std::endl;
    std::cout << "| Pressure    : " << std::setw(8) << r.pressure
              << " kPa  -> " << std::setw(7) << n[3] << " |" << std::endl;
    std::cout << "+-----------------------------------------+" << std::endl;
}
