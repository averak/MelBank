## -----*----- Makefile -----*----- ##

# リアルタイムで音声録音
record.always: ./lib/scripts/detection.py
	@python ./lib/scripts/detection.py

# 一度だけ音声録音
record.once: ./lib/scripts/recording.py
	@python ./lib/scripts/recording.py

# 教師データの作成
teach.make: ./make_teacher.py
	@python ./make_teacher.py