import os
import codecs
import sys


def convert_kifu_to_kif(kifu_file, output_folder, debug=False):
    """(1) kifu_file(*.kifu)ファイルを読み取ります
    (2) *.kifファイルを kif フォルダーへ生成します
    (3) 読み終えた *.kifuファイルは done_folder フォルダーへ移動します

    Returns
    -------
    str
        新しいパス。
        KIFUファイルでなかったなら空文字列
    """

    # シフトJISエンコードのテキストファイルの読み込み
    with codecs.open(kifu_file, "r", encoding='utf-8') as f:

        # basename
        try:
            basename = os.path.basename(kifu_file)
        except:
            print(f"Error: kifu_file={kifu_file} except={sys.exc_info()[0]}")
            raise

        stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kifu':
            return ""

        # New file
        out_path = os.path.join(output_folder, f"{stem}.kif")

        if debug:
            print(
                f"[DEBUG] convert_kifu_to_kif.py convert_kifu_to_kif(): Write to [{out_path}]")
        with codecs.open(out_path, "w", encoding='shift_jis') as f_out:

            # UTF-8形式に変換して保存
            for row in f:
                f_out.write(row)

    return out_path
