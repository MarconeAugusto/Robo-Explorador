from threading import Lock, Event, Semaphore

def init():
    global sa_lock, sa_event, sa_msg, sw_event, sw_lock, sw_msg, sr_lock, autonomo_msg
    global autonomo_lock, autonomo_event, main_event, main_lock, main_msg, sacomrx

    sa_event = Event()
    sa_lock = Lock()
    sa_msg = {}

    sw_event = Event()
    sw_lock = Lock()
    sw_msg = {}

    sr_lock = Lock()
    sacomrx = Lock()


    autonomo_event = Event()
    autonomo_lock = Lock()
    autonomo_msg = {}

    main_event = Event()
    main_lock = Lock()
    main_msg = {}