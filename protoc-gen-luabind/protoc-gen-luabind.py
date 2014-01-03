#!/usr/bin/env python
# -*- encoding:utf8 -*-
# protoc-gen-luabind
#
# Copyright (C) 2013, https://github.com/wubenqi. All rights reserved
#
# Distributable under the terms of either the Apache License (Version 2.0) or 
# the GNU Lesser General Public License, as specified in the COPYING file.
#
# Author: wubenqi<wubenqi@gmail.com>, 2012-08-03
#
# 参考 protoc-gen-lua, https://code.google.com/p/protoc-gen-lua/
#

import sys
import os.path as path
from cStringIO import StringIO

import plugin_pb2
import google.protobuf.descriptor_pb2 as descriptor_pb2

_packages = {}
_files = {}
_message = {}

FDP = plugin_pb2.descriptor_pb2.FieldDescriptorProto

if sys.platform == "win32":
    import msvcrt, os
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

class CppType:
    CPPTYPE_INT32       = 1
    CPPTYPE_INT64       = 2
    CPPTYPE_UINT32      = 3
    CPPTYPE_UINT64      = 4
    CPPTYPE_DOUBLE      = 5
    CPPTYPE_FLOAT       = 6
    CPPTYPE_BOOL        = 7
    CPPTYPE_ENUM        = 8
    CPPTYPE_STRING      = 9
    CPPTYPE_MESSAGE     = 10

CPP_TYPE ={
    FDP.TYPE_DOUBLE         : CppType.CPPTYPE_DOUBLE,
    FDP.TYPE_FLOAT          : CppType.CPPTYPE_FLOAT,
    FDP.TYPE_INT64          : CppType.CPPTYPE_INT64,
    FDP.TYPE_UINT64         : CppType.CPPTYPE_UINT64,
    FDP.TYPE_INT32          : CppType.CPPTYPE_INT32,
    FDP.TYPE_FIXED64        : CppType.CPPTYPE_UINT64,
    FDP.TYPE_FIXED32        : CppType.CPPTYPE_UINT32,
    FDP.TYPE_BOOL           : CppType.CPPTYPE_BOOL,
    FDP.TYPE_STRING         : CppType.CPPTYPE_STRING,
    FDP.TYPE_MESSAGE        : CppType.CPPTYPE_MESSAGE,
    FDP.TYPE_BYTES          : CppType.CPPTYPE_STRING,
    FDP.TYPE_UINT32         : CppType.CPPTYPE_UINT32,
    FDP.TYPE_ENUM           : CppType.CPPTYPE_ENUM,
    FDP.TYPE_SFIXED32       : CppType.CPPTYPE_INT32,
    FDP.TYPE_SFIXED64       : CppType.CPPTYPE_INT64,
    FDP.TYPE_SINT32         : CppType.CPPTYPE_INT32,
    FDP.TYPE_SINT64         : CppType.CPPTYPE_INT64
}

CC_TYPE = {
    FDP.TYPE_DOUBLE         : 'double',
    FDP.TYPE_FLOAT          : 'float',
    FDP.TYPE_INT64          : '::google::protobuf::int64',
    FDP.TYPE_UINT64         : '::google::protobuf::uint64',
    FDP.TYPE_INT32          : '::google::protobuf::int32',
    FDP.TYPE_FIXED64        : '::google::protobuf::uint64',
    FDP.TYPE_FIXED32        : '::google::protobuf::uint32',
    FDP.TYPE_BOOL           : 'bool',
    FDP.TYPE_STRING         : 'std::string',
    FDP.TYPE_MESSAGE        : 'message',
    FDP.TYPE_BYTES          : 'std::string',
    FDP.TYPE_UINT32         : '::google::protobuf::uint32',
    FDP.TYPE_ENUM           : 'int',
    FDP.TYPE_SFIXED32       : '::google::protobuf::int32',
    FDP.TYPE_SFIXED64       : '::google::protobuf::int64',
    FDP.TYPE_SINT32         : '::google::protobuf::int32',
    FDP.TYPE_SINT64         : '::google::protobuf::int64'
}
def printerr(*args):
    sys.stderr.write(" ".join(args))
    sys.stderr.write("\n")
    sys.stderr.flush()

