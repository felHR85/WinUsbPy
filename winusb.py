from ctypes import *
from winusberror import WinUSBError

class WinUSBApi:
	""" Facade class wrapping USB libraray WinUSB"""
	_WinUsb_Initialize = "WinUsb_Initialize"
	_WinUsb_ControlTransfer = "WinUsb_ControlTransfer"
	_WinUsb_GetDescriptor = "WinUsb_GetDescriptor"
	_WinUsb_ReadPipe = "WinUsb_ReadPipe"
	_WinUsb_WritePipe = "WinUsb_WritePipe"
	_WinUsb_Free = "WinUsb_Free"
	_WinUsb_QueryDeviceInformation = "WinUsb_QueryDeviceInformation"
	_WinUsb_QueryInterfaceSettings = "WinUsb_QueryInterfaceSettings"
	_WinUsb_QueryPipe = "WinUsb_QueryPipe"
	_WinUsb_ControlTransfer = "WinUsb_ControlTransfer"
	_Kernel32_Close_Handle = "CloseHandle"


	def __init__(self):
		
		try:
			self._kernel32 = windll.kernel32
		except WindowsError:
			raise WinUSBError("Kernel32 dll is not present. Are you in Windows?")

		try:
			self._windll = windll.winusb
		except WindowsError:
			raise WinUSBError("WinUsb dll is not present")

		# Functions availabe from WinUsb dll
		self._winusb_functions = {}
		self._winusb_functions[self._WinUsb_Initialize] = self._windll.WinUsb_Initialize
		self._winusb_functions[self._WinUsb_ControlTransfer] = self._windll.WinUsb_ControlTransfer
		self._winusb_functions[self._WinUsb_GetDescriptor] = self._windll.WinUsb_GetDescriptor
		self._winusb_functions[self._WinUsb_ReadPipe] = self._windll.WinUsb_ReadPipe
		self._winusb_functions[self._WinUsb_WritePipe] = self._windll.WinUsb_WritePipe
		self._winusb_functions[self._WinUsb_Free] = self._windll.WinUsb_Free
		self._winusb_functions[self._WinUsb_QueryDeviceInformation] = self._windll.WinUsb_QueryDeviceInformation
		self._winusb_functions[self._WinUsb_QueryInterfaceSettings] = self._windll.WinUsb_QueryInterfaceSettings
		self._winusb_functions[self._WinUsb_ControlTransfer] = self._windll._WinUsb_ControlTransfer

		# Functions needed from Kernel32 dll
		self._kernel32_functions = {}
		self._kernel32[self._Kernel32_Close_Handle] = self._kernel32.CloseHandle


		



		







