current = ['idle', 'idle', 'idle', 'idle', 'idle', 'idle', 'idle', 'idle']
last = ['pass', 'pass', 'pass', 'pass', 'pass', 'pass', 'pass', 'pass']

def set_tester_state(id, state):
    current[id] = state


def get_aab(id, state):
    if(state=='fail'):
        if(last[id]=='pass'):
            ret = 'A'
        else:
            ret = 'B'
    else:
        ret = 'Next'
    last[id] = state
    return ret