class TreeNode(object):
    def __init__(self, name, parent=None, filename=None, package=None):
        super(TreeNode, self).__init__()
        self.child = []
        self.parent = parent
        self.filename = filename
        self.package = package
        if parent:
            self.parent.add_child(self)
        self.name = name

    def add_child(self, child):
        self.child.append(child)

    def find_child(self, child_names):
        if child_names:
            for i in self.child:
                if i.name == child_names[0]:
                    return i.find_child(child_names[1:])
            raise StandardError
        else:
            return self

    def get_child(self, child_name):
        for i in self.child:
            if i.name == child_name:
                return i
        return None

    def get_path(self, end = None):
        pos = self
        out = []
        while pos and pos != end:
            out.append(pos.name)
            pos = pos.parent
        out.reverse()
        return '.'.join(out)

    def get_global_name(self):
        return self.get_path()

    def get_local_name(self):
        pos = self
        while pos.parent:
            pos = pos.parent
            if self.package and pos.name == self.package[-1]:
                break
        return self.get_path(pos)

    def __str__(self):
        return self.to_string(0)

    def __repr__(self):
        return str(self)

    def to_string(self, indent = 0):
        return ' '*indent + '<TreeNode ' + self.name + '(\n' + \
                ','.join([i.to_string(indent + 4) for i in self.child]) + \
                ' '*indent +')>\n'

class Env(object):
    filename = None
    package = None
    extend = None
    descriptor = None
    message = None
    message2 = None
    context = None
    register = None
    def __init__(self):
        self.message_tree = TreeNode('')
        self.scope = self.message_tree

    def get_global_name(self):
        return self.scope.get_global_name()

    def get_local_name(self):
        return self.scope.get_local_name()

    def get_ref_name(self, type_name):
        try:
            node = self.lookup_name(type_name)
        except:
            # if the child doesn't be founded, it must be in this file
            return type_name[len('.'.join(self.package)) + 2:]
        #if node.filename != self.filename:
        #    return node.filename + '_pb.' + node.get_local_name()
        return node.get_global_name().replace('.', '::')

    def get_ref_name3(self, type_name):
        try:
            node = self.lookup_name(type_name)
        except:
            # if the child doesn't be founded, it must be in this file
            return type_name[len('.'.join(self.package)) + 2:].upper()
        if node.filename != self.filename:
            return node.filename + '_pb.' + node.filename.upper() + '_PB_' + node.get_local_name().upper()
        return node.get_local_name().upper()
		
    def lookup_name(self, name):
        names = name.split('.')
        if names[0] == '':
            return self.message_tree.find_child(names[1:])
        else:
            return self.scope.parent.find_child(names)

    def enter_package(self, package):
        if not package:
            return self.message_tree
        names = package.split('.')
        pos = self.message_tree
        for i, name in enumerate(names):
            new_pos = pos.get_child(name)
            if new_pos:
                pos = new_pos
            else:
                return self._build_nodes(pos, names[i:])
        return pos

    def enter_file(self, filename, package):
        self.filename = filename
        self.package = package.split('.')
        self._init_field()
        self.scope = self.enter_package(package)

    def exit_file(self):
        self._init_field()
        self.filename = None
        self.package = []
        self.scope = self.scope.parent

    def enter(self, message_name):
        self.scope = TreeNode(message_name, self.scope, self.filename,
                              self.package)

    def exit(self):
        self.scope = self.scope.parent

    def _init_field(self):
        self.descriptor = []
        self.context = []
        self.message = []
        self.message2 = []
        self.register = []

    def _build_nodes(self, node, names):
        parent = node
        for i in names:
            parent = TreeNode(i, parent, self.filename, self.package)
        return parent

class Writer(object):
    def __init__(self, prefix=None):
        self.io = StringIO()
        self.__indent = ''
        self.__prefix = prefix

    def getvalue(self):
        return self.io.getvalue()

    def __enter__(self):
        self.__indent += '    '
        return self

    def __exit__(self, type, value, trackback):
        self.__indent = self.__indent[:-4]

    def __call__(self, data):
        self.io.write(self.__indent)
        if self.__prefix:
            self.io.write(self.__prefix)
        self.io.write(data)

