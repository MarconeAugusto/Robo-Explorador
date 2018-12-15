from threading import Lock, Event

def init():
    global solicita_gerente, gerente_msg_lock, gerente_msg, transmitir_event, transmitir_msg_lock, transmitir_msg
    solicita_gerente = Event()
    gerente_msg_lock = Lock()
    gerente_msg = {}

    transmitir_event = Event()
    transmitir_msg_lock = Lock()
    transmitir_msg = {}