def fire_alarm():

    from pyfirmata import Arduino, util
    import pyfirmata
    board = Arduino('COM3')

    iterator = util.Iterator(board)
    iterator.start()

    import time
    thm = board.get_pin('a:1:i')
    buzz = board.get_pin('d:10:p')

    time.sleep(0.5)
    temp = thm.read() #get resistance of LDR - 0.5-0.9

    if temp>0.75:
        buzz.write(1.0) #buzzer on
    else:
        buzz.write(0.0) #buzzer off
