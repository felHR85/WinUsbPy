from ctypes import *
from ctypes.wintypes import *
from winusberror import WinUSBError
from winusbutils import *

class WinUSBApi(object):
	""" Facade class wrapping USB library WinUSB"""

	""" Windows functions names """
	WinUsb_Initialize = "WinUsb_Initialize"
	WinUsb_ControlTransfer = "WinUsb_ControlTransfer"
	WinUsb_GetDescriptor = "WinUsb_GetDescriptor"
	WinUsb_ReadPipe = "WinUsb_ReadPipe"
	WinUsb_WritePipe = "WinUsb_WritePipe"
	WinUsb_Free = "WinUsb_Free"
	WinUsb_QueryDeviceInformation = "WinUsb_QueryDeviceInformation"
	WinUsb_QueryInterfaceSettings = "WinUsb_QueryInterfaceSettings"
	WinUsb_QueryPipe = "WinUsb_QueryPipe"
	WinUsb_ControlTransfer = "WinUsb_ControlTransfer"
	Close_Handle = "CloseHandle"
	CreateFileW = "CreateFileW"
	ReadFile = "ReadFile"
	CancelIo  = "CancelIo"
	WriteFile = "WriteFile"
	SetEvent  = "SetEvent"
	WaitForSingleObject = "WaitForSingleObject"
	SetupDiGetClassDevs  = "SetupDiGetClassDevs"
	SetupDiEnumDeviceInterfaces = "SetupDiEnumDeviceInterfaces"
	SetupDiGetDeviceInterfaceDetail = "SetupDiGetDeviceInterfaceDetail"


	def __init__(self):

		try:
			self._kernel32 = windll.kernel32
		except WindowsError:
			raise WinUSBError("Kernel32 dll is not present. Are you in Windows?")

		try:
			self._windll = windll.winusb
		except WindowsError:
			raise WinUSBError("WinUsb dll is not present")

		try:
			self._setupapi = windll.SetupApi
		except WindowsError:
			raise WinUSBError("SetupApi dll is not present")

		self._winusb_functions_dict = get_winusb_functions()
		self._kernel32_functions_dict = get_kernel32_functions()

		"""Functions needed from SetupApi dll"""
		# TODO Refactor setupapi to winusbutils
		self._setupapi_functions = {}
		self._setupapi_restypes = {}
		self._setupapi_argtypes = {}

		#HDEVINFO SetupDiGetClassDevs(_In_opt_ const GUID *ClassGuid,_In_opt_ PCTSTR Enumerator,_In_opt_ HWND hwndParent,_In_ DWORD Flags);
		self._setupapi_functions[self.SetupDiGetClassDevs] = self._setupapi.SetupDiGetClassDevs
		self._setupapi_restypes = c_void_p
		self._setupapi_argtypes = [GUID, c_wchar_p, HANDLE, DWORD]

		#
		self._setupapi_functions[self.SetupDiEnumDeviceInterfaces] = self._setupapi.SetupDiEnumDeviceInterfaces
		self._setupapi_functions[self.SetupDiGetDeviceInterfaceDetail] = self._setupapi.SetupDiGetDeviceInterfaceDetail



	def exec_function_winusb(self, function=None, **kwargs):
		function_caller = _configure_ctype_function(self._winusb_functions, function)
		return True

	def exec_function_kernel32(self, function=None, **kwargs):
		function_caller = _configure_ctype_function(self._kernel32_functions, function)
		return True

	def exec_function_setupapi(self, function=None, **kwargs):
		function_caller = _configure_ctype_function(self._setupapi_functions, function)
		return True

	def _configure_ctype_function(self, dll_dict_functions, function=None):
		def _function_caller(**kwargs):
			win_function = dll_dict_functions[function]

			
			return True
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

	




		



		







