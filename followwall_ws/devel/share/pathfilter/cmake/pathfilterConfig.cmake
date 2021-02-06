# generated from catkin/cmake/template/pkgConfig.cmake.in

# append elements to a list and remove existing duplicates from the list
# copied from catkin/cmake/list_append_deduplicate.cmake to keep pkgConfig
# self contained
macro(_list_append_deduplicate listname)
  if(NOT "${ARGN}" STREQUAL "")
    if(${listname})
      list(REMOVE_ITEM ${listname} ${ARGN})
    endif()
    list(APPEND ${listname} ${ARGN})
  endif()
endmacro()

# append elements to a list if they are not already in the list
# copied from catkin/cmake/list_append_unique.cmake to keep pkgConfig
# self contained
macro(_list_append_unique listname)
  foreach(_item ${ARGN})
    list(FIND ${listname} ${_item} _index)
    if(_index EQUAL -1)
      list(APPEND ${listname} ${_item})
    endif()
  endforeach()
endmacro()

# pack a list of libraries with optional build configuration keywords
# copied from catkin/cmake/catkin_libraries.cmake to keep pkgConfig
# self contained
macro(_pack_libraries_with_build_configuration VAR)
  set(${VAR} "")
  set(_argn ${ARGN})
  list(LENGTH _argn _count)
  set(_index 0)
  while(${_index} LESS ${_count})
    list(GET _argn ${_index} lib)
    if("${lib}" MATCHES "^(debug|optimized|general)$")
      math(EXPR _index "${_index} + 1")
      if(${_index} EQUAL ${_count})
        message(FATAL_ERROR "_pack_libraries_with_build_configuration() the list of libraries '${ARGN}' ends with '${lib}' which is a build configuration keyword and must be followed by a library")
      endif()
      list(GET _argn ${_index} library)
      list(APPEND ${VAR} "${lib}${CATKIN_BUILD_CONFIGURATION_KEYWORD_SEPARATOR}${library}")
    else()
      list(APPEND ${VAR} "${lib}")
    endif()
    math(EXPR _index "${_index} + 1")
  endwhile()
endmacro()

# unpack a list of libraries with optional build configuration keyword prefixes
# copied from catkin/cmake/catkin_libraries.cmake to keep pkgConfig
# self contained
macro(_unpack_libraries_with_build_configuration VAR)
  set(${VAR} "")
  foreach(lib ${ARGN})
    string(REGEX REPLACE "^(debug|optimized|general)${CATKIN_BUILD_CONFIGURATION_KEYWORD_SEPARATOR}(.+)$" "\\1;\\2" lib "${lib}")
    list(APPEND ${VAR} "${lib}")
  endforeach()
endmacro()


if(pathfilter_CONFIG_INCLUDED)
  return()
endif()
set(pathfilter_CONFIG_INCLUDED TRUE)

# set variables for source/devel/install prefixes
if("TRUE" STREQUAL "TRUE")
  set(pathfilter_SOURCE_PREFIX /home/czp/followwall_ws/src/pathfilter)
  set(pathfilter_DEVEL_PREFIX /home/czp/followwall_ws/devel)
  set(pathfilter_INSTALL_PREFIX "")
  set(pathfilter_PREFIX ${pathfilter_DEVEL_PREFIX})
else()
  set(pathfilter_SOURCE_PREFIX "")
  set(pathfilter_DEVEL_PREFIX "")
  set(pathfilter_INSTALL_PREFIX /home/czp/followwall_ws/install)
  set(pathfilter_PREFIX ${pathfilter_INSTALL_PREFIX})
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "WARNING: package 'pathfilter' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  message("${_msg}")
endif()

# flag project as catkin-based to distinguish if a find_package()-ed project is a catkin project
set(pathfilter_FOUND_CATKIN_PROJECT TRUE)

if(NOT "/home/czp/followwall_ws/devel/include;/home/czp/followwall_ws/src/pathfilter/include " STREQUAL " ")
  set(pathfilter_INCLUDE_DIRS "")
  set(_include_dirs "/home/czp/followwall_ws/devel/include;/home/czp/followwall_ws/src/pathfilter/include")
  if(NOT " " STREQUAL " ")
    set(_report "Check the issue tracker '' and consider creating a ticket if the problem has not been reported yet.")
  elseif(NOT " " STREQUAL " ")
    set(_report "Check the website '' for information and consider reporting the problem.")
  else()
    set(_report "Report the problem to the maintainer 'czp <czp@todo.todo>' and request to fix the problem.")
  endif()
  foreach(idir ${_include_dirs})
    if(IS_ABSOLUTE ${idir} AND IS_DIRECTORY ${idir})
      set(include ${idir})
    elseif("${idir} " STREQUAL "include ")
      get_filename_component(include "${pathfilter_DIR}/../../../include" ABSOLUTE)
      if(NOT IS_DIRECTORY ${include})
        message(FATAL_ERROR "Project 'pathfilter' specifies '${idir}' as an include dir, which is not found.  It does not exist in '${include}'.  ${_report}")
      endif()
    else()
      message(FATAL_ERROR "Project 'pathfilter' specifies '${idir}' as an include dir, which is not found.  It does neither exist as an absolute directory nor in '/home/czp/followwall_ws/src/pathfilter/${idir}'.  ${_report}")
    endif()
    _list_append_unique(pathfilter_INCLUDE_DIRS ${include})
  endforeach()
endif()

