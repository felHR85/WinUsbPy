from ctypes import *
from ctypes.wintypes import *
from winusberror import WinUSBError
from winusbutils import *

class WinUSBApi(object):
	""" Facade class wrapping USB library WinUSB"""

	def __init__(self):

		try:
			self._kernel32 = windll.kernel32
		except WindowsError:
			raise WinUSBError("Kernel32 dll is not present. Are you really using Windows?")

		try:
			self._winusb = windll.winusb
		except WindowsError:
			raise WinUSBError("WinUsb dll is not present")

		try:
			self._setupapi = windll.SetupApi
		except WindowsError:
			raise WinUSBError("SetupApi dll is not present")

		self._winusb_functions_dict = get_winusb_functions(self._winusb)
		self._kernel32_functions_dict = get_kernel32_functions(self._kernel32)
		self._setupapi_functions_dict = get_setupapi_functions(self._setupapi)


	def exec_function_winusb(self, function_name=None, *args):
		function_caller = _configure_ctype_function(self._winusb_functions, function_name)
		return function_caller(kwargs)

	def exec_function_kernel32(self, function_name=None, *args):
		function_caller = _configure_ctype_function(self._kernel32_functions, function_name)
		return function_caller(kwargs)

	def exec_function_setupapi(self, function_name=None, *args):
		function_caller = _configure_ctype_function(self._setupapi_functions, function_name)
		return function_caller(kwargs)

	def _configure_ctype_function(self, dll_dict_functions, function_name=None):
		def _function_caller(*args):
			function = dll_dict_functions["functions"][function_name]
			function.restype = dll_dict_functions["restypes"][function_name]
			function.argtypes = dll_dict_functions["argtypes"][function_name]
			return function(*args)
		return _function_caller


class UsbSetupPacket(Structure):
	_fields_ = [("request_type", c_ubyte), ("request", c_ubyte),
				("value", c_ushort), ("index", c_ushort), ("length", c_ushort)]


""" LPOVERLAPPED still not defined. It will be NULL """
class LpOverlapped(Structure):
	_fields_ = []


class UsbInterfaceDescriptor(Structure):
	_fields_ = [("b_length",c_ubyte), ("b_descriptor_type",c_ubyte),
				("b_interface_number",c_ubyte), ("b_alternate_setting",c_ubyte),
				("b_num_endpoints",c_ubyte), ("b_interface_class",c_ubyte),
				("b_interface_sub_class",c_ubyte), ("b_interface_protocol",c_ubyte),
				("i_interface",c_ubyte)]


class LpSecurityAttributes(Structure):
	_fields_ = [("n_length", DWORD), ("lp_security_descriptor", c_void_p), 
			 	("b_Inherit_handle",BOOL)]


class GUID(Structure):
	_fields_ = [("data1", DWORD), ("data2", WORD),
				("data3", WORD), ("data4", c_byte)]


class PspDevinfoData(Structure):
	_fields_ = [("cb_size", DWORD), ("class_guid", GUID),
				("dev_inst", DWORD), ("reserved", c_ulong)]


class PspDeviceInterfaceData(Structure):
	_fields_ = [("cb_size", DWORD), ("interface_class_guid", GUID),
				("flags", DWORD), ("reserved", c_ulong)]


class Psp_Device_Interface_Detail_Data(Structure):
	_fields_ = [("cb_size", DWORD), ("device_path",c_ubyte)] #devicePath array
