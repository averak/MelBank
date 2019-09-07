# -*- coding: utf-8 -*-
import os, sys, re, shutil, unicodedata


class Console(object):
    def __init__(self, file, frame=True):
        ## -----*----- コンストラクタ -----*----- ##
        # デザインフォーマット読み込み
        self.file = file
        self.text = re.sub(r'\$[0-9]*', '$', open(file, 'r').read())
        self.size = list(map(lambda item: item.split('$')[-1], re.findall(r'\$[0-9]*', open(file, 'r').read())))

        # ウィンドウサイズの取得
        self.width = shutil.get_terminal_size().columns
        self.position = {}

        cnt = 0
        lines = self.text.split('\n')
        for i in range(len(lines)):
            if lines[i].find('$') == -1:
                continue
            bias = 0
            columns = lines[i].split('$')
            for j in range(len(columns) - 1):
                self.position[cnt] = {'x': self.count_length(columns[j]) + bias, 'y': i}
                if not self.size[cnt] == '':
                    bias = self.position[cnt]['x'] + int(self.size[cnt])
                cnt += 1
        os.system('clear')
        if frame:
            self.create_frame()

    def draw(self, *datas):
        ## -----*----- 描画 -----*----- ##
        for i in range(len(self.size)):
            if self.size[i] == '':
                _str = self.clear_sequense(datas[i])
                value = _str[1] + (_str[0] + ' ' * self.width)[0:(self.width - self.position[i]['x'] - 6)] + _str[2]
            else:
                value = str(datas[i])
            sys.stdout.write('\033[{0}C\033[{1}B%-{2}s\033[{3}A\033[{4}D'
                             .format(self.position[i]['x'] + 3, self.position[i]['y'], self.size[i],
                                     len(self.text.split('\n')), self.width) % value)
        sys.stdout.flush()

    def create_frame(self):
        ## -----*----- 「*」でフレームを生成 -----*----- ##
        field = self.text
        for i in range(len(self.size)):
            if self.size[i] == '':
                field = field.replace('$', '', 1)
            else:
                field = field.replace('$', ' ' * int(self.size[i]), 1)
        lines = field.split('\n') + ['']
        lines[0] = lines[0] + '*' * (self.width - self.count_length(lines[0]))
        for i in range(1, len(lines)):
            lines[i] = '*  ' + lines[i] + '\033[{0}C*'.format(self.width)
        lines.append('*' * self.width)
        field = '\n'.join(lines)
        sys.stdout.write('{0}\033[{1}A\033[{2}D'.format(field, len(lines), self.width))

    def clear_sequense(self, text):
        ## -----*----- シーケンスを削除 -----*----- ##
        ret = [str(text), '', '']
        if not repr(text).find('\\x1b') == -1:
            ret[0] = re.split(r'\\', re.split(r'[0-9]*m', repr(text))[1])[0]
            ret = [ret[0], *text.split(ret[0])]
        return ret

    def count_length(self, text):
        ## -----*----- テキストの長さを取得 -----*----- ##
        cnt = 0
        for c in self.clear_sequense(text)[0]:
            if unicodedata.east_asian_width(c) in 'FWA':
                cnt += 2
            else:
                cnt += 1
        return cnt