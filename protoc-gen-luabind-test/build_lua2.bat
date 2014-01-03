@set out_src=.\
@set language=lua
@set import=-I.\


@set path=%path%;%protobuf_lib%
@echo off
FOR   %%f   IN   (*.proto)   DO   (   
  echo %%f
  ..\protoc-gen-luabind\protoc %import% --plugin=protoc-gen-lua="..\protoc-gen-luabind\protoc-gen-luabind.bat" --%language%_out=%out_src% %%f 
)

pause