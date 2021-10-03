import os
import sys
from scripts.test_lib import create_sha256_by_file_path
from scripts.convert_kif_to_pivot import convert_kif_to_pivot
from scripts.convert_pivot_to_kif import convert_pivot_to_kif
import argparse
from remove_all_temporary import remove_all_temporary
from scripts.converter_template import ConverterTemplate


def __main(debug=False):
    converter = ConverterTemplate()
    # 1. 出力フォルダーを空っぽにします
    if not debug:
        converter.last_layer_folder_clean = True
        converter.last_layer_folder_clean_echo = False

    # 2. 指定のファイルを 指定のフォルダーへコピーします
    converter.firlst_layer_file_pattern = './input/*.kif'
    converter.layer2_folder = 'temporary/kif'

    # 3-1. 処理対処となる各ファイル
    converter.layer2_file_pattern = './temporary/kif/*.kif'

    # 4. KIF ファイル一覧
    kif_files = converter.convert_before_loop()

    for kif_file in kif_files:

        # 3-1. SHA256 生成
        kif_sha256 = create_sha256_by_file_path(kif_file)

        # 3-2. kif -> pivot 変換
        pivot_file, _done_kif_file = convert_kif_to_pivot(kif_file)
        if pivot_file is None:
            # Error
            print(f"convert kif to pivot_file fail. kif_file={kif_file}")
            return None

        # 3-3. pivot -> kif 変換
        reverse_kif_file, _reverse_done_pivot_file = convert_pivot_to_kif(
            pivot_file, output_folder='reverse-temporary/kif')
        if reverse_kif_file is None:
            # Error
            print(
                f"convert pivot to kif fail. reverse_kif_file={reverse_kif_file}")
            return None

        # 3-4. ファイルをバイナリ形式で読み込んで SHA256 生成
        reverse_kif_sha256 = create_sha256_by_file_path(reverse_kif_file)

        # 3-5. 一致比較
        if kif_sha256 != reverse_kif_sha256:
            try:
                basename = os.path.basename(kif_file)
            except:
                print(f"Error: kif_file={kif_file} except={sys.exc_info()[0]}")
                raise

            _stem, extention = os.path.splitext(basename)
            if extention.lower() != '.kif':
                return ""

            # Error
            print(f"Not match SHA256. basename={basename}")
            return None

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary(echo=False)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Test .kif Convert.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)
