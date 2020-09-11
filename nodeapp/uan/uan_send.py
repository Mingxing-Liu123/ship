#!/usr/bin/python

import uan_protocol
import socket

class UAN_Send:
    def send(fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM), packet = uan_protocol.UAN_Packet()):
        sendMsg = bytes()
        sendMsg = packet.toByte()
        print("sendmsg:",sendMsg)
        fd.send(sendMsg)

