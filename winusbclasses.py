from ctypes import *
from ctypes.wintypes import *

"""Flags controlling what is included in the device information set built by SetupDiGetClassDevs"""
DIGCF_DEFAULT = 0x00000001
DIGCF_PRESENT = 0x00000002
DIGCF_ALLCLASSES = 0x00000004
DIGCF_PROFILE = 0x00000008
DIGCF_DEVICE_INTERFACE = 0x00000010

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
				("data3", WORD), ("data4", c_byte * 8)]


class SpDevinfoData(Structure):
	_fields_ = [("cb_size", DWORD), ("class_guid", GUID),
				("dev_inst", DWORD), ("reserved", POINTER(c_ulong))]


class SpDeviceInterfaceData(Structure):
	_fields_ = [("cb_size", DWORD), ("interface_class_guid", GUID),
				("flags", DWORD), ("reserved", POINTER(c_ulong))]


class SpDeviceInterfaceDetailData(Structure):
	_fields_ = [("cb_size", DWORD), ("device_path",WCHAR * 1)] #devicePath array!!!