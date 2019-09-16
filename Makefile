## -----*----- Makefile -----*----- ##

# リアルタイムで音声録音
record.always: ./lib/scripts/detection.py
	@python ./lib/scripts/detection.py

# 一度だけ音声録音
record.once: ./lib/scripts/recording.py
	@python ./lib/scripts/recording.py

# 教師データの元を録音
teach.record: ./make_teacher.py
	@python ./make_teacher.py

# 教師データを作成
teach.build: ./lib/scripts/shift.py
	@python ./lib/scripts/shift.py