import os
import inspect
import codecs
import sys


def convert_kif_to_kifu(kif_file, output_folder, debug=False):
    """(1) kif_file(*.kif)ファイルを読み取ります
    (2) *.kifuファイルを output_folder へ生成します

    Returns
    -------
    (str, str)
        出力したkifuファイルへのパス, 読み終えたkifファイルへのパス
        KIFファイルでなかったなら空文字列
    """

    out_path = ""

    # シフトJISエンコードのテキストファイルの読み込み
    with codecs.open(kif_file, "r", encoding='shift_jis') as f_in:

        # basename
        try:
            basename = os.path.basename(kif_file)
        except:
            print(
                f"Basename fail. kif_file={kif_file} except={sys.exc_info()[0]}")
            raise

        stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kif':
            return None

        # Append new extention
        out_path = os.path.join(output_folder, f"{stem}.kifu")

        if debug:
            print(
                f"[DEBUG] {os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}: Write to [{out_path}]")
        with codecs.open(out_path, "w", encoding='utf-8') as f_out:

            # UTF-8形式に変換して保存
            for row in f_in:
                f_out.write(row)

    return out_path
