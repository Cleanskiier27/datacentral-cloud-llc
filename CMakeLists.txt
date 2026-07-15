cmake_minimum_required(VERSION 3.10)
project(NeuralNetworkDemo CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- Neural network library ---
add_library(neural
    engine/neural/NeuralNetwork.cpp
)
target_include_directories(neural PUBLIC engine/neural)

# --- LED board library (includes MatrixAnimator) ---
add_library(led
    engine/led/LEDBoard.cpp
    engine/led/MatrixAnimator.cpp
)
target_include_directories(led PUBLIC engine/led)

# --- Demo executable ---
add_executable(neural_demo
    examples/neural_demo/main.cpp
)
target_link_libraries(neural_demo PRIVATE neural)

# --- Artemis demo executable ---
add_executable(artemis_demo
    examples/artemis_demo/main.cpp
)
target_link_libraries(artemis_demo PRIVATE neural led)

# --- Matrix LED board animation demo ---
add_executable(matrix_demo
    examples/matrix_demo/main.cpp
)
target_link_libraries(matrix_demo PRIVATE led)
