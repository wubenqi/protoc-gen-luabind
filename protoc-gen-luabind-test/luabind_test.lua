-- Copyright 2010, www.lelewan.com
-- All rights reserved
--
-- 此代码为message_handler_tool工具自动生成，请在函数体里实现您的逻辑
--

function DoMain()
--[[
	local message = 
	local message_size = message:ByteSize()
	print('source message, size = ' .. message_size)
	

	message:PrintDebugString()
	-- IOBuffer io_buffer
	local io_buffer = message:SerializeToIOBuffer()
	
	print('dest message')
	local message2 = MTestList()
	message2:ParseFromIOBuffer(io_buffer)
	message2:PrintDebugString()
	
--]]
	
	-- ETest
	print('enum test...')
	print('enum kEnumType_1 = ' .. kEnumTest_1)
	print('enum kEnumType_2 = ' .. kEnumTest_2)
	print('enum kEnumTest_3 = ' .. kEnumTest_3)

	-- MTest
	local mtest = MTest()
	mtest.name = 'wubenqi'
	mtest.value = 2
	mtest:PrintDebugString()
	
	-- MTestList
	local mtest_list = MTestList()
	
	-- MTestList/one
	local one = mtest_list:mutable_one()
	one.name = 'wubenqi_0'
	one.value = 0
	
	-- MTestList/m_all
	one = mtest_list:add_m_all()
	one.name = 'wubenqi_1'
	one.value = 1
	
	one = mtest_list:add_m_all()
	one.name = 'wubenqi_2'
	one.value = 2

	-- MTestList/i_all
	mtest_list:add_i_all(1)
	mtest_list:add_i_all(2)
	--mtest_list:PrintDebugString()

	-- MTestList/s_all
	mtest_list:add_s_all("wubenqi_s1")
	mtest_list:add_s_all("wubenqi_s2")
	
	mtest_list.i_t = 10
	mtest_list.s_t = "wubenqi_st"
	mtest_list.b_t = "wubenqi_bt"
	mtest_list.e_t = kEnumTest_1
	
	print('\n\n')
	mtest_list:PrintDebugString()
	
	local io_buffer = mtest_list:SerializeToIOBuffer()
	local mtest_list2 = MTestList()
	mtest_list2:ParseFromIOBuffer(io_buffer)
	
	print('\n\n')
	mtest_list2:PrintDebugString()
	
	local data = io_buffer:ToString()
	print(string.len(data) .. " ==> " .. io_buffer:GetDataLen())
	local o = io.open("mtest_list.data", "wb")
	o:write(data)
	o:close()
	
	return 1
end
