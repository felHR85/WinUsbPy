"""Test2: PL2303 serial port user-space driver using WINUSB high level api"""
import time
from winusbpy import *

pl2303_vid = "2309"
pl2303_pid = "0606"

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

""" USB Data """
hello = "Hello"
header = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x01\x08\x01\x00\x00\x08\x01\x00\x00\x08\x01\x00\x00\x08\x01\x00\x00\x08\x01\x00\x00\x08\x01\x00\x00\x08\x01\x00\x00"
tx1 = b"\x18"
tx2 = b"\x08"
tx3 = b"\x08"
tx4 = b"\x14"
tx5 = b"\x14"
tx6 = b"\x22"
tx7 = b"\x3e"
tx8 = b"\x22"
tx9 = b"\x77"
tx10 = b"\x00"
tx11 = b"\x00"
tx12 = b"\x00"

""" WinUsbPy  """

api = WinUsbPy()
result = api.list_usb_devices(deviceinterface=True, present=True)
if result:
    if api.init_winusb_device(pl2303_vid, pl2303_pid):
        speed = api.query_device_info(query=1)
        if speed != -1:
            print("Device Speed: " + str(speed))
        else:
            print("Device speed could not be obtained")

        interface_descriptor = api.query_interface_settings(0)

        if interface_descriptor != None:
            print("bLength: " + str(interface_descriptor.b_length))
            print("bDescriptorType: " + str(interface_descriptor.b_descriptor_type))
            print("bInterfaceNumber: " + str(interface_descriptor.b_interface_number))
            print("bAlternateSetting: " + str(interface_descriptor.b_alternate_setting))
            print("bNumEndpoints " + str(interface_descriptor.b_num_endpoints))
            print("bInterfaceClass " + str(interface_descriptor.b_interface_class))
            print("bInterfaceSubClass: " + str(interface_descriptor.b_interface_sub_class))
            print("bInterfaceProtocol: " + str(interface_descriptor.b_interface_protocol))
            print("iInterface: " + str(interface_descriptor.i_interface))

        pipe_info_list = map(api.query_pipe, range(interface_descriptor.b_num_endpoints))
        for item in pipe_info_list:
            print("PipeType: " + str(item.pipe_type))
            print("PipeId: " + str(item.pipe_id))
            print("MaximumPacketSize: " + str(item.maximum_packet_size))
            print("Interval: " + str(item.interval))

        """
        buff = None -> Buffer length will be zero. No data expected
        """
        api.control_transfer(pkt1, buff=[0])
        api.control_transfer(pkt2, buff=None)
        api.control_transfer(pkt3, buff=[0])
        api.control_transfer(pkt4, buff=[0])
        api.control_transfer(pkt5, buff=[0])
        api.control_transfer(pkt6, buff=None)
        api.control_transfer(pkt7, buff=[0])
        api.control_transfer(pkt8, buff=[0])
        api.control_transfer(pkt9, buff=None)
        api.control_transfer(pkt10, buff=None)
        api.control_transfer(pkt11, buff=None)
        api.control_transfer(pkt12, buff=None)
        api.control_transfer(pkt13, buff=[0xc0, 0x12, 0x00, 0x00, 0x00, 0x00, 0x08])
        api.control_transfer(pkt14, buff=None)
        api.control_transfer(pkt15, buff=None)
        api.control_transfer(pkt16, buff=None)
        api.control_transfer(pkt17, buff=None)
        api.control_transfer(pkt18, buff=[0, 0])
        api.control_transfer(pkt19, buff=[0, 0])
        api.control_transfer(pkt20, buff=None)

        api.write(0x02, hello)
        time.sleep(0.045)
        api.write(0x02, header)
        time.sleep(0.380)
        api.write(0x02, tx1)
        time.sleep(0.380)
        api.write(0x02, tx2)
        time.sleep(0.380)
        api.write(0x02, tx3)
        time.sleep(0.380)
        api.write(0x02, tx4)
        time.sleep(0.380)
        api.write(0x02, tx5)
        time.sleep(0.380)
        api.write(0x02, tx6)
        time.sleep(0.380)
        api.write(0x02, tx7)
        time.sleep(0.380)
        api.write(0x02, tx8)
        time.sleep(0.380)
        api.write(0x02, tx9)
        time.sleep(0.380)
        api.write(0x02, tx10)
        time.sleep(0.380)
        api.write(0x02, tx11)
        time.sleep(0.380)
        api.write(0x02, tx12)


    else:
        print("PL2303 could not be init")

else:
    print("No Usb devices connected")
