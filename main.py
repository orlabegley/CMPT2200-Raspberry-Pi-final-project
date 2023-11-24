import time
import board
import adafruit_dht
import digitalio

from tkinter import *
from tkinter.messagebox import showinfo

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)  # heater fan connect to input 5, 6
GPIO.setup(6, GPIO.OUT)  # heater fan
GPIO.setup(13, GPIO.OUT)  # fan connect to input 13, 26
GPIO.setup(26, GPIO.OUT)  # fan

dhtDevice = adafruit_dht.DHT22(board.D18)  # connect dht22 input to 18


class MyGui:
    def __init__(self):
        self.myWindow = Tk()
        self.myWindow.geometry("500x300+100+100")
        self.frame = Frame(self.myWindow, width=500, height=300)
        self.frame.place(x=10, y=10)

        self.actualTemp = IntVar()
        self.targetTemp = IntVar()
        self.targetTemp.set(20)

        # actual temp
        self.label1 = Label(self.frame, text="Actual Temperature: ", background="white", foreground="black")
        self.label1.place(x=10, y=40)
        self.entry1 = Entry(self.frame, textvariable=self.actualTemp)
        self.entry1.place(x=280, y=40)

        # target temp
        self.label2 = Label(self.frame, text="Target Temperature: ", background="white", foreground="black")
        self.label2.place(x=10, y=100)
        self.entry1 = Entry(self.frame, textvariable=self.targetTemp)
        self.entry1.place(x=280, y=100)

        self.submitButton = Button(self.frame, text="Submit", command=self.submit)
        self.submitButton.place(x=250, y=200)

        self.getTempButton = Button(self.frame, text="Get Actual Temperature", command=self.getTemp)
        self.getTempButton.place(x=50, y=200)

        self.quitButton = Button(self.frame, text="Quit", command=self.myWindow.destroy)
        self.quitButton.place(x=350, y=200)

    def submit(self):
        showinfo("Temperature reading", "Actual temperature is: " + str(self.actualTemp.get()) + '\n'
                 + "Target temperature is: " + str(self.targetTemp.get()))

        if (int(self.actualTemp.get()) > int(self.targetTemp.get())):  # turn on fake heater
            GPIO.output(5, True)  # connect heater fan to gpios 5 and 6
            GPIO.output(6, False)
        if (int(self.actualTemp.get()) < int(self.targetTemp.get())):  # turn on fan
            GPIO.output(13, True)  # connect fan to gpios 13 and 26
            GPIO.output(26, False)

    def getTemp(self):
        try:
            # get the info from the DHT22 sensor
            temperatureRaw = dhtDevice.temperature  # temp as degrees celcius
            temp = format(temperatureRaw, '.0f')

            self.actualTemp.set(int(temp))

        except RuntimeError as error:  # print an error message if runtime error so doesnt crash
            print(error.args[0])
            time.sleep(2.0)
        except Exception as error:  # catch any other errors that may occur
            dhtDevice.exit()
            raise error


my_gui = MyGui()
mainloop()