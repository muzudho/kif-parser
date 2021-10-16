import argparse
from scripts.reversible_convert_kif_to_kifu import reversible_convert_kif_to_kifu
from scripts.reversible_convert_kif_to_pivot import reversible_convert_kif_to_pivot

"""使い方

python.exe debug.py --tool kif2kifu
python.exe debug.py --tool kif2pivot
"""

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Debug tool.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--tool', help='"kif2kifu".')
    args = parser.parse_args()

    if args.tool == "kif2kifu":
        # KIF to KIFU
        reversible_convert_kif_to_kifu(debug=True)
    elif args.tool == "kif2pivot":
        reversible_convert_kif_to_pivot(debug=True)
