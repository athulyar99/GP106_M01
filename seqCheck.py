def check_seq(pb1_response,pb2_response):

    from pyfirmata import Arduino, util
    import pyfirmata
    board = Arduino('COM3')

    iterator = util.Iterator(board)
    iterator.start()

    import time

    pb1 = board.get_pin('d:12:i') #push button 1 - security 1
    pb2 = board.get_pin('d:2:i') #push button 2 - security 2
    buzz = board.get_pin('d:10:p') #pulse input to digi10

    pb1_response = pb1.read()
    pb2_response = pb2.read()
    CorSeq = [1,1,0,2]
    global CheckSeq
    checkSeq = []
    global locked
    locked = True

    if pb1.response is True and pb2_response is True: #both pressed
        CheckSeq.append(0)

    elif pb1_response is True and pb2_response is False: #pb1 pressed
        CheckSeq.append(1)

    elif pb1_response is False and pb2_response is True: #pb2 pressed
        CheckSeq.append(2)

    #time.sleep(1.0)
    #print(CheckSeq)
    if len(CheckSeq) == 4:
        if CheckSeq == CorSeq: #if sequence correct
            print('Access Granted')
            locked = False

        else: #if sequence incorrect
            print('Access Denied')
            for j in range(30):
                buzz.write(j/50) #buzzer on
                time.sleep(0.1)
