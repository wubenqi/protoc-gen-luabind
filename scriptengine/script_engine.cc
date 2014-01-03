// Copyright (C) 2012 by wubenqi
// Distributable under the terms of either the Apache License (Version 2.0) or 
// the GNU Lesser General Public License, as specified in the COPYING file.
//
// By: wubenqi<wubenqi@gmail.com>
//

#include "scriptengine/script_engine.h"

#include <assert.h>
#include <list>

#include <boost/filesystem/path.hpp>
#include <boost/filesystem/operations.hpp>

#include <luabind/iterator_policy.hpp>

#include "scriptengine/luabind_register_manager.h"

void ScriptEngine::Initialize() {
	// 确保只会初始化一次
	if (!lua_state_) {
		lua_state_ = lua_open(); // 创建Lua状态
		if (!lua_state_) {
			std::cerr << "ScriptEngine::Init() lua_open failed!";
			return;
		}
		luaL_openlibs(lua_state_); // 为该Lua状态打开所有Lua库
		luabind::open(lua_state_); // 为该Lua状态打开luabind库
		//lua_interface_.Init(lua_state_);
	}
}

ScriptEngine::~ScriptEngine() {
	if (lua_state_) {
		lua_close(lua_state_);
		lua_state_ = NULL;
	}
}

void ScriptEngine::Refresh() {
	if (lua_state_) {
		lua_close(lua_state_);
		lua_state_ = NULL;
	}
	
	Initialize();
}

void ScriptEngine::Load(const std::string& lua_file) {
	assert(lua_state_ != NULL);

	if(boost::filesystem::exists(lua_file)) {
		if (luaL_dofile(lua_state_, lua_file.c_str())) {
			std::cerr << "load " << lua_file << " error: " << lua_tostring(lua_state_, -1);
		}
	}
}

void ScriptEngine::RegisterAll() {
	//luabind::module (lua_state_)
	//	[
	//		Register_IOBuffer(),
	//		Register_MessageLite(),
	//		Register_Message(),
	//		Register_ETest(),
	//		Register_MTest(),
	//		Register_MTestList()
	//	];

	// std::list<luabind::scope> registers;
	
	luabind::module_ module(lua_state_, 0);
	module.register_begin();

	std::vector<LuabindRegister_Func>& funcs = LuabindRegisterManager::GetInstance()->MutableRegisters();
	for(size_t i=0; i<funcs.size(); ++i) {
   luabind::scope s = funcs[i]();
		module.register_one(s);		
	}

	module.register_end();


/*	
	[
		funcs[0](),
		funcs[1](),
		funcs[2](),
		funcs[3](),
		funcs[4](),
		funcs[5]()
	];
*/
}

