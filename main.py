import glob

# ファイル一覧
files = glob.glob("./input/*")
for file in files:
    print(file)
