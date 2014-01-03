// Copyright (C) 2012 by wubenqi
// Distributable under the terms of either the Apache License (Version 2.0) or 
// the GNU Lesser General Public License, as specified in the COPYING file.
//
// By: wubenqi<wubenqi@gmail.com>
//

#ifndef SCRIPTENGINE_BASE_LUABIND_PB_H_
#define SCRIPTENGINE_BASE_LUABIND_PB_H_

#include "luabind/scope.hpp"

luabind::scope LuabindPBRegister_IOBuffer();
luabind::scope LuabindPBRegister_MessageLite();
luabind::scope LuabindPBRegister_Message();
//luabind::scope Register_SerializeToIOBuffer();

#endif
