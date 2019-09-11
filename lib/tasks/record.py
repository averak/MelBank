# -*- coding: utf-8 -*-
#from ..scripts import detection
import sys

sys.path.append('./lib/scripts/')
#print(sys.path)
from detection import Detection

desc('Start Recording')
proc = lambda : Detection().start()
task('record', proc)
