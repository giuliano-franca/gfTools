project(gfToolsMayaMainPlugin)

configure_file("mainPlugin.cpp.in"
    "${CMAKE_CURRENT_BINARY_DIR}/mainPlugin.cpp" @ONLY)

set(SOURCE_FILES
    "${CMAKE_CURRENT_BINARY_DIR}/mainPlugin.cpp")

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} PRIVATE Maya::Maya)
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} Maya::Maya)
target_compile_options(${PROJECT_NAME} PRIVATE ${COMPILE_FLAGS})
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "gfTools")
if(BUILD_TOOLS)
    target_compile_definitions(${PROJECT_NAME} PRIVATE ADD_SHELF_AND_MENU=1)
endif()

MAYA_PLUGIN(${PROJECT_NAME})

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    install(TARGETS ${PROJECT_NAME}
        ${MAYA_TARGET_TYPE} DESTINATION "plugin/maya/${MAYA_VERSION}")
else()
    install(TARGETS ${PROJECT_NAME}
        ${MAYA_TARGET_TYPE} DESTINATION "plugin/maya/${MAYA_VERSION}")
endif()