// Copyright (C) 2012 by wubenqi
// Distributable under the terms of either the Apache License (Version 2.0) or 
// the GNU Lesser General Public License, as specified in the COPYING file.
//
// By: wubenqi<wubenqi@gmail.com>
//

#ifndef SCRIPTENGINE_LUABIND_REGISTER_MANAGER_H_
#define SCRIPTENGINE_LUABIND_REGISTER_MANAGER_H_

#include <vector>

#include "scriptengine/singleton.h"
#include "scriptengine/luabind_register_func.h"

class LuabindRegisterManager : public base2::Singleton<LuabindRegisterManager> {
public:
	void RegisterLuabindMessage(LuabindRegister_Func func) {
		registers_.push_back(func);
	}

	std::vector<LuabindRegister_Func>& MutableRegisters() {
		return registers_;
	}

private:
	friend class base2::Singleton<LuabindRegisterManager>;

	~LuabindRegisterManager() {
	}

	LuabindRegisterManager();

	std::vector<LuabindRegister_Func> registers_;
};


#endif // SCRIPTENGINE_LUABIND_PB_REGISTER_MANAGER_H_
