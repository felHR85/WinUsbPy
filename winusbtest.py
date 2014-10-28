from winusb import *

api = WinUSBApi()
guid = GUID()
enumerator = c_wchar_p()
hwnd = HANDLE()
flags = DWORD()

hdev_info = api.exec_function_setupapi(guid, enumerator, hwnd, flags, function_name="SetupDiGetClassDevs")