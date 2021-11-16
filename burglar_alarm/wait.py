from time import time

def wait(sec):
    set_time = time()
    while set_time - time() != sec:
        pass
    return