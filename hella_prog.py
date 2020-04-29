#!/usr/bin/python3

import can
import time
import datetime
import sys

now = datetime.datetime.now()

#interface = can.interfaces.socketcan.SocketcanBus('slcan0')
#interface = can.interfaces.slcan.slcanbBus('/dev/ttyACM0', bitrate=500000)

class hella_prog:
    def __init__(self, channel, interface):
        self.interface = can.interface.Bus(channel=channel, interface=interface, bitrate=500000,  ttyBaudrate=128000)
        self.msg_req = can.Message(extended_id=False,arbitration_id=0x3F0,data=bytearray([0x49,0x00,0x00,0x00,0x00,0x00,0x00,0x00]))
    
    def readmemory(self):
        self.interface.send(self.msg_req)
        answer = self.interface.recv(1)
        with open(now.strftime('%Y%m%d-%H%M%S.bin'),'wb') as fn:
            for n in range(128):
                while answer is not None and answer.arbitration_id != 0x3EB and answer.data[7] != 0x53:
                    answer = self.interface.recv(1)
                msg = can.Message(extended_id=False,arbitration_id=0x3F0,data=bytearray([0x31,0x0C,n,0x00,0x00,0x00,0x00,0x00]))
                self.interface.send(msg)
                answer = self.interface.recv(1)
                while answer is not None:
                    if answer.arbitration_id == 0x3E8:
                        print('%02X: %02X'%(n,answer.data[0]))
                        sys.stdout.flush()
                        fn.write(bytes([answer.data[0]]))
                        break
                    answer = self.interface.recv(1)
    
    def readmax(self):
        self.interface.send(self.msg_req)
        answer = self.interface.recv(1)
        if True:
            for n in [5,6]:
                firstanswer = int(answer.data[0])
                while answer is not None and answer.arbitration_id != 0x3EB and answer.data[7] != 0x53:
                    answer = self.interface.recv(1)
                msg = can.Message(extended_id=False,arbitration_id=0x3F0,data=bytearray([0x31,0x0C,n,0x00,0x00,0x00,0x00,0x00]))
                self.interface.send(msg)
                answer = self.interface.recv(1)
                while answer is not None:
                    if answer.arbitration_id == 0x3E8:
                        break
                    answer = self.interface.recv(1)
            retval = (firstanswer * 256 + int(answer.data[0]))
            while answer is not None:
                answer = self.interface.recv(1)
            return retval

    def readmin(self):
        self.interface.send(self.msg_req)
        answer = self.interface.recv(1)
        if True:
            for n in [3,4]:
                firstanswer = int(answer.data[0])
                while answer is not None and answer.arbitration_id != 0x3EB and answer.data[7] != 0x53:
                    answer = self.interface.recv(1)
                msg = can.Message(extended_id=False,arbitration_id=0x3F0,data=bytearray([0x31,0x0C,n,0x00,0x00,0x00,0x00,0x00]))
                self.interface.send(msg)
                answer = self.interface.recv(1)
                while answer is not None:
                    if answer.arbitration_id == 0x3E8:
                        break
                    answer = self.interface.recv(1)
            retval = (firstanswer * 256 + int(answer.data[0]))
            while answer is not None:
                answer = self.interface.recv(1)
            return retval

    def readminmax(self):
        self.interface.send(self.msg_req)
        answer = self.interface.recv(1)
        if True:
            addr = [3,4,0x22]
            answers = [0]*len(addr)
            for n in range(len(addr)):
                while answer is not None and answer.arbitration_id != 0x3EB and answer.data[7] != 0x53:
                    answer = self.interface.recv(1)
                msg = can.Message(extended_id=False,arbitration_id=0x3F0,data=bytearray([0x31,0x0C,addr[n],0x00,0x00,0x00,0x00,0x00]))
                self.interface.send(msg)
                answer = self.interface.recv(1)
                while answer is not None:
                    if answer.arbitration_id == 0x3E8:
                        answers[n]=answer.data[0]
                        break
                    answer = self.interface.recv(1)
            while answer is not None:
                answer = self.interface.recv(1)
        return [answers[0]*256+answers[1],answers[0]*256+answers[1]+answers[2]*4]

    def recv(self, timeout):
        answer = self.interface.recv(timeout)
        if answer is not None:
            print(answer.arbitration_id)
            sys.stdout.flush()
        return answer

    def set_max(self, pos):
        x = (int(pos)>>8)&0xFF
        y = (int(pos)&0xFF)
        z = 99#255 - int((int(pos)/1024)*255)
        print(('%X ')*3%(x,y,z))
        
        msg = can.Message(extended_id=False,arbitration_id=0x3F0,data=bytearray([0x31,0x0C,0x00,0x00,0x00,0x00,0x00,0x00]))
        msgs = [
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x01, 0x5D, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x2D, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, x, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, y, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x2D, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x8D, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, z, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x8D, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x23, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x01, 0x5D, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
        ]
        for item in msgs:
            msg.data = item
            self.interface.send(msg)
            time.sleep(0.02)
        answer = self.interface.recv(1)
        while answer is not None:
            answer = self.interface.recv(1)
    
    def set_min(self, pos):
        x = (int(pos)>>8)&0xFF
        y = (int(pos)&0xFF)
        z = 99#255 - int((int(pos)/1024)*255)
        msg = can.Message(extended_id=False,arbitration_id=0x3F0,data=bytearray([0x31,0x0C,0x00,0x00,0x00,0x00,0x00,0x00]))
        msgs = [
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x01, 0x5D, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x2D, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, x, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, y, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x2D, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x8D, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, z, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x8D, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x23, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x01, 0x5D, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
        ]
        for item in msgs:
            msg.data = item
            self.interface.send(msg)
            time.sleep(0.02)
        answer = self.interface.recv(1)
        while answer is not None:
            answer = self.interface.recv(1)
    
    def set_minmax(self, minpos, maxpos):
        x = (int(minpos)>>8)&0xFF
        y = (int(minpos)&0xFF)
        z = int((maxpos-minpos)/4)
        msg = can.Message(extended_id=False,arbitration_id=0x3F0,data=bytearray([0x31,0x0C,0x00,0x00,0x00,0x00,0x00,0x00]))
        msgs = [
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x01, 0x5D, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x2D, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, x, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, y, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x2D, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x8D, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, z, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x8D, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x0C, 0x23, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x01, 0x5D, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x57, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x31, 0x00, 0x94, 0x00, 0x00, 0x00, 0x00, 0x00]),
            bytearray([0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
        ]
        for item in msgs:
            msg.data = item
            self.interface.send(msg)
            time.sleep(0.02)
        answer = self.interface.recv(1)
        while answer is not None:
            answer = self.interface.recv(1)

    def find_end_positions(self):
        msg = can.Message(extended_id=False,arbitration_id=0x3F0,data=bytearray([0x31,0x0C,0x00,0x00,0x00,0x00,0x00,0x00]))
        msgs1 = [
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,1,93,0,0,0,0,0]),
            bytearray([87,0,0,5,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,1,99,0,0,0,0,0]),
            bytearray([87,0,0,40,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,0,128,0,0,0,0,0]),
            bytearray([87,0,0,1,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,1,97,0,0,0,0,0]),
            bytearray([87,0,0,1,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([68,0,0,0,0,0,0,0]),
            ]
        msgs2 = [
            bytearray([49,1,97,0,0,0,0,0]),
            bytearray([87,0,0,0,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,0,128,0,0,0,0,0]),
            bytearray([87,0,0,0,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,1,97,0,0,0,0,0]),
            bytearray([87,0,0,1,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([68,0,0,0,0,0,0,0]),
            ]
        msgs3 = [
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,1,97,0,0,0,0,0]),
            bytearray([87,0,0,0,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([49,1,93,0,0,0,0,0]),
            bytearray([87,0,0,2,0,0,0,0]),
            bytearray([49,0,148,0,0,0,0,0]),
            bytearray([68,0,0,0,0,0,0,0]),
            ]
        self.interface.send(self.msg_req)
        time.sleep(1)
        for item in msgs1:
            msg.data = item
            self.interface.send(msg)
            time.sleep(0.02)
        time.sleep(2)
        self.interface.send(self.msg_req)
        answer = self.interface.recv(1)
        while answer is not None:
            if answer.arbitration_id == 0x3EA:
                print('%02X%02X'%(answer.data[5],answer.data[6]))
            answer = self.interface.recv(1)
        for item in msgs2:
            msg.data = item
            self.interface.send(msg)
            time.sleep(0.02)
        time.sleep(2)
        self.interface.send(self.msg_req)
        answer = self.interface.recv(1)
        while answer is not None:
            if answer.arbitration_id == 0x3EA:
                print('%02X%02X'%(answer.data[5],answer.data[6]))
            answer = self.interface.recv(1)
        for item in msgs3:
            msg.data = item
            self.interface.send(msg)
            time.sleep(0.02)
        self.interface.send(self.msg_req)
        time.sleep(1)
    
    def readCurrentPosition(self):
        self.interface.send(self.msg_req)
        answer = self.interface.recv(1)
        self.interface.send(self.msg_req)
        while answer is not None:
            if answer.arbitration_id == 0x3EA:
                print('%02X%02X'%(answer.data[5],answer.data[6]))
            answer = self.interface.recv(1)
    
    def shutdown(self):
        self.interface.shutdown()

if __name__ == "__main__":
    hp = hella_prog('vcan0', 'socketcan')

    #set_max(0x0220)
    #set_max(0x033D)
    #set_min(0x0113)
    #set_min(0x01FF)
    hp.readmemory()
    
    #hp.find_end_positions()


# vim: et:sw=4:ts=4:smarttab:foldmethod=indent:si
