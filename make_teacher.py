# -*- coding: utf-8 -*-
from lib.scripts.recording import Recording
import time
import os

# ===== 新規話者の登録 ===============
dir = './tmp/speaker'

# 標準入力で話者名を指定
print('新規話者： ', end='')
name = input()
# ディレクトリ作成
os.makedirs('{0}/{1}'.format(dir, name), exist_ok=True)

record = Recording()
os.system('clear')

for i in range(10):
    time.sleep(2)
    record.file = '{0}/{1}/{2}.wav'.format(dir, name, i + 1)
    print("===== {0} START ===============".format(i + 1))
    time.sleep(0.5)
    record.record_start.set()
    time.sleep(1.0)
    record.record_start.clear()
    print("===== END ===============\n")

record.is_exit = True
