import machine
from machine import Pin, ADC
import time
from datetime import datetime
import network
import socket

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('fbi', 'Personal') #change to wifi ssid and password
    while not wlan.isconnected():
        print("Connecting...")
        time.sleep(1)
    print(wlan.ifconfig())
    return wlan.ifconfig()[0]

def open_socket(ip):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((ip, 1000))
    return clientSocket

p_laser = Pin(5, Pin.OUT, drive=Pin.HIGH_POWER)
p_sensor = ADC(Pin(1))
button = Pin(2, Pin.IN, Pin.PULL_UP)
id = machine.unique_id()
ip = connect()
s = open_socket(ip)

def shoot_laser():
    p_laser.on()
    s.send("Shot " + id + datetime.now().strftime("%H:%M:%S") + "\n")
    time.sleep(0.1)
    p_laser.off()

while True:
    if button.value() == 1:
        shoot_laser()
    l = p_sensor.read_u16()
    if l>0.8:
        s.send("Got " + id + datetime.now().strftime("%H:%M:%S") + "\n")
    time.sleep(0.2)