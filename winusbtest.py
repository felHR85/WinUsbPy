"""Test1: Execute every function to check if executes correctly.It does not mean They are called in a meaningful way. Further tests will check that """
from winusb import WinUSBApi
from winusbutils import *
from ctypes import *
from ctypes.wintypes import *
b=UsbSetupPacket()
api = WinUSBApi()
guid = GUID()
enumerator = c_wchar_p()
hwnd = HANDLE()
flags = DWORD()
sp_device_info_data = SpDevinfoData()
member_index = DWORD(0)
sp_device_interface_data = SpDeviceInterfaceData()

"""SetupDiGetClassDevs"""
"""
Device interface (GUID) is specified in the .INF file (WINUSB template)
"""
#Guid beter byref(guid)
hdev_info = api.exec_function_setupapi("SetupDiGetClassDevs", pointer(guid), enumerator, hwnd, flags)

response = api.exec_function_setupapi("SetupDiEnumDeviceInterfaces", hdev_info, byref(sp_device_info_data), pointer(guid), member_index, byref(sp_device_interface_data)) 

