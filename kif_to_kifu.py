import glob
import shutil
import os
import codecs
import sys
import argparse
from remove_all_temporary import remove_all_temporary
from remove_all_output import remove_all_output


def copy_kif_from_input(output_folder='temporary/kif'):
    """inputフォルダーにある `*.kif` ファイルを kifフォルダーへコピーします"""

    input_files = glob.glob("./input/*.kif")
    for input_file in input_files:
        # basename
        try:
            basename = os.path.basename(input_file)
        except:
            print(f"Error: input_file={input_file} except={sys.exc_info()[0]}")
            raise

        copy_file = os.path.join(output_folder, basename)
        shutil.copyfile(input_file, copy_file)


def convert_kif_to_kifu(kif_file, output_folder='temporary/kifu', done_folder='temporary/kif-done'):
    """(1) kif_file(*.kif)ファイルを読み取ります
    (2) *.kifuファイルを output_folder へ生成します
    (3) 読み終えた *.kifファイルは done_folder へ移動します

    Returns
    -------
    (str, str)
        出力したkifuファイルへのパス, 読み終えたkifファイルへのパス
        KIFファイルでなかったなら空文字列
    """

    out_path = ""

    # シフトJISエンコードのテキストファイルの読み込み
    with codecs.open(kif_file, "r", encoding='shift_jis') as f:

        # basename
        try:
            basename = os.path.basename(kif_file)
        except:
            print(f"Error: kif_file={kif_file} except={sys.exc_info()[0]}")
            raise

        stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kif':
            return None, None

        # Append new extention
        out_path = os.path.join(output_folder, f"{stem}.kifu")

        with codecs.open(out_path, "w", encoding='utf-8') as fOut:

            # UTF-8形式に変換して保存
            for row in f:
                fOut.write(row)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    done_path = shutil.move(kif_file, os.path.join(done_folder, basename))
    return out_path, done_path


def __main(debug=False):
    if not debug:
        # 出力フォルダーを空っぽにします
        remove_all_output()

    copy_kif_from_input()

    # KIFファイル一覧
    kif_files = glob.glob("./temporary/kif/*.kif")
    for kif_file in kif_files:
        out_path, _done_path = convert_kif_to_kifu(
            kif_file, output_folder='output')
        if out_path is None:
            print(f"Parse fail. kif_file={kif_file}")

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary()


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":

    # Description
    parser = argparse.ArgumentParser(
        description='Convert from .kif file to .kifu file.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)
