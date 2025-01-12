# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/shc/volumetric_drilling

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/shc/volumetric_drilling/build

# Include any dependencies generated for this target.
include CMakeFiles/camera_projection_override.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/camera_projection_override.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/camera_projection_override.dir/flags.make

CMakeFiles/camera_projection_override.dir/plugin/camera_projection_override/projection_override.cpp.o: CMakeFiles/camera_projection_override.dir/flags.make
CMakeFiles/camera_projection_override.dir/plugin/camera_projection_override/projection_override.cpp.o: ../plugin/camera_projection_override/projection_override.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/shc/volumetric_drilling/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/camera_projection_override.dir/plugin/camera_projection_override/projection_override.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/camera_projection_override.dir/plugin/camera_projection_override/projection_override.cpp.o -c /home/shc/volumetric_drilling/plugin/camera_projection_override/projection_override.cpp

CMakeFiles/camera_projection_override.dir/plugin/camera_projection_override/projection_override.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/camera_projection_override.dir/plugin/camera_projection_override/projection_override.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/shc/volumetric_drilling/plugin/camera_projection_override/projection_override.cpp > CMakeFiles/camera_projection_override.dir/plugin/camera_projection_override/projection_override.cpp.i

CMakeFiles/camera_projection_override.dir/plugin/camera_projection_override/projection_override.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/camera_projection_override.dir/plugin/camera_projection_override/projection_override.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/shc/volumetric_drilling/plugin/camera_projection_override/projection_override.cpp -o CMakeFiles/camera_projection_override.dir/plugin/camera_projection_override/projection_override.cpp.s

# Object files for target camera_projection_override
camera_projection_override_OBJECTS = \
"CMakeFiles/camera_projection_override.dir/plugin/camera_projection_override/projection_override.cpp.o"

# External object files for target camera_projection_override
camera_projection_override_EXTERNAL_OBJECTS =

libcamera_projection_override.so: CMakeFiles/camera_projection_override.dir/plugin/camera_projection_override/projection_override.cpp.o
libcamera_projection_override.so: CMakeFiles/camera_projection_override.dir/build.make
libcamera_projection_override.so: /home/shc/ambf/build/libambf_framework.a
libcamera_projection_override.so: /home/shc/ambf/build/libchai3d.a
libcamera_projection_override.so: /home/shc/ambf/build/libbullet.a
libcamera_projection_override.so: /home/shc/ambf/build/external/GLFW/libglfw.a
libcamera_projection_override.so: /usr/lib/x86_64-linux-gnu/libGL.so
libcamera_projection_override.so: /usr/lib/x86_64-linux-gnu/libGLU.so
libcamera_projection_override.so: /usr/lib/x86_64-linux-gnu/libGL.so
libcamera_projection_override.so: /usr/lib/x86_64-linux-gnu/libGLU.so
libcamera_projection_override.so: /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.71.0
libcamera_projection_override.so: CMakeFiles/camera_projection_override.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/shc/volumetric_drilling/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared library libcamera_projection_override.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/camera_projection_override.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/camera_projection_override.dir/build: libcamera_projection_override.so

.PHONY : CMakeFiles/camera_projection_override.dir/build

CMakeFiles/camera_projection_override.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/camera_projection_override.dir/cmake_clean.cmake
.PHONY : CMakeFiles/camera_projection_override.dir/clean

CMakeFiles/camera_projection_override.dir/depend:
	cd /home/shc/volumetric_drilling/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/shc/volumetric_drilling /home/shc/volumetric_drilling /home/shc/volumetric_drilling/build /home/shc/volumetric_drilling/build /home/shc/volumetric_drilling/build/CMakeFiles/camera_projection_override.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/camera_projection_override.dir/depend

