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
interface_detail_size = DWORD(0)
required_size = DWORD(0)
sp_device_interface_detail_data = SpDeviceInterfaceDetailData()

"""SetupDiGetClassDevs"""
"""
Device interface (GUID) is specified in the .INF file (WINUSB template)
"""
#Guid beter byref(guid)
hdev_info = api.exec_function_setupapi("SetupDiGetClassDevs", pointer(guid), enumerator, hwnd, flags)

response_interfaces = api.exec_function_setupapi("SetupDiEnumDeviceInterfaces", hdev_info, byref(sp_device_info_data), pointer(guid), member_index, byref(sp_device_interface_data))

response_details = api.exec_function_setupapi("SetupDiGetDeviceInterfaceDetail", hdev_info, byref(sp_device_interface_data), byref(sp_device_interface_detail_data), interface_detail_size, byref(required_size), byref(sp_device_info_data)) 
print response_details
