from time import sleep
import serial

from Model import Agent

ser = serial.Serial('COM15', 115200) # Establish the connection on a specific port
sleep(2)
bot = Agent()

ard_reply = ""

while True:
    a, x, y = bot.random_action()
    print(str(a) + chr(x + 32) + chr(y + 32))

    ser.flush()

    # Send to Arduino
    ser.write((str(a) + chr(x + 32) + chr(y + 32)).encode()) #cmd
    sleep(0.3)
    
    # Read Arduino Reply
    ard_reply = ser.read(ser.inWaiting())
    print("Ard:", ard_reply) # Read the newest output from the Arduino