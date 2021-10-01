import os
import glob


def main():
    file_patterns = ('./output/*.kif')
    file_patterns = ('./output/*.kifu')
    file_patterns = ('./output/*.json')
    file_patterns = ('./output/*.toml')

    for file_pattern in file_patterns:
        # 出力ファイル一覧
        files = glob.glob(file_pattern)
        for file in files:
            print(f"Remove: {file}")
            os.remove(file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
