# -*- coding: utf-8 -*-
import os, sys, time, wave, glob


class Shift(object):
    def __init__(self):
        ## -----*----- コンストラクタ -----*----- ##
        self.teacher_path = './config/format.wav'
        self.shift_path = './tmp/teach'

        self.cnt = 0

        # 教師データからフォーマットを取得
        self.read_format(self.teacher_path)

    def read_format(self, path):
        ## -----*----- 教師データからフォーマットを取得 -----*----- ##
        wf = wave.open(path, 'rb')
        self.format = {'channel': wf.getnchannels(), 'width': wf.getsampwidth(),
                       'rate': wf.getframerate(), 'point': len(wf.readframes(wf.getnframes()))}
        print(self.format)
        wf.close()

    def get_dats(self, path):
        ## -----*----- フレーム数の取得 -----*----- ##
        dats = []
        wf = wave.open(path)
        wf_point = wf.readframes(wf.getnframes())
        dats_frames = len(wf_point)
        dats.append(wf_point)
        wf.close()
        return dats, dats_frames

    def get_shift_size(self, dats_size):
        ## -----*----- シフトする個数の取得 -----*----- ##
        total_shift_size = dats_size - self.format['point']
        shift_size = int(self.format['point'] * 0.1)
        while (total_shift_size % shift_size != 0) and (shift_size < int(self.format['point'] * 0.2)):
            shift_size += 1
        if shift_size == int(self.format['point'] * 0.2):
            shift_size = int(self.format['point'] * 0.1)
            total_shift_size -= 1
            while (total_shift_size % shift_size != 0) and (shift_size < int(self.format['point'] * 0.5)):
                shift_size += 1
        return total_shift_size, shift_size

    def save_shift_audio(self, dats, cmd, total_shift_size, shift_size):
        ## -----*----- シフトしたファイルを保存 -----*----- ##
        os.makedirs('{0}/{1}'.format(self.shift_path, cmd), exist_ok=True)
        total_shift = 0
        cnt = 0
        while total_shift <= total_shift_size:
            wf = wave.open('{0}/{1}/{2}.wav'.format(self.shift_path, cmd, self.cnt), 'wb')
            wf.setnchannels(self.format['channel'])
            wf.setsampwidth(self.format['width'])
            wf.setframerate(self.format['rate'])
            wf.writeframes(dats[0][int(shift_size) * cnt:self.format['point'] + int(shift_size) * cnt])
            wf.close()
            total_shift += shift_size
            cnt += 1
            self.cnt += 1


if __name__ == '__main__':
    shift = Shift()

    files = glob.glob('./tmp/recorded/*/*.wav')
    for file in files:
        cmd = file.split('/')[3]
        dats, dats_frames = shift.get_dats(file)
        total_shift_size, shift_size = shift.get_shift_size(dats_frames)
        shift.save_shift_audio(dats, cmd, total_shift_size, shift_size)