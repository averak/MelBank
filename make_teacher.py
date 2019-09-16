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

exit (0)

record = Recording()
for i in range(10):
    record.file = '{0}/{1}/{2}.wav'.format(dir, name, i)

time.sleep(1)
print('start')
record.record_start.set()
time.sleep(0.3)
record.record_start.clear()
record.is_exit = True
