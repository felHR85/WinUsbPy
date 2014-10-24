from ctypes import *
from ctypes.wintypes import *
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

		""" Functions availabe from WinUsb dll and their types"""
		self._winusb_functions = {}
		self._winusb_restypes = {}
		self._winusb_argtypes = {}

		# BOOL __stdcall WinUsb_Initialize( _In_ HANDLE DeviceHandle,_Out_  PWINUSB_INTERFACE_HANDLE InterfaceHandle);
		self._winusb_functions[self.WinUsb_Initialize] = self._windll.WinUsb_Initialize
		self._winusb_restypes[self.WinUsb_Initialize] = BOOL
		self._winusb_argtypes[self.WinUsb_Initialize] = [HANDLE, c_void_p]

		#BOOL __stdcall WinUsb_ControlTransfer(_In_ WINUSB_INTERFACE_HANDLE InterfaceHandle,_In_ WINUSB_SETUP_PACKET SetupPacket, _Out_ PUCHAR Buffer,_In_ ULONG BufferLength,_Out_opt_  PULONG LengthTransferred,_In_opt_  LPOVERLAPPED Overlapped);
		self._winusb_functions[self.WinUsb_ControlTransfer] = self._windll.WinUsb_ControlTransfer
		self._winusb_restypes[self.WinUsb_ControlTransfer] = BOOL
		self._winusb_argtypes[self.WinUsb_ControlTransfer] = [c_void_p, UsbSetupPacket, pointer(c_ubyte), c_ulong, pointer(c_ulong), LpOverlapped] 

		#BOOL __stdcall WinUsb_GetDescriptor(_In_ WINUSB_INTERFACE_HANDLE InterfaceHandle,_In_ UCHAR DescriptorType,_In_ UCHAR Index,_In_ USHORT LanguageID,_Out_ PUCHAR Buffer,_In_ ULONG BufferLength,_Out_ PULONG LengthTransferred);
		self._winusb_functions[self.WinUsb_GetDescriptor] = self._windll.WinUsb_GetDescriptor
		self._winusb_restypes[self.WinUsb_GetDescriptor] = BOOL
		self._winusb_argtypes[self.WinUsb_GetDescriptor] = [c_void_p, c_ubyte, c_ubyte, c_ushort, pointer(c_ubyte), c_ulong, pointer(c_ulong)]

		#BOOL __stdcall WinUsb_ReadPipe( _In_ WINUSB_INTERFACE_HANDLE InterfaceHandle,_In_ UCHAR PipeID,_Out_ PUCHAR Buffer,_In_ ULONG BufferLength,_Out_opt_ PULONG LengthTransferred,_In_opt_ LPOVERLAPPED Overlapped);
		self._winusb_functions[self.WinUsb_ReadPipe] = self._windll.WinUsb_ReadPipe
		self._winusb_restypes[self.WinUsb_ReadPipe] = BOOL
		self._winusb_argtypes[self.WinUsb_ReadPipe] = [c_void_p, c_ubyte, pointer(c_ubyte), c_ulong, pointer(c_ulong), LpOverlapped]

		#BOOL __stdcall WinUsb_WritePipe(_In_ WINUSB_INTERFACE_HANDLE InterfaceHandle,_In_ UCHAR PipeID,_In_ PUCHAR Buffer,_In_ ULONG BufferLength,_Out_opt_  PULONG LengthTransferred,_In_opt_ LPOVERLAPPED Overlapped);
		self._winusb_functions[self.WinUsb_WritePipe] = self._windll.WinUsb_WritePipe
		self._winusb_restypes[self.WinUsb_WritePipe] = BOOL
		self._winusb_argtypes[self.WinUsb_WritePipe] = [c_void_p, c_ubyte, pointer(c_ubyte), c_ulong, pointer(c_ulong), LpOverlapped]

		#BOOL __stdcall WinUsb_Free(_In_ WINUSB_INTERFACE_HANDLE InterfaceHandle);
		self._winusb_functions[self.WinUsb_Free] = self._windll.WinUsb_Free
		self._winusb_restypes[self.WinUsb_Free] = BOOL
		self._winusb_argtypes[self.WinUsb_Free] = [c_void_p]

		#BOOL __stdcall WinUsb_QueryDeviceInformation(_In_ WINUSB_INTERFACE_HANDLE InterfaceHandle,_In_ ULONG InformationType,_Inout_ PULONG BufferLength,_Out_ PVOID Buffer);
		self._winusb_functions[self.WinUsb_QueryDeviceInformation] = self._windll.WinUsb_QueryDeviceInformation
		self._winusb_restypes = BOOL
		self._winusb_argtypes = [c_void_p, c_ulong, pointer(c_ulong), c_void_p]

		#BOOL __stdcall WinUsb_QueryInterfaceSettings(_In_ WINUSB_INTERFACE_HANDLE InterfaceHandle,_In_ UCHAR AlternateSettingNumber,_Out_ PUSB_INTERFACE_DESCRIPTOR UsbAltInterfaceDescriptor);
		self._winusb_functions[self.WinUsb_QueryInterfaceSettings] = self._windll.WinUsb_QueryInterfaceSettings
		self._winusb_restypes[self.WinUsb_QueryInterfaceSettings] = BOOL
		self._winusb_argtypes[self.WinUsb_QueryInterfaceSettings] = [c_void_p, c_ubyte, UsbInterfaceDescriptor]

		"""Functions needed from Kernel32 dll and their types"""
		self._kernel32_functions = {}
		self._kernel32_functions[self.Close_Handle] = self._kernel32.CloseHandle
		self._kernel32_functions[self.ReadFile] = self._kernel32.ReadFile
		self._kernel32_functions[self.CancelIo] = self._kernel32.CancelIo
		self._kernel32_functions[self.WriteFile] = self._kernel32.WriteFile
		self._kernel32_functions[self.SetEvent] = self._kernel32.SetEvent
		self._kernel32_functions[self.WaitForSingleObject] = self._kernel32.WaitForSingleObject
		self._kernel32_functions[self.CreateFileW] = self._kernel32.CreateFileW 

		"""Functions needed from SetupApi dll"""
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
	




		



		







