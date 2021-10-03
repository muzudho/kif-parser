import os
import glob


def clear_last_layer_folder(echo=True):
    file_patterns = ('./output/*.kif',
                     './output/*.kifu',
                     './output/*.json',
                     './output/*.toml')

    for file_pattern in file_patterns:
        # 出力ファイル一覧
        files = glob.glob(file_pattern)
        for file in files:
            if echo:
                print(f"Remove: {file}")
            os.remove(file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    clear_last_layer_folder()
