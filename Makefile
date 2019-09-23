## -----*----- Makefile -----*----- ##

# リアルタイムで音源分離
exec:
	@python ./exec.py

# 音声録音
record:
	@python ./lib/scripts/recording.py

# 教師データの元を録音
teach.record:
	@python ./make_teacher.py

# 教師データを作成
teach.build:
	@python ./lib/scripts/shift.py

# 学習
train:
	@python ./train.py