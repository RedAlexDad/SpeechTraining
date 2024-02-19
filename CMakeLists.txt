cmake_minimum_required(VERSION 3.26)
project(SpeechTraining)

set(CMAKE_CXX_STANDARD 20)

# Путь к заголовочным файлам TensorFlow
include_directories(/usr/local/include)
# Путь к заголовочным файлам Eigen
include_directories(/usr/local/include/eigen)

add_executable(
        SpeechTraining
        main.cpp
#        driver.cpp
)

# Подключение к библиотекам SYCL
target_link_libraries(
        SpeechTraining PRIVATE
        /usr/local/lib/libtensorflow.so
)

# Добавление директорий для заголовочных файлов SYCL
target_include_directories(
        SpeechTraining PRIVATE
        ${OpenCL_INCLUDE_DIRS}
)