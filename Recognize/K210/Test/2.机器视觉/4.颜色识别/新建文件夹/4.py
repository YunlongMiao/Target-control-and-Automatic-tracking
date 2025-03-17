
#调用需要使用到的库文件
from machine import UART
from Maix import GPIO
from fpioa_manager import fm
import utime
#映射UART2的两个引脚
fm.register(GPIO.GPIOHS9,fm.fpioa.UART2_TX)
fm.register(GPIO.GPIOHS10,fm.fpioa.UART2_RX)
#初始化串口，返回调用句柄
uart_A = UART(UART.UART2, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)
#定义一个要发送的字符串
write_str = 'get dat\r\n'
#主循环
while(True):
    read_str = uart_A.read(10)
    print("%s",read_str)
    utime.sleep_ms(100)
    #判断接受到后返回信息
    if read_str != None:
        uart_A.write(write_str)
    utime.sleep_ms(100)


