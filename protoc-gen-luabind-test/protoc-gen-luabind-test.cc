// Copyright (C) 2012 by wubenqi
// Distributable under the terms of either the Apache License (Version 2.0) or 
// the GNU Lesser General Public License, as specified in the COPYING file.
//
// By: wubenqi<wubenqi@gmail.com>
//

#include <iostream>

#include "scriptengine/script_engine.h"
#include "scriptengine/luabind_register_manager.h"

#include "luabind_pb_test.pb.h"

void LuabindPB_luabind_pb_test_RegisterAll();

int main(int argc, char **argv) {
  if (argc!=2) {
    std::cerr << "Useage: \n\t" << argv[0] << " luafile" << std::endl;
    return -1;
  }

  LuabindPB_luabind_pb_test_RegisterAll();

  ScriptEngine script_;
  script_.Initialize();
  script_.RegisterAll();

  script_.Load(argv[1]);
  script_.CallFunction("DoMain");

  return 0;
}