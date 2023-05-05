```python
from machine import Pin
import time

PirSensor = Pin(14, Pin.IN, Pin.PULL_DOWN)

while True:
    if PirSensor.value():
        print("Movimiento detectado")
        time.sleep(2)
    else:
        print("Sin movimiento")
        time.sleep(2)
```
