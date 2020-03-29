import keyboard
import pyscreenshot as ImageGrab
import serial
import time
import cv2
import threading 
import os
import mouse
import pickle

from time import sleep
import serial

from Model import Agent

global kb_done
global m_done

global kb_recorded
global m_recorded

ser = serial.Serial('COM15', 115200) # Establish the connection on a specific port
sleep(2)
bot = Agent()

kb_done = False
m_done = False

folder = "records/"

# Create Functions to Thread:

# Controller Function
def controller_thread():
    while (not kb_done) or (not m_done):
        a, x, y = bot.random_action()
        print(str(a) + chr(x + 32) + chr(y + 32))

        ser.flush()

        # Send to Arduino
        ser.write((str(a) + chr(x + 32) + chr(y + 32)).encode()) #cmd
        sleep(0.3)
        
        # Read Arduino Reply
        try:
            print("Ard:", ser.read(ser.inWaiting())) # Read the newest output from the Arduino
        except Exception:
            pass

# KeyBoard Record Function
def keyboard_thread():
    global kb_done
    global kb_recorded

    kb_recorded = keyboard.record(until='alt+esc')
    print("kb_thread finished")
    kb_done = True

# Mouse Record Function
def mouse_thread():
    global m_done
    global m_recorded

    m_recorded = mouse.record(button="right",target_types="double")
    print("m_thread finished")
    m_done = True

# Screenshot Record Function
def screenshot_thread():
    while (not kb_done) and (not m_done):
        # Capture frame-by-frame
        im = ImageGrab.grab()

        # Save the resulting frame
        inst_name = str(int(time.time()*1000))
        im.save(folder + inst_name + '.png')

    print("s_thread finished")

# Threads

# creating threads 
kb_thread = threading.Thread(target=keyboard_thread, name='kb_thread') 
m_thread = threading.Thread(target=mouse_thread, name='m_thread')
s_thread = threading.Thread(target=screenshot_thread, name='s_thread')
c_thread = threading.Thread(target=controller_thread, name='c_thread')

# starting threads 
kb_thread.start()
m_thread.start()
s_thread.start()
c_thread.start()

# wait until threads finish 
kb_thread.join()
m_thread.join()
s_thread.join()

# Save Data:
inst_name = str(int(time.time()*1000))
pickle.dump({"keyboard":kb_recorded,"mouse":m_recorded}, open(inst_name + "_data.p", "wb"))
test = pickle.load(open(inst_name + "_data.p", "rb" ))
print(test)

ser.close()

# Turn this into a pip library