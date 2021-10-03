import glob
from scripts.move_output_to_input_danger import move_output_to_input_danger


def main():
    output_file_patterns = ('./output/*.kif',
                            './output/*.kifu',
                            './output/*.json',
                            './output/*.toml')

    for output_file_pattern in output_file_patterns:
        # 出力ファイル一覧
        output_files = glob.glob(output_file_pattern)
        for output_file in output_files:
            _undone_input_file = move_output_to_input_danger(
                output_file, output_folder='input')


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
