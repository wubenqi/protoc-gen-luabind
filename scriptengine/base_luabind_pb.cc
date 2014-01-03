// Copyright (C) 2012 by wubenqi
// Distributable under the terms of either the Apache License (Version 2.0) or 
// the GNU Lesser General Public License, as specified in the COPYING file.
//
// By: wubenqi<wubenqi@gmail.com>
//

#include "scriptengine/base_luabind_pb.h"

#include "google/protobuf/message.h"

#include "luabind/luabind.hpp"
#include "luabind/out_value_policy.hpp"
#include "luabind/raw_policy.hpp"


class IOBuffer2 {
public:
  explicit IOBuffer2(int size) {
    data_ = static_cast<char*>(malloc(size));
    size_ = size;
    is_new_ = true;
  }

  IOBuffer2(const void* data, int size) {
    data_ = static_cast<char*>(const_cast<void*>(data));
    is_new_ = false;
  }

  ~IOBuffer2() {
    if (is_new_) {
      free(data_);
    }
  }

  inline char* data() const {
    return data_;
  }

  inline int size() const {
    return size_;
  }

private:
  char* data_;
  int size_;
  bool is_new_;
};

namespace {

bool ParseFromIOBuffer(google::protobuf::MessageLite* message_lite, const IOBuffer2& data) {
	return message_lite->ParseFromArray(data.data(), data.size());
}

IOBuffer2* SerializeToIOBuffer(const google::protobuf::MessageLite* message_lite) {
  IOBuffer2* io_buffer = new IOBuffer2(message_lite->ByteSize());
  if (io_buffer) {
    if(!message_lite->SerializeToArray(io_buffer->data(), io_buffer->size())) {
      delete io_buffer;
      io_buffer = NULL;
    }
  }
  return io_buffer;
}

bool ParseFromString(google::protobuf::MessageLite* message_lite, const std::string& data) {
  return message_lite->ParseFromString(data);
}

std::string SerializeToString(const google::protobuf::MessageLite* message_lite) {
  std::string data;
  message_lite->SerializeToString(&data);
  return data;
}

void ToString(IOBuffer2* io_buffer, lua_State* L) {
	lua_pushlstring(L, io_buffer->data(), io_buffer->size());
}

}

luabind::scope LuabindPBRegister_IOBuffer() {
 return luabind::class_<IOBuffer2>("IOBuffer")
  .def(luabind::constructor<int>())
  .def(luabind::constructor<const char*, int>())
  .def("ToString", &ToString)
  .def("GetDataLen", &IOBuffer2::size);
}

luabind::scope LuabindPBRegister_MessageLite() {
 return luabind::class_<google::protobuf::MessageLite>("MessageLite")
  .def("ParseFromIOBuffer", &ParseFromIOBuffer)
  .def("SerializeToIOBuffer", &SerializeToIOBuffer)
  .def("ParseFromString", &ParseFromString)
  .def("SerializeToString", &SerializeToString)
  .def("ByteSize", &google::protobuf::MessageLite::ByteSize)
  .def("Clear", &google::protobuf::MessageLite::Clear);
}

luabind::scope LuabindPBRegister_Message() {
 return luabind::class_<google::protobuf::Message, google::protobuf::MessageLite>("Message")
  .def("PrintDebugString", &google::protobuf::Message::PrintDebugString)
  .def("Utf8DebugString", &google::protobuf::Message::Utf8DebugString)
  .def("CopyFrom", &google::protobuf::Message::CopyFrom);
}

