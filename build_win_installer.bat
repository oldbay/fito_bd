python.exe setup_cx.py build

md .\build\exe.win32-2.7\camelot
xcopy C:\Python27\Lib\site-packages\Camelot-12.06.29-py2.7.egg\camelot .\build\exe.win32-2.7\camelot /e

xcopy .\for_build .\build\exe.win32-2.7 /e

md  .\build\exe.win32-2.7\plugins
xcopy C:\Python27\Lib\site-packages\PyQt4\plugins .\build\exe.win32-2.7\plugins /e

md .\build\exe.win32-2.7\fito_bd
xcopy .\fito_bd .\build\exe.win32-2.7\fito_bd /e

del .\build\exe.win32-2.7\fito_bd\translations\*.po
del .\build\exe.win32-2.7\fito_bd\translations\*.pot
del .\build\exe.win32-2.7\fito_bd\translations\*.sh
del .\build\exe.win32-2.7\fito_bd\translations\*.mo

python.exe setup_cx.py bdist_msi