DEFAULT_VALUE = {
    FDP.TYPE_DOUBLE         : '0.0',
    FDP.TYPE_FLOAT          : '0.0',
    FDP.TYPE_INT64          : '0',
    FDP.TYPE_UINT64         : '0',
    FDP.TYPE_INT32          : '0',
    FDP.TYPE_FIXED64        : '0',
    FDP.TYPE_FIXED32        : '0',
    FDP.TYPE_BOOL           : 'false',
    FDP.TYPE_STRING         : '""',
    FDP.TYPE_MESSAGE        : 'nil',
    FDP.TYPE_BYTES          : '""',
    FDP.TYPE_UINT32         : '0',
    FDP.TYPE_ENUM           : '1',
    FDP.TYPE_SFIXED32       : '0',
    FDP.TYPE_SFIXED64       : '0',
    FDP.TYPE_SINT32         : '0',
    FDP.TYPE_SINT64         : '0',
}

def code_gen_field(index, field_desc, env):
    full_name = env.get_local_name() + '.' + field_desc.name
    obj_name = full_name.upper().replace('.', '_') + '_FIELD'
	
    class_name = env.get_local_name()
    full_class_name = env.get_global_name().replace('.', '::')
    message_type_name = CC_TYPE[field_desc.type]
    if field_desc.HasField('type_name'):
        if field_desc.type == FDP.TYPE_MESSAGE:
            message_type_name = env.get_ref_name(field_desc.type_name)
        else:
            message_type_name = field_desc.type_name.replace('.', '::');		
    
    if field_desc.label == FDP.LABEL_REPEATED:
        env.message.append('\n  .def("%s_size", (int (%s::*)(void) const)&%s::%s_size)' % (field_desc.name.lower(), full_class_name, full_class_name, field_desc.name.lower()))
        if field_desc.type == FDP.TYPE_MESSAGE:
            env.message.append('\n  .def("add_%s", (%s* (%s::*)(void))&%s::add_%s)' % (field_desc.name.lower(), message_type_name, full_class_name, full_class_name, field_desc.name.lower()))
            env.message.append('\n  .def("%s", (const %s& (%s::*)(int) const)&%s::%s)' % (field_desc.name.lower(), message_type_name, full_class_name, full_class_name, field_desc.name.lower()))
        elif (field_desc.type == FDP.TYPE_STRING or field_desc.type == FDP.TYPE_BYTES):
            env.message.append('\n  .def("add_%s", (void (%s::*)(const char*))&%s::add_%s)' % (field_desc.name.lower(), full_class_name, full_class_name, field_desc.name.lower()))
            env.message.append('\n  .def("%s", (const %s& (%s::*)(int) const)&%s::%s)' % (field_desc.name.lower(), message_type_name, full_class_name, full_class_name, field_desc.name.lower()))
        else:
            env.message.append('\n  .def("add_%s", (void (%s::*)(%s))&%s::add_%s)' % (field_desc.name.lower(), full_class_name, message_type_name, full_class_name, field_desc.name.lower()))
            env.message.append('\n  .def("%s", (%s (%s::*)(int) const)&%s::%s)' % (field_desc.name.lower(), message_type_name, full_class_name, full_class_name, field_desc.name.lower()))
    else:
        if field_desc.type == FDP.TYPE_MESSAGE:
            env.message.append('\n  .def("%s", (const %s& (%s::*)(void) const)&%s::%s)' % (field_desc.name.lower(), message_type_name, full_class_name, full_class_name, field_desc.name.lower()))
            env.message.append('\n  .def("mutable_%s", (%s* (%s::*)(void))&%s::mutable_%s)' % (field_desc.name.lower(), message_type_name, full_class_name, full_class_name, field_desc.name.lower()))
        elif (field_desc.type == FDP.TYPE_STRING or field_desc.type == FDP.TYPE_BYTES):
            env.message.append('\n  .property("%s", (const std::string& (%s::*)(void) const)&%s::%s, (void (%s::*)(const char*))&%s::set_%s)' % (field_desc.name.lower(), full_class_name, full_class_name, field_desc.name.lower(), full_class_name, full_class_name, field_desc.name.lower()))
        else:
            env.message.append('\n  .property("%s", (%s (%s::*)(void) const)&%s::%s, (void (%s::*)(%s))&%s::set_%s)' % (field_desc.name.lower(), message_type_name, full_class_name, full_class_name, field_desc.name.lower(), full_class_name, message_type_name, full_class_name, field_desc.name.lower()))
    return obj_name

