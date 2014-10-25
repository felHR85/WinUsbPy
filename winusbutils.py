from ctypes.wintypes import *

def get_winusb_functions():
	""" Functions availabe from WinUsb dll and their types"""
	winusb_dict = {}
	winusb_functions = {}
	winusb_restypes = {}
	winusb_argtypes = {}

	# BOOL __stdcall WinUsb_Initialize( _In_ HANDLE DeviceHandle,_Out_  PWINUSB_INTERFACE_HANDLE InterfaceHandle);
	winusb_functions[self.WinUsb_Initialize] = self._windll.WinUsb_Initialize
	winusb_restypes[self.WinUsb_Initialize] = BOOL
	winusb_argtypes[self.WinUsb_Initialize] = [HANDLE, c_void_p]

	#BOOL __stdcall WinUsb_ControlTransfer(_In_ WINUSB_INTERFACE_HANDLE InterfaceHandle,_In_ WINUSB_SETUP_PACKET SetupPacket, _Out_ PUCHAR Buffer,_In_ ULONG BufferLength,_Out_opt_  PULONG LengthTransferred,_In_opt_  LPOVERLAPPED Overlapped);
	winusb_functions[self.WinUsb_ControlTransfer] = self._windll.WinUsb_ControlTransfer
	winusb_restypes[self.WinUsb_ControlTransfer] = BOOL
	winusb_argtypes[self.WinUsb_ControlTransfer] = [c_void_p, UsbSetupPacket, pointer(c_ubyte), c_ulong, pointer(c_ulong), LpOverlapped] 

	#BOOL __stdcall WinUsb_GetDescriptor(_In_ WINUSB_INTERFACE_HANDLE InterfaceHandle,_In_ UCHAR DescriptorType,_In_ UCHAR Index,_In_ USHORT LanguageID,_Out_ PUCHAR Buffer,_In_ ULONG BufferLength,_Out_ PULONG LengthTransferred);
	winusb_functions[self.WinUsb_GetDescriptor] = self._windll.WinUsb_GetDescriptor
	winusb_restypes[self.WinUsb_GetDescriptor] = BOOL
	winusb_argtypes[self.WinUsb_GetDescriptor] = [c_void_p, c_ubyte, c_ubyte, c_ushort, pointer(c_ubyte), c_ulong, pointer(c_ulong)]

	#BOOL __stdcall WinUsb_ReadPipe( _In_ WINUSB_INTERFACE_HANDLE InterfaceHandle,_In_ UCHAR PipeID,_Out_ PUCHAR Buffer,_In_ ULONG BufferLength,_Out_opt_ PULONG LengthTransferred,_In_opt_ LPOVERLAPPED Overlapped);
	winusb_functions[self.WinUsb_ReadPipe] = self._windll.WinUsb_ReadPipe
	winusb_restypes[self.WinUsb_ReadPipe] = BOOL
	winusb_argtypes[self.WinUsb_ReadPipe] = [c_void_p, c_ubyte, pointer(c_ubyte), c_ulong, pointer(c_ulong), LpOverlapped]

	#BOOL __stdcall WinUsb_WritePipe(_In_ WINUSB_INTERFACE_HANDLE InterfaceHandle,_In_ UCHAR PipeID,_In_ PUCHAR Buffer,_In_ ULONG BufferLength,_Out_opt_  PULONG LengthTransferred,_In_opt_ LPOVERLAPPED Overlapped);
	winusb_functions[self.WinUsb_WritePipe] = self._windll.WinUsb_WritePipe
	winusb_restypes[self.WinUsb_WritePipe] = BOOL
	winusb_argtypes[self.WinUsb_WritePipe] = [c_void_p, c_ubyte, pointer(c_ubyte), c_ulong, pointer(c_ulong), LpOverlapped]

	#BOOL __stdcall WinUsb_Free(_In_ WINUSB_INTERFACE_HANDLE InterfaceHandle);
	winusb_functions[self.WinUsb_Free] = self._windll.WinUsb_Free
	winusb_restypes[self.WinUsb_Free] = BOOL
	winusb_argtypes[self.WinUsb_Free] = [c_void_p]

	#BOOL __stdcall WinUsb_QueryDeviceInformation(_In_ WINUSB_INTERFACE_HANDLE InterfaceHandle,_In_ ULONG InformationType,_Inout_ PULONG BufferLength,_Out_ PVOID Buffer);
	winusb_functions[self.WinUsb_QueryDeviceInformation] = self._windll.WinUsb_QueryDeviceInformation
	winusb_restypes = BOOL
	winusb_argtypes = [c_void_p, c_ulong, pointer(c_ulong), c_void_p]

	#BOOL __stdcall WinUsb_QueryInterfaceSettings(_In_ WINUSB_INTERFACE_HANDLE InterfaceHandle,_In_ UCHAR AlternateSettingNumber,_Out_ PUSB_INTERFACE_DESCRIPTOR UsbAltInterfaceDescriptor);
	winusb_functions[self.WinUsb_QueryInterfaceSettings] = self._windll.WinUsb_QueryInterfaceSettings
	winusb_restypes[self.WinUsb_QueryInterfaceSettings] = BOOL
	winusb_argtypes[self.WinUsb_QueryInterfaceSettings] = [c_void_p, c_ubyte, UsbInterfaceDescriptor]

	winusb_dict["functions"] = winusb_functions 
	winusb_dict["restypes"] = winusb_restypes
	winusb_dict["argtypes"] = winusb_argtypes
	return winusb_dict

