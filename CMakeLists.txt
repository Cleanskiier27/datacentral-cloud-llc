cmake_minimum_required(VERSION 3.10)
project(NeuralNetworkDemo CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- Neural network library ---
add_library(neural
    engine/neural/NeuralNetwork.cpp
)
target_include_directories(neural PUBLIC engine/neural)

# --- LED board library ---
add_library(led
    engine/led/LEDBoard.cpp
)
target_include_directories(led PUBLIC engine/led)

# --- Demo executable ---
add_executable(neural_demo
    examples/neural_demo/main.cpp
)
target_link_libraries(neural_demo PRIVATE neural)

# --- Overhead light library ---
add_library(overhead
    engine/overhead/OverheadLight.cpp
)
target_include_directories(overhead PUBLIC engine/overhead)

# --- Engineering module library ---
add_library(engineering
    engine/engineering/EngineeringModule.cpp
)
target_include_directories(engineering PUBLIC engine/engineering)

# --- Artemis demo executable ---
add_executable(artemis_demo
    examples/artemis_demo/main.cpp
)
target_link_libraries(artemis_demo PRIVATE neural led)

# --- Overhead demo executable ---
add_executable(overhead_demo
    examples/overhead_demo/main.cpp
)
target_link_libraries(overhead_demo PRIVATE neural overhead engineering)
