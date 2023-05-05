```python
from machine import Pin
import time

Buzzer = Pin(14, Pin.OUT)

while True:
    Buzzer.on()
    time.sleep(1)
    Buzzer.off()
    time.sleep(1)

```
