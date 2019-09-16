## -----*----- Makefile -----*----- ##

# リアルタイムで音声録音
record.always: ./lib/scripts/detection.py
	@python ./lib/scripts/detection.py

# 一度だけ音声録音
record.once: ./lib/scripts/recording.py
	@python ./lib/scripts/recording.py