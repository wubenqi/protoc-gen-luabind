// Copyright (C) 2012 by wubenqi
// Distributable under the terms of either the Apache License (Version 2.0) or 
// the GNU Lesser General Public License, as specified in the COPYING file.
//
// By: wubenqi<wubenqi@gmail.com>
//

#ifndef SCRIPTENGINE_LUABIND_REGISTER_PB_H_
#define SCRIPTENGINE_LUABIND_REGISTER_PB_H_

namespace luabind {
	struct scope;
}

typedef luabind::scope (*LuabindRegister_Func)();



#endif