def get_kernel32_functions():
	kernel32_dict = {}
	kernel32_functions = {}
	kernel32_restypes = {}
	kernel32_argtypes = {}

	#BOOL WINAPI CloseHandle(_In_  HANDLE hObject);
	kernel32_functions[self.Close_Handle] = self._kernel32.CloseHandle
	kernel32_restypes[self.Close_Handle] = BOOL
	kernel32_argtypes[self.Close_Handle] = [HANDLE]

	#BOOL WINAPI ReadFile(_In_ HANDLE hFile,_Out_ LPVOID lpBuffer,_In_ DWORD nNumberOfBytesToRead,_Out_opt_ LPDWORD lpNumberOfBytesRead,_Inout_opt_ LPOVERLAPPED lpOverlapped);
	kernel32_functions[self.ReadFile] = self._kernel32.ReadFile
	kernel32_restypes[self.ReadFile] = BOOL
	kernel32_argtypes[self.ReadFile] = [HANDLE, c_void_p, DWORD, pointer(DWORD), LpOverlapped]

	#BOOL WINAPI CancelIo(_In_  HANDLE hFile);
	kernel32_functions[self.CancelIo] = self._kernel32.CancelIo
	kernel32_restypes[self.CancelIo] = BOOL
	kernel32_argtypes[self.CancelIo] = [HANDLE]

	#BOOL WINAPI WriteFile(_In_ HANDLE hFile,_In_ LPCVOID lpBuffer,_In_ DWORD nNumberOfBytesToWrite,_Out_opt_ LPDWORD lpNumberOfBytesWritten,_Inout_opt_  LPOVERLAPPED lpOverlapped);
	kernel32_functions[self.WriteFile] = self._kernel32.WriteFile
	kernel32_restypes[self.WriteFile] = BOOL
	kernel32_argtypes[self.WriteFile] = [HANDLE, c_void_p, DWORD, pointer(DWORD), LpOverlapped]

	#BOOL WINAPI SetEvent(_In_ HANDLE hEvent);
	kernel32_functions[self.SetEvent] = self._kernel32.SetEvent
	kernel32_restypes[self.SetEvent] = BOOL
	kernel32_argtypes[self.SetEvent] = [HANDLE]

	#DWORD WINAPI WaitForSingleObject(_In_ HANDLE hHandle, _In_  DWORD dwMilliseconds);
	kernel32_functions[self.WaitForSingleObject] = self._kernel32.WaitForSingleObject
	kernel32_restypes[self.WaitForSingleObject] = DWORD
	kernel32_argtypes[self.WaitForSingleObject] = [HANDLE, DWORD]

	#HANDLE WINAPI CreateFile(_In_ LPCTSTR lpFileName,_In_ DWORD dwDesiredAccess,_In_ DWORD dwShareMode,_In_opt_ LPSECURITY_ATTRIBUTES lpSecurityAttributes,_In_ DWORD dwCreationDisposition,_In_ DWORD dwFlagsAndAttributes,_In_opt_ HANDLE hTemplateFile);
	kernel32_functions[self.CreateFileW] = self._kernel32.CreateFileW 
	kernel32_restypes[self.CreateFileW] = HANDLE
	kernel32_argtypes[self.CreateFileW] = [c_wchar_p, DWORD, DWORD, LpSecurityAttributes, DWORD, DWORD, HANDLE]

	kernel32_dict["functions"] = kernel32_functions
	kernel32_dict["restypes"] = kernel32_restypes
	kernel32_dict["argtypes"] = kernel32_argtypes

	return kernel32_dict

