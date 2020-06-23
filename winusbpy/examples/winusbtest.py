"""Test1: PL2303 serial port user-space driver using WINUSB low level api"""
import time
from winusbpy import *
from ctypes import *
from ctypes.wintypes import *
from ..winusbclasses import DIGCF_DEVICE_INTERFACE, DIGCF_PRESENT, GENERIC_WRITE, GENERIC_READ, FILE_SHARE_READ, \
    FILE_SHARE_WRITE, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, FILE_FLAG_OVERLAPPED, INVALID_HANDLE_VALUE

pl2303_vid = "067b"
pl2303_pid = "2303"
path = ""
interface_descriptor = UsbInterfaceDescriptor()

""" USB Setup Packets """
pkt1 = UsbSetupPacket(0xc0, 0x01, 0x8484, 0x00, 0x01)
pkt2 = UsbSetupPacket(0x40, 0x01, 0x0404, 0x00, 0x00)
pkt3 = UsbSetupPacket(0x40, 0x01, 0x0404, 0x00, 0x01)
pkt4 = UsbSetupPacket(0xc0, 0x01, 0x8383, 0x00, 0x01)
pkt5 = UsbSetupPacket(0xc0, 0x01, 0x8484, 0x00, 0x01)
pkt6 = UsbSetupPacket(0x40, 0x01, 0x0404, 0x01, 0x00)
pkt7 = UsbSetupPacket(0xc0, 0x01, 0x8484, 0x00, 0x01)
pkt8 = UsbSetupPacket(0xc0, 0x01, 0x8383, 0x00, 0x01)
pkt9 = UsbSetupPacket(0x40, 0x01, 0x0000, 0x01, 0x00)
pkt10 = UsbSetupPacket(0x40, 0x01, 0x0001, 0x00, 0x00)
pkt11 = UsbSetupPacket(0x40, 0x01, 0x0002, 0x44, 0x00)
pkt12 = UsbSetupPacket(0x00, 0x01, 0x0001, 0x00, 0x00)

pkt13 = UsbSetupPacket(0x21, 0x20, 0x0000, 0x00, 0x07)
pkt14 = UsbSetupPacket(0x40, 0x01, 0x0505, 0x1311, 0x00)
pkt15 = UsbSetupPacket(0x21, 0x22, 0x0001, 0x00, 0x00)
pkt16 = UsbSetupPacket(0x40, 0x01, 0x0505, 0x1311, 0x00)
pkt17 = UsbSetupPacket(0x21, 0x22, 0x0001, 0x00, 0x00)
pkt18 = UsbSetupPacket(0xc0, 0x01, 0x0080, 0x00, 0x02)
pkt19 = UsbSetupPacket(0xc0, 0x01, 0x0081, 0x00, 0x02)
pkt20 = UsbSetupPacket(0x40, 0x01, 0x0000, 0x01, 0x00)

""" USB Data"""
hello = create_string_buffer("Hello")
header = create_string_buffer(
    "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x01\x08\x01\x00\x00\x08\x01\x00\x00\x08\x01\x00\x00\x08\x01\x00\x00\x08\x01\x00\x00\x08\x01\x00\x00\x08\x01\x00\x00")
tx1 = create_string_buffer("\x18")
tx2 = create_string_buffer("\x08")
tx3 = create_string_buffer("\x08")
tx4 = create_string_buffer("\x14")
tx5 = create_string_buffer("\x14")
tx6 = create_string_buffer("\x22")
tx7 = create_string_buffer("\x3e")
tx8 = create_string_buffer("\x22")
tx9 = create_string_buffer("\x77")
tx10 = create_string_buffer("\x00")
tx11 = create_string_buffer("\x00")
tx12 = create_string_buffer("\x00")

