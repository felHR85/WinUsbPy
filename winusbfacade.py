from winusb import WinUSBApi
from winusbclasses import GUID, DIGCF_ALLCLASSES, DIGCF_DEFAULT, DIGCF_PRESENT, DIGCF_PROFILE, DIGCF_DEVICE_INTERFACE, SpDeviceInterfaceData,  SpDeviceInterfaceDetailData, SpDevinfoData, GENERIC_WRITE, GENERIC_READ, FILE_SHARE_WRITE, FILE_SHARE_READ, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, FILE_FLAG_OVERLAPPED, INVALID_HANDLE_VALUE
from ctypes import c_byte, byref, sizeof, c_ulong, resize, wstring_at, c_void_p
from ctypes.wintypes import DWORD, WCHAR
from winusbutils import SetupDiGetClassDevs, SetupDiEnumDeviceInterfaces, SetupDiGetDeviceInterfaceDetail, is_device, CreateFileW, WinUsb_Initialize, Close_Handle, WinUsb_Free, GetLastError

class WinUsbPy(object):

	def __init__(self):
		self.api = WinUSBApi()
		byte_array = c_byte * 8
		self.guid = GUID(0xA5DCBF10L, 0x6530, 0x11D2, byte_array(0x90, 0x1F, 0x00, 0xC0, 0x4F, 0xB9, 0x51, 0xED))
		self.handle_file = INVALID_HANDLE_VALUE
		self.handle_winusb = c_void_p()


	def list_usb_devices(self, **kwargs):
		self.device_paths = []
		value = 0x00000000
		try:
			if kwargs["default"] == True:
				value |= DIGCF_DEFAULT
			if kwargs["present"] == True:
				value |= DIGCF_PRESENT
			if kwargs["allclasses"] == True:
				value |= DIGCF_ALLCLASSES
			if kwargs["profile"] == True:
				value |= DIGCF_PROFILE
			if kwargs["deviceinterface"] == True:
				value |= DIGCF_DEVICE_INTERFACE
		except KeyError:
			if value == 0x00000000:
				value = 0x00000010
			pass

		flags = DWORD(value)
		self.handle = self.api.exec_function_setupapi(SetupDiGetClassDevs, byref(self.guid), None, None, flags)

		sp_device_interface_data = SpDeviceInterfaceData()
		sp_device_interface_data.cb_size = sizeof(sp_device_interface_data)
		sp_device_interface_detail_data = SpDeviceInterfaceDetailData()
		sp_device_info_data = SpDevinfoData()
		sp_device_info_data.cb_size = sizeof(sp_device_info_data)
		i = 0
		required_size = c_ulong(0)
		member_index = DWORD(i)

		while self.api.exec_function_setupapi(SetupDiEnumDeviceInterfaces , self.handle, None, byref(self.guid), member_index, byref(sp_device_interface_data)):
			self.api.exec_function_setupapi(SetupDiGetDeviceInterfaceDetail, self.handle, byref(sp_device_interface_data), None, 0, byref(required_size), None)
			resize(sp_device_interface_detail_data, required_size.value)
			sp_device_interface_detail_data.cb_size = sizeof(SpDeviceInterfaceDetailData) - sizeof(WCHAR * 1)
			if self.api.exec_function_setupapi(SetupDiGetDeviceInterfaceDetail, self.handle, byref(sp_device_interface_data), byref(sp_device_interface_detail_data), required_size, byref(required_size), byref(sp_device_info_data)):
				path = wstring_at(byref(sp_device_interface_detail_data, sizeof(DWORD)))
				self.device_paths.append(path)
			i += 1
		member_index = DWORD(i)
		required_size = c_ulong(0)
		resize(sp_device_interface_detail_data, sizeof(SpDeviceInterfaceDetailData))
		return len(self.device_paths) > 0
	

	def find_device(self, vid, pid):
		for i in range(len(self.device_paths)):
			if is_device(vid, pid, self.device_paths[i]) == True:
				return True
		return False


	def init_winusb_device(self, vid, pid):
		for i in range(len(self.device_paths)):
			if is_device(vid, pid, self.device_paths[i]) == True:
				self.handle_file = self.api.exec_function_kernel32(CreateFileW, self.device_paths[i], GENERIC_WRITE|GENERIC_READ, FILE_SHARE_WRITE|FILE_SHARE_READ, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL|FILE_FLAG_OVERLAPPED, None)

				if self.handle_file == INVALID_HANDLE_VALUE:
					return False
				result = self.api.exec_function_winusb(WinUsb_Initialize, self.handle_file, byref(self.handle_winusb))
				if result == 0:
					return False
				else:
					return True		
		return False


	def close_winusb_device(self):
		result_file = self.api.exec_function_kernel32(Close_Handle, self.handle_file)
		result_winusb = self.api.exec_function_winusb(WinUsb_Free, self.handle_winusb)
		return result_file != 0 and result_winusb != 0

	def get_last_error_code(self):
		return self.api.exec_function_kernel32(GetLastError)

	def query_device_info(self):
		return 0

	def query_interface_settings(self, index):
		return 0


