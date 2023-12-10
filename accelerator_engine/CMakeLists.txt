cmake_minimum_required (VERSION 3.8)

project ("engine")

include (GenerateExportHeader)

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET engine PROPERTY CXX_STANDARD 20)
endif()

include_directories(
    "C:\Users\Fekete Tamas\AppData\Local\Programs\Python\Python310\Include"
    "D:\Projects\Causality\causalityEnv3.10\lib\site-packages\pybind11\include"
)

add_library(engine SHARED "engine.cpp")
set_target_properties(engine PROPERTIES SUFFIX ".pyd")
GENERATE_EXPORT_HEADER(engine
    BASE_NAME engine
    EXPORT_MACRO_NAME engine_EXPORT
    EXPORT_FILE_NAME engine_Export.h
    STATIC_DEFINE engine_BUILT_AS_STATIC
)