api = WinUSBApi()
byte_array = c_byte * 8
guid = GUID(0xA5DCBF10, 0x6530, 0x11D2, byte_array(0x90, 0x1F, 0x00, 0xC0, 0x4F, 0xB9, 0x51, 0xED))
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
Enumerate all USB Devices Searching for a PL2303 device
"""
hdev_info = api.exec_function_setupapi("SetupDiGetClassDevs", byref(guid), None, None, flags)

while api.exec_function_setupapi("SetupDiEnumDeviceInterfaces", hdev_info, None, byref(guid), member_index,
                                 byref(sp_device_interface_data)):
    # Get the required buffer size and resize SpDeviceInterfaceDetailData
    api.exec_function_setupapi("SetupDiGetDeviceInterfaceDetail", hdev_info, byref(sp_device_interface_data), None, 0,
                               byref(required_size), None)
    resize(sp_device_interface_detail_data, required_size.value)

    """ I have been stuck here for hours. cb_size must reflect the fix part of the Struct!!!!"""
    sp_device_interface_detail_data.cb_size = sizeof(SpDeviceInterfaceDetailData) - sizeof(WCHAR * 1)

    if api.exec_function_setupapi("SetupDiGetDeviceInterfaceDetail", hdev_info, byref(sp_device_interface_data),
                                  byref(sp_device_interface_detail_data), required_size, byref(required_size),
                                  byref(sp_device_info_data)):
        path = wstring_at(byref(sp_device_interface_detail_data, sizeof(DWORD)))
        if is_device(pl2303_vid, pl2303_pid, path):
            print("PL 2303 PATH: " + path)
            break
    else:
        error_code = api.exec_function_kernel32("GetLastError")
        print("Error: " + str(error_code))

    i += 1
    member_index = DWORD(i)
    required_size = c_ulong(0)
    resize(sp_device_interface_detail_data, sizeof(SpDeviceInterfaceDetailData))

"""Open PL2303 Device"""
handle_file = api.exec_function_kernel32("CreateFileW", path, GENERIC_WRITE | GENERIC_READ,
                                         FILE_SHARE_WRITE | FILE_SHARE_READ, None, OPEN_EXISTING,
                                         FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OVERLAPPED, None)
if INVALID_HANDLE_VALUE == handle_file:
    print("Error Creating File")
else:
    print("No error")
    handle_winusb = c_void_p()
    result = api.exec_function_winusb("WinUsb_Initialize", handle_file, byref(handle_winusb))
    if result != 0:
        """ Get PL2303 Speed """
        info_type = c_ulong(1)
        buff = (c_void_p * 1)()
        buff_length = c_ulong(sizeof(c_void_p))

        result = api.exec_function_winusb("WinUsb_QueryDeviceInformation", handle_winusb, info_type, byref(buff_length),
                                          buff)
        if result != 0:
            print("Speed: " + str(buff[0]))

        else:
            error_code = api.exec_function_kernel32("GetLastError")
            print("Error Query Device: " + str(error_code))

        """ Interface Settings """
        response = api.exec_function_winusb("WinUsb_QueryInterfaceSettings", handle_winusb, c_ubyte(0),
                                            byref(interface_descriptor))

        if response == 0:
            error_code = api.exec_function_kernel32("GetLastError")
            print("Error Query Interface: " + str(error_code))
        if response != 0:
            print("bLength: " + str(interface_descriptor.b_length))
            print("bDescriptorType: " + str(interface_descriptor.b_descriptor_type))
            print("bInterfaceNumber: " + str(interface_descriptor.b_interface_number))
            print("bAlternateSetting: " + str(interface_descriptor.b_alternate_setting))
            print("bNumEndpoints " + str(interface_descriptor.b_num_endpoints))
            print("bInterfaceClass " + str(interface_descriptor.b_interface_class))
            print("bInterfaceSubClass: " + str(interface_descriptor.b_interface_sub_class))
            print("bInterfaceProtocol: " + str(interface_descriptor.b_interface_protocol))
            print("iInterface: " + str(interface_descriptor.i_interface))

            """ Endpoints information """
            i = 0
            endpoint_index = c_ubyte(0)
            pipe_info = PipeInfo()
            while i <= interface_descriptor.b_num_endpoints:
                result = api.exec_function_winusb("WinUsb_QueryPipe", handle_winusb, c_ubyte(0), endpoint_index,
                                                  byref(pipe_info))
                if result != 0:
                    print("PipeType: " + str(pipe_info.pipe_type))
                    print("PipeId: " + str(pipe_info.pipe_id))
                    print("MaximumPacketSize: " + str(pipe_info.maximum_packet_size))
                    print("Interval: " + str(pipe_info.interval))
                i += 1
                endpoint_index = c_ubyte(i)

            """ Control setup """
            buff1 = c_ubyte()
            buff2 = (c_ubyte * 2)()
            buff_set_line = (c_ubyte * 7)(0xc0, 0x12, 0x00, 0x00, 0x00, 0x00, 0x08)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt1, byref(buff1), c_ulong(1),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt2, byref(buff1), c_ulong(0),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt3, byref(buff1), c_ulong(1),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt4, byref(buff1), c_ulong(1),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt5, byref(buff1), c_ulong(1),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt6, byref(buff1), c_ulong(0),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt7, byref(buff1), c_ulong(1),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt8, byref(buff1), c_ulong(1),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt9, byref(buff1), c_ulong(0),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt10, byref(buff1), c_ulong(0),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt11, byref(buff1), c_ulong(0),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt12, byref(buff1), c_ulong(0),
                                     byref(c_ulong(0)), None)

            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt13, byref(buff_set_line), c_ulong(7),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt14, byref(buff1), c_ulong(0),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt15, byref(buff1), c_ulong(0),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt16, byref(buff1), c_ulong(0),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt17, byref(buff1), c_ulong(0),
                                     byref(c_ulong(0)), None)

            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt18, byref(buff2), c_ulong(1),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt19, byref(buff2), c_ulong(1),
                                     byref(c_ulong(0)), None)
            api.exec_function_winusb("WinUsb_ControlTransfer", handle_winusb, pkt20, byref(buff1), c_ulong(0),
                                     byref(c_ulong(0)), None)

            """ Send Data """
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), hello, c_ulong(5),
                                     byref(c_ulong(0)), None)
            time.sleep(0.045)
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), header, c_ulong(42),
                                     byref(c_ulong(0)), None)
            time.sleep(0.380)
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), tx1, c_ulong(1),
                                     byref(c_ulong(0)), None)
            time.sleep(0.380)
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), tx2, c_ulong(1),
                                     byref(c_ulong(0)), None)
            time.sleep(0.380)
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), tx3, c_ulong(1),
                                     byref(c_ulong(0)), None)
            time.sleep(0.380)
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), tx4, c_ulong(1),
                                     byref(c_ulong(0)), None)
            time.sleep(0.380)
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), tx5, c_ulong(1),
                                     byref(c_ulong(0)), None)
            time.sleep(0.380)
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), tx6, c_ulong(1),
                                     byref(c_ulong(0)), None)
            time.sleep(0.380)
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), tx7, c_ulong(1),
                                     byref(c_ulong(0)), None)
            time.sleep(0.380)
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), tx8, c_ulong(1),
                                     byref(c_ulong(0)), None)
            time.sleep(0.380)
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), tx9, c_ulong(1),
                                     byref(c_ulong(0)), None)
            time.sleep(0.380)
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), tx10, c_ulong(1),
                                     byref(c_ulong(0)), None)
            time.sleep(0.380)
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), tx11, c_ulong(1),
                                     byref(c_ulong(0)), None)
            time.sleep(0.380)
            api.exec_function_winusb("WinUsb_WritePipe", handle_winusb, c_ubyte(0x02), tx12, c_ulong(1),
                                     byref(c_ulong(0)), None)

    else:
        error_code = api.exec_function_kernel32("GetLastError")
        print("Error" + str(error_code))
