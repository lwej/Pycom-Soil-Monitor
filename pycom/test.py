import machine
from time import sleep
from machine import Timer
from machine import Pin


class RPM:

    def __init__(self, pin):
        self._pin = Pin(pin,mode=Pin.IN)
        self._intvl = 0
        self._pin.callback(Pin.IRQ_RISING,handler=self._callback,arg=self)
        self._timer = Timer.Chrono()
        self._timer.start()

    def _callback(self,obj):
        self._intvl = self._timer.read_ms()
        self._timer.reset()

    def rpm(self):
        return self._intvl

while True:
    data = RPM('G10')
    print(data.rpm())
    sleep(1)
