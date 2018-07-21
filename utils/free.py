from random import choice
from datetime import datetime

def Ran():
    s_tr = 'zxcvbnmasdfghjklpoiuytrewq1234567890'
    run = ''
    for _ in range(20):
        run += choice(s_tr)
    return run


def order_o_num():
    s_tr = 'zxcvbnmasdfghjklpoiuytrewq1234567890'
    time = datetime.now()
    a = time.strftime('%Y%m%d%H%M%S')
    num = ''
    for _ in range(20):
        num += choice(s_tr)

    return num + a

















