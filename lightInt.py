def light_intensity():

    from pyfirmata import Arduino, util
    import pyfirmata
    board = Arduino('COM3')

    iterator = util.Iterator(board)
    iterator.start()

    import time

    LDR = board.get_pin('a:0:i')
    LEDr = board.get_pin('d:6:p') #red LED -> no/wrong sequence
    LEDg = board.get_pin('d:5:p')
    buzz = board.get_pin('d:10:p')

    time.sleep(0.5)
    li = LDR.read() #get resistance of LDR - 0.5-0.9
    LEDr.write(0.3) #red LED on
    LEDg.write(0.0) #green LED off
    if li>0.75:
        buzz.write(1.0) #buzzer on
    else: #if not locked
        buzz.write(0.0) #buzzer off
