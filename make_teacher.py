# -*- coding: utf-8 -*-
from lib.scripts.recording import Recording
import time, os, threading
import glob

# ===== 新規話者の登録 ===============

dir = './tmp/recorded'

# 標準入力で話者名を指定
print('新規話者： ', end='')
name = input()
# ディレクトリ作成
os.makedirs('{0}/{1}'.format(dir, name), exist_ok=True)

record = Recording()
os.system('clear')
print('*** ENTERを押して録音開始・終了 ***')

mode = 0  # 0：録音開始，1：録音終了
cnt = len(glob.glob('{0}/{1}/*.wav'.format(dir, name))) + 1

while True:
    key = input()

    if mode == 0:
        # 録音開始
        print("===== {0} START ===============".format(cnt))
        record.file = '{0}/{1}/{2}.wav'.format(dir, name, cnt)
        record.record_start.set()
        mode = 1

    else:
        # 録音終了
        print("===== END ===============")
        record.record_start.clear()
        mode = 0
        cnt += 1
