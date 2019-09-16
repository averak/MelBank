# -*- coding: utf-8 -*-
from lib.scripts.recording import Recording
import time


# ========== 録音 ====================
record = Recording()
time.sleep(1)
print('start')
record.record_start.set()
time.sleep(0.3)
record.record_start.clear()
record.is_exit = True