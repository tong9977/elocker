import serial
import libscrc
import config
import time

def onRelay(slaveID,chanel,delay):
    list_of_values = [slaveID, 0x06, 0x00, chanel, 0x06, delay]
    bytes_of_values = bytes(list_of_values)
    crc16 = libscrc.modbus(bytes_of_values)
    crc_lo = crc16 & 0x00ff
    crc_hi = (crc16 & 0xff00) >> 8

    ser = serial.Serial()
    ser.port = config.comport
    ser.baudrate = 9600
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.open()
    ser.write(serial.to_bytes([slaveID, 0x06, 0x00, chanel, 0x06, delay, crc_lo, crc_hi]))
    ser.close()


def openBox(boxNo):
    slaveID = config.boxMap[boxNo][0]
    chanel = config.boxMap[boxNo][1]
    onRelay(slaveID,chanel,config.delaySec)

def openAll():
    for i in range(1,49,1):
        print(i)
        openBox(i)
        time.sleep(2)