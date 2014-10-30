"""Test1: Execute every function to check if executes correctly.It does not mean They are called in a meaningful way. Further tests will check that """
from winusb import WinUSBApi
from winusbutils import *
from ctypes import *
from ctypes.wintypes import *
b=UsbSetupPacket()
api = WinUSBApi()
byte_array = c_byte * 8
guid = GUID(0xA5DCBF10L, 0x6530, 0x11D2, byte_array(0x90, 0x1F, 0x00, 0xC0, 0x4F, 0xB9, 0x51, 0xED))
enumerator = c_wchar_p("USB")
hwnd = HANDLE()
flags = DWORD(18) # Devices present DIGCF_PRESENT
i = 0
member_index = DWORD(i)

sp_device_info_data = SpDevinfoData()
sp_device_interface_data = SpDeviceInterfaceData()

"""
Enumerate all USB Devices
"""
#Guid beter byref(guid)
hdev_info = api.exec_function_setupapi("SetupDiGetClassDevs", byref(guid), None, None, flags)
print hdev_info
sp_device_interface_data.cb_size = sizeof(sp_device_interface_data)
while api.exec_function_setupapi("SetupDiEnumDeviceInterfaces", hdev_info, None, byref(guid), member_index, byref(sp_device_interface_data)):
	print sp_device_interface_data.cb_size
	print sp_device_interface_data.interface_class_guid.data1
	i += 1
	member_index = DWORD(i)


#response_details = api.exec_function_setupapi("SetupDiGetDeviceInterfaceDetail", hdev_info, byref(sp_device_interface_data), byref(sp_device_interface_detail_data), interface_detail_size, byref(required_size), byref(sp_device_info_data)) 
#print response_details
