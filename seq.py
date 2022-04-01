from pyfirmata import Arduino, util
import time
import pyfirmata

board = Arduino('COM3')

iterator = util.Iterator(board)
iterator.start()

CorSeq_conf = [1,1,0,2] #correct sequence - confidential
CorSeq_secret = [1,1,2,2] #correct sequence - confidential
CorSeq_top = [1,2,1,2] #correct sequence - confidential
CheckSeq = [] #to store entered squence
locked = True #True -> no/wrong sequence, False -> correct sequence

pb1 = board.get_pin('d:12:i') #push button 1 - security 1
pb2 = board.get_pin('d:2:i') #push button 2 - security 2
pb3 = board.get_pin('d:7:i') # reset button
pressure_sensor = board.get_pin('d:4:i') #pressure sensor
buzz = board.get_pin('d:10:p') #pulse input to digi10
LDR = board.get_pin('a:0:i') #input analog 0
thm = board.get_pin('a:1:i') #input thermistor to analog 0
LEDr = board.get_pin('d:6:p') #red LED -> no/wrong sequence
LEDg = board.get_pin('d:5:p') #green LED -> correct sequence
LED_lockdown = board.get_pin('d:9:p') #lockdown indicator

while True:
    if pb1.read() is None or pb2.read() is None:
        continue
    print('Ready') #check whether board ready to get inputs
    break

while True:
    time.sleep(0.5)
    temp = thm.read() #get resistance of LDR - 0.5-0.9

    if temp>0.75:
        buzz.write(1.0)
        LED_lockdown.write(1.0) #buzzer on
    else:
        buzz.write(0.0) #buzzer off

    if(locked):
        time.sleep(0.5)
        li = LDR.read() #get resistance of LDR - 0.5-0.9
        LEDr.write(0.3) #red LED on
        LEDg.write(0.0) #green LED off
        if li>0.75:
            buzz.write(1.0) #buzzer on
            LED_lockdown.write(1.0)
        else:
            buzz.write(0.0) #buzzer off

        pressure_sensor_status = pressure_sensor.read()

        if pressure_sensor_status is True:
            buzz.write(1.0) #buzzer on
            LED_lockdown.write(1.0)

    else:
        #print(locked)
        LEDg.write(0.3) #green LED on
        LEDr.write(0.0) #red LED off



        if pb1.read() == True and pb2.read() == True: #both pressed
            print('Response Recorded')
            CheckSeq.append(0)

        elif pb1.read() == True and pb2.read() == False: #pb1 pressed
            print('Response Recorded')
            CheckSeq.append(1)

        elif pb1.read() == False and pb2.read() == True: #pb2 pressed
            print('Response Recorded')
            CheckSeq.append(2)

        #time.sleep(1.0)
        #print(CheckSeq)
        if len(CheckSeq) == 4:
            if CheckSeq == CorSeq_conf or CheckSeq == CorSeq_secret or CheckSeq == CorSeq_top: #if sequence correct
                print('Access Granted')
                locked = False
                break

            else: #if sequence incorrect
                print('Access Denied')
                CheckSeq.clear()
                continue


    if pb3.read() == True: #if reset button is pressed
        locked = True
        buzz.write(0.0) #buzzer off
        LED_lockdown.write(0.0)

        CheckSeq.clear() #reset check sequence

board.exit()
