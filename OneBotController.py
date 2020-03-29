from time import sleep
import serial

from Model import Agent

ser = serial.Serial('COM15', 115200) # Establish the connection on a specific port
sleep(2)
bot = Agent()

while True:
    a, x, y = bot.random_action()
    print(str(a) + chr(x + 32) + chr(y + 32))

    ser.flush()

    # Send to Arduino
    ser.write((str(a) + chr(x + 32) + chr(y + 32)).encode()) #cmd
    sleep(0.3)
    
    # Read Arduino Reply
    print("Ard:", ser.read(ser.inWaiting())) # Read the newest output from the Arduino