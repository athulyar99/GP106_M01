#light intensity

from pyfirmata import Arduino, util
import time
import pyfirmata

board = Arduino('COM3')

iterator = util.Iterator(board)
iterator.start()

buzz = board.get_pin('d:10:p') #pulse input to digi10
LDR = board.get_pin('a:0:i') #input analog 0

while True:
    time.sleep(1.0)
    li = LDR.read() #get resistance of LDR - 0.5-0.9

    if li>0.75:
        buzz.write(1.0) #buzzer on
    else:
        buzz.write(0.0) #buzzer off

board.exit()
