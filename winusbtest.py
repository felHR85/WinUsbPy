"""Test1: PL2303 serial port user-space driver using WINUSB"""
from winusb import WinUSBApi
from winusbutils import *
from ctypes import *
from ctypes.wintypes import *
from winusbclasses import DIGCF_DEVICE_INTERFACE, DIGCF_PRESENT, GENERIC_WRITE, GENERIC_READ, FILE_SHARE_READ, FILE_SHARE_WRITE, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, FILE_FLAG_OVERLAPPED, INVALID_HANDLE_VALUE

pl2303_vid = "067b"
pl2303_pid = "2303"
path = ""
interface_descriptor = UsbInterfaceDescriptor()

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

sp_device_interface_data.cb_size = sizeof(sp_device_interface_data)
sp_device_info_data.cb_size = sizeof(sp_device_info_data)

"""
Enumerate all USB Devices
"""
hdev_info = api.exec_function_setupapi("SetupDiGetClassDevs", byref(guid), None, None, flags)

while api.exec_function_setupapi("SetupDiEnumDeviceInterfaces", hdev_info, None, byref(guid), member_index, byref(sp_device_interface_data)):
	# Get the required buffer size and resize SpDeviceInterfaceDetailData
	api.exec_function_setupapi("SetupDiGetDeviceInterfaceDetail", hdev_info, byref(sp_device_interface_data), None, 0, byref(required_size), None)
	resize(sp_device_interface_detail_data, required_size.value)
	
	""" I have been stuck here for hours. cb_size must reflect the fix part of the Struct!!!!"""
	sp_device_interface_detail_data.cb_size = sizeof(SpDeviceInterfaceDetailData) - sizeof(WCHAR * 1)
	
	if api.exec_function_setupapi("SetupDiGetDeviceInterfaceDetail", hdev_info, byref(sp_device_interface_data), byref(sp_device_interface_detail_data), required_size, byref(required_size), byref(sp_device_info_data)):
		path = wstring_at(byref(sp_device_interface_detail_data, sizeof(DWORD)))
		if is_device(pl2303_vid, pl2303_pid, path):
			print "PL 2303 PATH: " + path
			break
	else:
		error_code = api.exec_function_kernel32("GetLastError")
		print "Error: " + str(error_code)

	i += 1
	member_index = DWORD(i)
	required_size = c_ulong(0)
	resize(sp_device_interface_detail_data, sizeof(SpDeviceInterfaceDetailData))

"""Open PL2303 Device"""
handle_file = api.exec_function_kernel32("CreateFileW", path, GENERIC_WRITE|GENERIC_READ, FILE_SHARE_WRITE|FILE_SHARE_READ, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL|FILE_FLAG_OVERLAPPED, None)
if INVALID_HANDLE_VALUE == handle_file:
	print "Error Creating File"
else:
	print "No error"
	handle_winusb = c_void_p()
	result = api.exec_function_winusb("WinUsb_Initialize", handle_file, byref(handle_winusb))
	if result != 0:
		""" Get PL2303 Speed """
		info_type = c_ulong(1)
		buff = c_void_p()
		result = api.exec_function_winusb("WinUsb_QueryDeviceInformation", handle_winusb, info_type, buff)
		if result != 0:
			print "SPEED: " + buff.value

		""" Interface Settings """
		response = api.exec_function_winusb("WinUsb_QueryInterfaceSettings", handle_winusb ,c_ubyte(0), byref(interface_descriptor))
		if response != 0:
			print "bLength: " + interface_descriptor.b_length.value
			print "bDescriptorType: " + interface_descriptor.b_descriptor_type.value
			print "bInterfaceNumber: " + interface_descriptor.b_interface_number.value
			print "bAlternateSetting: " + interface_descriptor.b_alternate_setting.value
			print "bNumEndpoints " + interface_descriptor.b_num_endpoints.value
			print "bInterfaceClass " + interface_descriptor.b_interface_class.value
			print "bInterfaceSubClass: " + interface_descriptor.b_interface_sub_class.value
			print "bInterfaceProtocol: " + interface_descriptor.b_interface_protocol.value
			print "iInterface: " + interface_descriptor.i_interface.value

			""" Endpoints information """
			i = 0
			endpoint_index = c_ubyte(0)
			pipe_info = PipeInfo()
			while i <= interface_descriptor.b_num_endpoints.value:
				result = api.exec_function_winusb("WinUsb_QueryPipe", handle_winusb, c_ubyte(0), endpoint_index, byref(pipe_info))
				if result != 0:
					print "PipeType: " + pipe_info.pipe_type.value
					print "PipeId: " + pipe_info.pipe_id.value
					print "MaximumPacketSize: " + pipe_info.maximum_packet_size.value
					print "Interval: " + pipe_info.interval.value
				i += 1
				endpoint_index = c_ubyte(i)

			""" Control setup """

	else:
		error_code = api.exec_function_kernel32("GetLastError")
		print "Error" + str(error_code)