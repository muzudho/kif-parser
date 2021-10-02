import glob
import shutil
import os
import sys


def move_output_to_input_danger(output_file, output_folder='input'):
    # basename
    try:
        basename = os.path.basename(output_file)
    except:
        print(f"Error: output_file={output_file} except={sys.exc_info()[0]}")
        raise

    _stem, extention = os.path.splitext(basename)
    if not (extention.lower() in ['.kif', '.kifu', '.json', '.toml']):
        return None

    # output_folderへ移動します
    undone_input_file = shutil.move(
        output_file, os.path.join(output_folder, basename))
    return undone_input_file


def main():
    output_file_patterns = ('./output/*.kif',
                            './output/*.kifu',
                            './output/*.json',
                            './output/*.toml')

    for output_file_pattern in output_file_patterns:
        # 出力ファイル一覧
        output_files = glob.glob(output_file_pattern)
        for output_file in output_files:
            _undone_input_file = move_output_to_input_danger(output_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
