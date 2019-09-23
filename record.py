# -*- coding: utf-8 -*-
from lib.scripts.recording import Recording
import time, os, threading

record = Recording()
os.system('clear')
print('*** ENTERを押して録音開始・終了 ***')

mode = 0  # 0：録音開始，1：録音終了
cnt = 1

while True:
    key = input()

    if mode == 0:
        # 録音開始
        print("===== {0} START ===============".format(cnt))
        record.record_start.set()
        mode = 1

    else:
        # 録音終了
        print("===== END ===============")
        record.record_start.clear()
        mode = 0
        cnt += 1
