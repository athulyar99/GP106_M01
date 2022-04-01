from pyfirmata import Arduino, util
import time
import pyfirmata

board = Arduino('COM3')

iterator = util.Iterator(board)
iterator.start()

#buzz = board.get_pin('d:13:p')
thm = board.get_pin('a:1:i')

while True:
    time.sleep(1.0)
    print(thm.read())

board.exit()
