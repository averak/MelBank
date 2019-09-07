# -*- coding: utf-8 -*-
from lib.scripts.detection import Detection

desc('Start Recording')
proc = lambda : Detection().start()
task('record', proc)
