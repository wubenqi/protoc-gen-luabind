// Copyright 2010, www.lelewan.com
// All rights reserved
//
// Author: wubenqi<wubenqi@caitong.net>, 2012-08-02
//

#include "google/protobuf/message.h"
#include "luabind/luabind.hpp"
#include "luabind/out_value_policy.hpp"

namespace {
struct IOBuffer {
	IOBuffer(int size) {
		data = new char[size];
		data_len = size;
	}

	IOBuffer() {
		data_len = 0;
		data = 0;
	}

	~IOBuffer() {
		if (data) {
			delete [] data;
		}
		data_len = 0;
	}

	void ReSize(int size) {
		if (size>data_len) {
			if (data) {
				delete [] data;
				data = new char[size];
			}
		}
		data_len = size;
	}

	char* data;
	int data_len;
};

bool ParseFromIOBuffer(google::protobuf::MessageLite* message_lite, const IOBuffer& data) {
	return message_lite->ParseFromArray(data.data, data.data_len);
}

bool SerializeToIOBuffer(google::protobuf::MessageLite* message_lite, IOBuffer* output) {
	output->ReSize(message_lite->ByteSize());
	return message_lite->SerializeToArray(output->data, output->data_len);
}

}

luabind::scope Register_IOBuffer() {
	return luabind::class_<IOBuffer>("IOBuffer")
		.def(luabind::constructor<int>())
		.def(luabind::constructor<>());
}

luabind::scope Register_MessageLite() {
	return luabind::class_<google::protobuf::MessageLite>("MessageLite")
		.def("ParseFromIOBuffer", &ParseFromIOBuffer)
		.def("SerializeToIOBuffer", &SerializeToIOBuffer, luabind::out_value(_3))
		.def("ByteSize", &google::protobuf::MessageLite::ByteSize);
}

luabind::scope Register_Message() {
	return luabind::class_<google::protobuf::Message, google::protobuf::MessageLite>("Message")
		.def("PrintDebugString", &google::protobuf::Message::PrintDebugString);
}


#if 0
void LuaPBTest() {
	ScriptManager::CreateSingleton();
	//GetInstance();
	ScriptManager::GetInstance().Init();
	RegisterPB(ScriptManager::GetInstance().GetLuaState());
	ScriptManager::GetInstance().Load();
	ScriptManager::GetInstance().CallFunction("LuaPBTest");

	ScriptManager::DeleteSingleton();
}
#endif

#if 0
			luabind::enum_("EnumType").def() [
				luabind::value("kEnumType_1", 1),
					luabind::value("kEnumType_2", 2)
			],

			luabind::enum_("EnumType2").def() [
				luabind::value("kEnumType2_1", 1),
					luabind::value("kEnumType2_2", 2)
			],


			luabind::class_<hammer::common::MTest, google::protobuf::Message>("MTest")
			.def(luabind::constructor<>())
			.property("name", (const ::std::string& (hammer::common::MTest::*)(void))&hammer::common::MTest::name, (void (hammer::common::MTest::*)(const char*))&hammer::common::MTest::set_name)
			.property("value", (::google::protobuf::uint32 (hammer::common::MTest::*)(void))&hammer::common::MTest::value, (void (hammer::common::MTest::*)(::google::protobuf::uint32))&hammer::common::MTest::set_value),

			luabind::class_<hammer::common::MTestList, google::protobuf::Message>("MTestList")
			.def(luabind::constructor<>())
			.def("one", (const hammer::common::MTest& (hammer::common::MTestList::*)(void))&hammer::common::MTestList::one)
			.def("mutable_one", (hammer::common::MTest* (hammer::common::MTestList::*)(void))&hammer::common::MTestList::mutable_one)
			.def("add_all", (hammer::common::MTest* (hammer::common::MTestList::*)(void))&hammer::common::MTestList::add_all)
			.def("all", (const hammer::common::MTest& (hammer::common::MTestList::*)(int) const)&hammer::common::MTestList::all)
			.def("all_size", (int (hammer::common::MTestList::*)())&hammer::common::MTestList::all_size)

			//.property("all", (::google::protobuf::uint32 (hammer::common::MTestList::*)(void))&hammer::common::MTestList::value, (void (hammer::common::MTestList::*)(::google::protobuf::uint32))&hammer::common::MTestList::set_value)
			//,
			//luabind::class_<hammer::common::MTest, google::protobuf::Message>("MTest")
			//.def(luabind::constructor<>())
			//.property("item_name", (const ::std::string& (hammer::common::MTest::*)(void))&hammer::common::MTest::item_name, (void (hammer::common::MTest::*)(const char*))&hammer::common::MTest::set_item_name)
			//.property("item_amount", (::google::protobuf::uint32 (hammer::common::MTest::*)(void))&hammer::common::MTest::item_amount, (void (hammer::common::MTest::*)(::google::protobuf::uint32))&hammer::common::MTest::set_item_amount)


			//enum ItemPayType {
			//	kItemPayType_Gold = 1,
			//	kItemPayType_Rmb = 2,
			//	kItemPayType_Yupai = 3
			//};

			//luabind::enum_("ItemPayType")
			//[
			//	value("my_enum", 4),
			//	value("my_2nd_enum", 7),
			//	value("another_enum", 6)
			//]
#endif