def code_gen_message(message_descriptor, env, containing_type = None):
    env.enter(message_descriptor.name)
    full_name = env.get_local_name()
    obj_name = full_name.upper().replace('.', '_')
    class_name = env.get_local_name()
    full_class_name = env.get_global_name().replace('.', '::')

    env.message.append('luabind::scope Register_%s() {\n' % class_name)
    env.message2.append('Register_%s' % class_name)
    env.message.append(' return luabind::class_< %s, ::google::protobuf::Message, ::google::protobuf::MessageLite>("%s")\n' % (full_class_name, class_name))
    env.message.append('  .def(luabind::constructor<>())')

    fields = []
    for i, field_desc in enumerate(message_descriptor.field):
        fields.append(code_gen_field(i, field_desc, env))

    env.message.append(';\n}\n\n')
    env.exit()
    return obj_name

def write_header(writer):
    writer("""// Generated By protoc-gen-luabind.  DO NOT EDIT!
//

""")

def code_gen_file(proto_file, env, is_gen):
    filename = path.splitext(proto_file.name)[0]
    env.enter_file(filename, proto_file.package)

    includes = []
    for f in proto_file.dependency:
        inc_file = path.splitext(f)[0]
        includes.append(inc_file)

    enums = []
    for enum_desc in proto_file.enum_type:
        enums.append('luabind::scope Register_%s() {\n' % enum_desc.name)
        env.message2.append('Register_%s' % enum_desc.name)
        enums.append(' return luabind::enum_("%s").def() [\n' % enum_desc.name)
        for enum_value in enum_desc.value:
            enums.append('  luabind::value("%s", %s)' % (enum_value.name,
                                              enum_value.number))
            enums.append(',\n')
        enums.pop()
        enums.append('\n')
        enums.append(' ];\n}\n\n')

    for msg_desc in proto_file.message_type:
        code_gen_message(msg_desc, env)

    if is_gen:
        lua = Writer()

        write_header(lua)
		
        lua('#include "%s.pb.h"\n\n' % env.filename)
		
        lua('#include "luabind/luabind.hpp"\n')
        lua('#include "luabind/enum.hpp"\n')
        lua('#include "luabind/out_value_policy.hpp"\n\n')
        lua('#include "scriptengine/luabind_register_manager.h"\n\n')
		
        map(lua, enums)
		
        lua('\n')
        map(lua, env.message)

        registers = []
        registers.append('//////////////////////////////////////////////////\n')
        registers.append('void LuabindPB_%s_RegisterAll() {\n' % env.filename)
        for func_name in env.message2:
            registers.append('  LuabindRegisterManager::GetInstance()->RegisterLuabindMessage(&%s);\n' % func_name)

        registers.append('}\n\n')
        registers.append('//////////////////////////////////////////////////\n')
        map(lua, registers)
		
        _files[env.filename+ '.luabind_pb.cc'] = lua.getvalue()
    env.exit_file()

def main():
    plugin_require_bin = sys.stdin.read()
    code_gen_req = plugin_pb2.CodeGeneratorRequest()
    code_gen_req.ParseFromString(plugin_require_bin)

    env = Env()
    for proto_file in code_gen_req.proto_file:
        code_gen_file(proto_file, env,
                proto_file.name in code_gen_req.file_to_generate)

    code_generated = plugin_pb2.CodeGeneratorResponse()
    for k in  _files:
        file_desc = code_generated.file.add()
        file_desc.name = k
        file_desc.content = _files[k]

    sys.stdout.write(code_generated.SerializeToString())

if __name__ == "__main__":
    main()

