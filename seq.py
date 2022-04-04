from cgitb import handler
from tkinter.messagebox import NO
from pyfirmata import Arduino, util
import time
import pyfirmata
from Network.mqtt import MQTT_Handler
from Utility.Event import TimedEventManager
import Topics as tp
import logging

logging.basicConfig(level = logging.WARNING)

board = Arduino('COM3')

iterator = util.Iterator(board)
iterator.start()

MQTT_NAME = "G9_CDR"
MQTT_PORT = 8883
MQTT_SERVER = "vpn.ce.pdn.ac.lk"

CorSeq_conf = [1, 1, 0, 2]  # correct sequence - confidential
CorSeq_secret = [1, 1, 2, 2]  # correct sequence - secret
CorSeq_top = [1, 2, 1, 2]  # correct sequence - top secret
CheckSeq = []  # to store entered squence
locked = True  # True -> no/wrong sequence, False -> correct sequence

pb1 = board.get_pin('d:12:i')  # push button 1 - security 1
pb2 = board.get_pin('d:2:i')  # push button 2 - security 2
pb3 = board.get_pin('d:7:i')  # reset button
pressure_sensor = board.get_pin('d:4:i')  # pressure sensor
buzz = board.get_pin('d:10:p')  # pulse input to digi10
LDR = board.get_pin('a:0:i')  # input analog 0
thm = board.get_pin('a:1:i')  # input thermistor to analog 0
LEDr = board.get_pin('d:6:p')  # red LED -> no/wrong sequence
LEDg = board.get_pin('d:5:p')  # green LED -> correct sequence
LED_lockdown = board.get_pin('d:9:p')  # lockdown indicator

mqtt_handler = MQTT_Handler(MQTT_NAME,MQTT_SERVER,MQTT_PORT)
timed_event_manager = TimedEventManager()


def convert_voltage_to_temp(temp): #converts reading from thermistor to temperature in celcius
    tempC = temp*30+10
    return tempC

def publish_temperature(): #To publish temperature value to mqtt broker
    temp =round(convert_voltage_to_temp(thm.read()),2)
    mqtt_handler.publish(tp.CDR.TEMPERATURE,temp)

def publish_li(): #To publish light intensity value to mqtt broker
    logging.debug('Publishing Light Intensity')
    li = LDR.read()
    mqtt_handler.publish(tp.CDR.LIGHT_INTENSITY,li)

def publish_seq(): #To publish entered sequence to mqtt broker
    logging.debug('Publishing Entered sequence')
    seq = str(CheckSeq)
    mqtt_handler.publish(tp.CDR.SEQ_SEND,seq)

def publish_pressure(): #To publish floor pressure value to mqtt broker
    logging.debug("Publishing Pressure")
    pressure = pressure_sensor.read()
    mqtt_handler.publish(tp.CDR.FLOOR_PRESSURE,pressure)


def seq_checker(msg_payload): #To react the signal sent by mqtt broker after reviewing the entered sequence
    global locked
    if msg_payload == "GRANTED TOP SECRET":
        print('Access Granted - TOP SECRET')
        locked = False
        LEDr.write(0.0)
        LEDg.write(1.0)

    elif msg_payload == "GRANTED SECRET":
        print('Access Granted - SECRET')
        locked = False
        LEDr.write(0.0)
        LEDg.write(1.0)

    elif msg_payload == "GRANTED CONFIDENTIAL":
        print('Access Granted - CONFIDENTIAL')
        locked = False
        LEDr.write(0.0)
        LEDg.write(1.0)

    else:
        print('Access Denied')
        LED_lockdown.write(1.0)
        buzz.write(1.0)

def lockdown(msg_payload): #Turns the system into lockdown status
    buzz.write(1.0)
    LED_lockdown.write(1.0)


timed_event_manager.add_event(1,publish_temperature)
timed_event_manager.add_event(1,publish_li)

mqtt_handler.observe_event(tp.CDR.SEQ_ACCESS, seq_checker)
mqtt_handler.observe_event(tp.CDR.LOCKDOWN, lockdown)

#to react to incoming messages from mqtt
#mqtt_handler.observe_event(topic_of_choosing, function to be run when the message is recieved)
#the function must be of the form function(payload) where payload is where the mqtt message content will be passed into the function
#example function
# def func(msg_payload):
#     print(msg_payload)
#     #returns nothing

while True:
    if pb1.read() is None or pb2.read() is None or thm.read() is None:
        continue
  # check whether board ready to get inputs
    print('Ready')
    break


while True:
    # print(locked)
    timed_event_manager.run()
    time.sleep(0.5)
    temp = thm.read()  # get resistance of LDR - 0.5-0.9

    if temp > 0.75:
        buzz.write(1.0)
        LED_lockdown.write(1.0)  # buzzer on
    else:
        buzz.write(0.0)  # buzzer off

    if(locked):
        time.sleep(0.5)
        li = LDR.read()  # get resistance of LDR - 0.5-0.9

        LEDr.write(0.3)  # red LED on
        LEDg.write(0.0)  # green LED off
        if li > 0.75:
            buzz.write(1.0)  # buzzer on
            LED_lockdown.write(1.0)
        else:
            buzz.write(0.0)  # buzzer off

        pressure_sensor_status = pressure_sensor.read()

        if pressure_sensor_status is True:
            buzz.write(1.0)  # buzzer on
            LED_lockdown.write(1.0)
            publish_pressure()

        if pb1.read() == True and pb2.read() == True:  # both pressed
            print('Response Recorded')
            CheckSeq.append(0)

        elif pb1.read() == True and pb2.read() == False:  # pb1 pressed
            print('Response Recorded')
            CheckSeq.append(1)

        elif pb1.read() == False and pb2.read() == True:  # pb2 pressed
            print('Response Recorded')
            CheckSeq.append(2)

        print(CheckSeq)

        if len(CheckSeq) == 4:
            publish_seq()
            CheckSeq.clear()

    else:
        LEDg.write(0.3)  # green LED on
        LEDr.write(0.0)  # red LED off

    if pb3.read() == True:  # if reset button is pressed
        locked = True
        buzz.write(0.0)  # buzzer off
        LED_lockdown.write(0.0)

        CheckSeq.clear()  # reset check sequence

board.exit()
