import glob
import shutil
import os

def read_kif_file(path):
    """KIFファイルを読み取ります
    """
    
    success = False
    
    # シフトJISエンコードのテキストファイルの読み込み
    with open(path, encoding='shift_jis') as f:
        s = f.read()

        print(s.rstrip())  # このファイルはシフトJISでエンコードされています
        
        # KIFU形式に変換
        
        success = True

    if success:
        # ファイルの移動
        new_path = shutil.move(path, 'input-done')
        print(new_path)
    
def main():
    # ファイル一覧
    files = glob.glob("./input/*")
    for file in files:
        read_kif_file(file)

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