set(libraries "pathfilter")
foreach(library ${libraries})
  # keep build configuration keywords, target names and absolute libraries as-is
  if("${library}" MATCHES "^(debug|optimized|general)$")
    list(APPEND pathfilter_LIBRARIES ${library})
  elseif(${library} MATCHES "^-l")
    list(APPEND pathfilter_LIBRARIES ${library})
  elseif(${library} MATCHES "^-")
    # This is a linker flag/option (like -pthread)
    # There's no standard variable for these, so create an interface library to hold it
    if(NOT pathfilter_NUM_DUMMY_TARGETS)
      set(pathfilter_NUM_DUMMY_TARGETS 0)
    endif()
    # Make sure the target name is unique
    set(interface_target_name "catkin::pathfilter::wrapped-linker-option${pathfilter_NUM_DUMMY_TARGETS}")
    while(TARGET "${interface_target_name}")
      math(EXPR pathfilter_NUM_DUMMY_TARGETS "${pathfilter_NUM_DUMMY_TARGETS}+1")
      set(interface_target_name "catkin::pathfilter::wrapped-linker-option${pathfilter_NUM_DUMMY_TARGETS}")
    endwhile()
    add_library("${interface_target_name}" INTERFACE IMPORTED)
    if("${CMAKE_VERSION}" VERSION_LESS "3.13.0")
      set_property(
        TARGET
        "${interface_target_name}"
        APPEND PROPERTY
        INTERFACE_LINK_LIBRARIES "${library}")
    else()
      target_link_options("${interface_target_name}" INTERFACE "${library}")
    endif()
    list(APPEND pathfilter_LIBRARIES "${interface_target_name}")
  elseif(TARGET ${library})
    list(APPEND pathfilter_LIBRARIES ${library})
  elseif(IS_ABSOLUTE ${library})
    list(APPEND pathfilter_LIBRARIES ${library})
  else()
    set(lib_path "")
    set(lib "${library}-NOTFOUND")
    # since the path where the library is found is returned we have to iterate over the paths manually
    foreach(path /home/czp/followwall_ws/devel/lib;/home/czp/lingao_ws/devel/lib;/home/czp/xsens_ws/devel/lib;/home/czp/turtlebot_ws/devel/lib;/home/czp/realsense_ros/devel/lib;/opt/ros/kinetic/lib)
      find_library(lib ${library}
        PATHS ${path}
        NO_DEFAULT_PATH NO_CMAKE_FIND_ROOT_PATH)
      if(lib)
        set(lib_path ${path})
        break()
      endif()
    endforeach()
    if(lib)
      _list_append_unique(pathfilter_LIBRARY_DIRS ${lib_path})
      list(APPEND pathfilter_LIBRARIES ${lib})
    else()
      # as a fall back for non-catkin libraries try to search globally
      find_library(lib ${library})
      if(NOT lib)
        message(FATAL_ERROR "Project '${PROJECT_NAME}' tried to find library '${library}'.  The library is neither a target nor built/installed properly.  Did you compile project 'pathfilter'?  Did you find_package() it before the subdirectory containing its code is included?")
      endif()
      list(APPEND pathfilter_LIBRARIES ${lib})
    endif()
  endif()
endforeach()

set(pathfilter_EXPORTED_TARGETS "pathfilter_generate_messages_cpp;pathfilter_generate_messages_eus;pathfilter_generate_messages_lisp;pathfilter_generate_messages_nodejs;pathfilter_generate_messages_py")
# create dummy targets for exported code generation targets to make life of users easier
foreach(t ${pathfilter_EXPORTED_TARGETS})
  if(NOT TARGET ${t})
    add_custom_target(${t})
  endif()
endforeach()

set(depends "message_runtime;geometry_msgs;nav_msgs;roscpp;rospy;sensor_msgs;std_msgs;tf")
foreach(depend ${depends})
  string(REPLACE " " ";" depend_list ${depend})
  # the package name of the dependency must be kept in a unique variable so that it is not overwritten in recursive calls
  list(GET depend_list 0 pathfilter_dep)
  list(LENGTH depend_list count)
  if(${count} EQUAL 1)
    # simple dependencies must only be find_package()-ed once
    if(NOT ${pathfilter_dep}_FOUND)
      find_package(${pathfilter_dep} REQUIRED NO_MODULE)
    endif()
  else()
    # dependencies with components must be find_package()-ed again
    list(REMOVE_AT depend_list 0)
    find_package(${pathfilter_dep} REQUIRED NO_MODULE ${depend_list})
  endif()
  _list_append_unique(pathfilter_INCLUDE_DIRS ${${pathfilter_dep}_INCLUDE_DIRS})

  # merge build configuration keywords with library names to correctly deduplicate
  _pack_libraries_with_build_configuration(pathfilter_LIBRARIES ${pathfilter_LIBRARIES})
  _pack_libraries_with_build_configuration(_libraries ${${pathfilter_dep}_LIBRARIES})
  _list_append_deduplicate(pathfilter_LIBRARIES ${_libraries})
  # undo build configuration keyword merging after deduplication
  _unpack_libraries_with_build_configuration(pathfilter_LIBRARIES ${pathfilter_LIBRARIES})

  _list_append_unique(pathfilter_LIBRARY_DIRS ${${pathfilter_dep}_LIBRARY_DIRS})
  list(APPEND pathfilter_EXPORTED_TARGETS ${${pathfilter_dep}_EXPORTED_TARGETS})
endforeach()

set(pkg_cfg_extras "pathfilter-msg-extras.cmake")
foreach(extra ${pkg_cfg_extras})
  if(NOT IS_ABSOLUTE ${extra})
    set(extra ${pathfilter_DIR}/${extra})
  endif()
  include(${extra})
endforeach()
