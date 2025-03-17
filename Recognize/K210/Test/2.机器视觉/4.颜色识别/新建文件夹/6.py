# Untitled - By: 30824 - 周日 4月 30 2023

import sensor, image, time
from machine import UART,Timer
from fpioa_manager import fm

#定义
fm.register(6, fm.fpioa.UART1_RX, force = Ture)
fm.register(7, fm.fpioa.UART1_TX, force = Ture)

machine.UART(UART.UART1,115200,8,None,1)

while True:
    text = UART.read(4)
    Line = UART.readline(;)
    print(text)
    print(Line)
    if text != None：
        UART.write(text)
    UART.deinit()
    exit(0)

