"""Test1: Execute every function to check if executes correctly.It does not mean They are called in a meaningful way. Further tests will check that """
from winusb import WinUSBApi
from winusbutils import *
from ctypes import *
from ctypes.wintypes import *
from winusbclasses import DIGCF_DEVICE_INTERFACE, DIGCF_PRESENT, GENERIC_WRITE, GENERIC_READ, FILE_SHARE_READ, FILE_SHARE_WRITE, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, FILE_FLAG_OVERLAPPED, INVALID_HANDLE_VALUE

api = WinUSBApi()
byte_array = c_byte * 8
guid = GUID(0xA5DCBF10L, 0x6530, 0x11D2, byte_array(0x90, 0x1F, 0x00, 0xC0, 0x4F, 0xB9, 0x51, 0xED))
flags = DWORD(DIGCF_DEVICE_INTERFACE | DIGCF_PRESENT)
i = 0
member_index = DWORD(i)
required_size = c_ulong(0)

sp_device_info_data = SpDevinfoData()
sp_device_interface_data = SpDeviceInterfaceData()
sp_device_interface_detail_data = SpDeviceInterfaceDetailData()

"""
Enumerate all USB Devices
"""
hdev_info = api.exec_function_setupapi("SetupDiGetClassDevs", byref(guid), None, None, flags)
print hdev_info
sp_device_interface_data.cb_size = sizeof(sp_device_interface_data)
#sp_device_interface_data.cb_size = sizeof(SpDeviceInterfaceData)
sp_device_info_data.cb_size = sizeof(sp_device_info_data)

while api.exec_function_setupapi("SetupDiEnumDeviceInterfaces", hdev_info, None, byref(guid), member_index, byref(sp_device_interface_data)):
	# Get the required buffer size
	api.exec_function_setupapi("SetupDiGetDeviceInterfaceDetail", hdev_info, byref(sp_device_interface_data), None, 0, byref(required_size), None)
	resize(sp_device_interface_detail_data, required_size.value)
	
	""" I have been stuck here for hours. cb_size must reflect the fix part of the Struct!!!!"""
	sp_device_interface_detail_data.cb_size = sizeof(SpDeviceInterfaceDetailData) - sizeof(WCHAR * 1)
	
	if api.exec_function_setupapi("SetupDiGetDeviceInterfaceDetail", hdev_info, byref(sp_device_interface_data), byref(sp_device_interface_detail_data), required_size, byref(required_size), byref(sp_device_info_data)):
		print "PATH: " +  wstring_at(byref(sp_device_interface_detail_data, sizeof(DWORD)))
	else:
		error_code = api.exec_function_kernel32("GetLastError")
		print "Error: " + str(error_code)

	i += 1
	member_index = DWORD(i)
	required_size = c_ulong(0)
	resize(sp_device_interface_detail_data, sizeof(SpDeviceInterfaceDetailData))

"""Open last encountered device"""
path = wstring_at(byref(sp_device_interface_detail_data, sizeof(DWORD)))
handle_file = api.exec_function_kernel32("CreateFileW", path, GENERIC_WRITE|GENERIC_READ, FILE_SHARE_WRITE|FILE_SHARE_READ, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL|FILE_FLAG_OVERLAPPED, None)
if INVALID_HANDLE_VALUE == handle_file:
	print "Error"
else:
	print "No error"
	handle_winusb = c_void_p()
	result = api.exec_function_winusb("WinUsb_Initialize", handle_file, byref(handle_winusb))
	if result == 0:
		error_code = api.exec_function_kernel32("GetLastError")
		print "Error" + str(error_code)
	print result