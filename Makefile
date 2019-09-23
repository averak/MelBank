## -----*----- Makefile -----*----- ##

# リアルタイムで音源分離
exec: ./exec.py
	@python ./exec.py

# 音声録音
record: ./lib/scripts/recording.py
	@python ./lib/scripts/recording.py

# 教師データの元を録音
teach.record: ./make_teacher.py
	@python ./make_teacher.py

# 教師データを作成
teach.build: ./lib/scripts/shift.py
	@python ./lib/scripts/shift.py

# 学習
train: ./train.py
	@python ./train.py