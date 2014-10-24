from ctypes import *
from winusberror import WinUSBError

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

		# Functions availabe from WinUsb dll
		self._winusb_functions = {}
		self._winusb_functions[self.WinUsb_Initialize] = self._windll.WinUsb_Initialize
		self._winusb_functions[self.WinUsb_ControlTransfer] = self._windll.WinUsb_ControlTransfer
		self._winusb_functions[self.WinUsb_GetDescriptor] = self._windll.WinUsb_GetDescriptor
		self._winusb_functions[self.WinUsb_ReadPipe] = self._windll.WinUsb_ReadPipe
		self._winusb_functions[self.WinUsb_WritePipe] = self._windll.WinUsb_WritePipe
		self._winusb_functions[self.WinUsb_Free] = self._windll.WinUsb_Free
		self._winusb_functions[self.WinUsb_QueryDeviceInformation] = self._windll.WinUsb_QueryDeviceInformation
		self._winusb_functions[self.WinUsb_QueryInterfaceSettings] = self._windll.WinUsb_QueryInterfaceSettings
		self._winusb_functions[self.WinUsb_ControlTransfer] = self._windll._WinUsb_ControlTransfer

		# Functions needed from Kernel32 dll
		self._kernel32_functions = {}
		self._kernel32_functions[self.Close_Handle] = self._kernel32.CloseHandle
		self._kernel32_functions[self.ReadFile] = self._kernel32.ReadFile
		self._kernel32_functions[self.CancelIo] = self._kernel32.CancelIo
		self._kernel32_functions[self.WriteFile] = self._kernel32.WriteFile
		self._kernel32_functions[self.SetEvent] = self._kernel32.SetEvent
		self._kernel32_functions[self.WaitForSingleObject] = self._kernel32.WaitForSingleObject
		self._kernel32_functions[self.CreateFileW] = self._kernel32.CreateFileW 

		# Functions needed from SetupApi dll
		self._setupapi_functions = {}
		self._setupapi_functions[self.SetupDiGetClassDevs] = self._setupapi.SetupDiGetClassDevs
		self._setupapi_functions[self.SetupDiEnumDeviceInterfaces] = self._setupapi.SetupDiEnumDeviceInterfaces
		self._setupapi_functions[self.SetupDiGetDeviceInterfaceDetail] = self._setupapi.SetupDiGetDeviceInterfaceDetail



	def exec_function_winusb(self, function=None, **kwargs):
		function_caller = _configure_ctype_function(self._winusb_functions, function)
		return True

	def exec_function_kernel32(self, function=None, **kwargs):
		return True

	def exec_function_setupapi(self, function=None, **kwargs):
		return True

	def _configure_ctype_function(self, dll_dict_functions, function=None):
		def _function_caller(**kwargs):
			win_function = dll_dict_functions[function]
			 
			
			return True
		return _function_caller




		



		







