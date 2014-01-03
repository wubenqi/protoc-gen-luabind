// Copyright (C) 2012 by wubenqi
// Distributable under the terms of either the Apache License (Version 2.0) or 
// the GNU Lesser General Public License, as specified in the COPYING file.
//
// By: wubenqi<wubenqi@gmail.com>
//

#include "scriptengine/luabind_register_manager.h"

#include "scriptengine/base_luabind_pb.h"

LuabindRegisterManager::LuabindRegisterManager() {
	registers_.push_back(&LuabindPBRegister_IOBuffer);
	registers_.push_back(&LuabindPBRegister_MessageLite);
	registers_.push_back(&LuabindPBRegister_Message);
}
