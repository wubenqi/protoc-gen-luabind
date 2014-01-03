SET(SRC_LIST base_luabind_pb.cc
		base_pb_luabind.cc
		luabind_engine_register.cc
		luabind_register_manager.cc
		lua_util.cc
		script_engine.cc)

SET(LIBRARY_OUTPUT_PATH ${TF_CURRENT_BINARY_PATH_LIB})

ADD_LIBRARY(scriptengine STATIC ${SRC_LIST})
	  