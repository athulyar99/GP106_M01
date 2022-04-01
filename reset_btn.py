def reset_btn(pb3_response):

    from pyfirmata import Arduino, util
    import pyfirmata
    board = Arduino('COM3')

    iterator = util.Iterator(board)
    iterator.start()

    pb3 = board.get_pin('d:7:i') # reset button
    buzz = board.get_pin('d:10:p') #pulse input to digi10

    global locked
    global CheckSeq

    if pb3.read() == True: #if reset button is pressed
        locked = True
        buzz.write(0.0) #buzzer off

        CheckSeq.clear() #reset check sequence
