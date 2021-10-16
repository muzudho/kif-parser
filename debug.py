"""このファイルの使い方

python.exe debug.py --tool kif2kifu
python.exe debug.py --tool kif2pivot
python.exe debug.py --tool kifu2kif
python.exe debug.py --tool kifu2pivot
python.exe debug.py --tool pivot2kif
python.exe debug.py --tool pivot2kifu
python.exe debug.py --rmin
python.exe debug.py --rmout
python.exe debug.py --rmtmp
"""
import argparse
from scripts.reversible_convert_kif_to_kifu import ReversibleConvertKifToKifu
from scripts.reversible_convert_kif_to_pivot import ReversibleConvertKifToPivot
from scripts.reversible_convert_kifu_to_kif import ReversibleConvertKifuToKif
from scripts.reversible_convert_kifu_to_pivot import ReversibleConvertKifuToPivot
from scripts.reversible_convert_pivot_to_kif import ReversibleConvertPivotToKif
from scripts.reversible_convert_pivot_to_kifu import ReversibleConvertPivotToKifu
from scripts.clear_all_records_in_folder import clear_all_records_in_folder
from scripts.remove_all_temporary import remove_all_temporary
from scripts.remove_all_input import remove_all_input


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Debug tool.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--tool', help='kif2kifu, kif2pivot, kifu2kif, kifu2pivot, pivot2kif, pivot2kifu.')
    parser.add_argument(
        '--rmin', action='store_true', help='Clean input folder after translation.')
    parser.add_argument(
        '--rmout', action='store_true', help='Clean output folder after translation.')
    parser.add_argument(
        '--rmtmp', action='store_true', help='Clean temporary folder after translation.')
    args = parser.parse_args()

    if args.tool == "kif2kifu":
        # KIF to KIFU
        reversible_convert_kif_to_kifu = ReversibleConvertKifToKifu(debug=True)
        reversible_convert_kif_to_kifu.reversible_convert_kif_to_kifu_ready()
        reversible_convert_kif_to_kifu.reversible_convert_kif_to_kifu()
        reversible_convert_kif_to_kifu.reversible_convert_kif_to_kifu_clean()
    elif args.tool == "kif2pivot":
        reversible_convert_kif_to_pivot = ReversibleConvertKifToPivot()
        reversible_convert_kif_to_pivot.reversible_convert_kif_to_pivot_ready()
        reversible_convert_kif_to_pivot.reversible_convert_kif_to_pivot(
            debug=True)
        reversible_convert_kif_to_pivot.reversible_convert_kif_to_pivot_clean()
    elif args.tool == "kifu2kif":
        reversible_convert_kifu_to_kif = ReversibleConvertKifuToKif(debug=True)
        reversible_convert_kifu_to_kif.reversible_convert_kifu_to_kif_ready()
        reversible_convert_kifu_to_kif.reversible_convert_kifu_to_kif()
        reversible_convert_kifu_to_kif.reversible_convert_kifu_to_kif_clean()
    elif args.tool == "kifu2pivot":
        reversible_convert_kifu_to_pivot = ReversibleConvertKifuToPivot(
            debug=True)
        reversible_convert_kifu_to_pivot.reversible_convert_kifu_to_pivot_ready()
        reversible_convert_kifu_to_pivot.reversible_convert_kifu_to_pivot()
        reversible_convert_kifu_to_pivot.reversible_convert_kifu_to_pivot_clean()
    elif args.tool == "pivot2kif":
        reversible_convert_pivot_to_kif = ReversibleConvertPivotToKif(
            debug=True)
        reversible_convert_pivot_to_kif.reversible_convert_pivot_to_kif_ready()
        reversible_convert_pivot_to_kif.reversible_convert_pivot_to_kif()
        reversible_convert_pivot_to_kif.reversible_convert_pivot_to_kif_clean()
    elif args.tool == "pivot2kifu":
        reversible_convert_pivot_to_kifu = ReversibleConvertPivotToKifu(
            debug=True)
        reversible_convert_pivot_to_kifu.reversible_convert_pivot_to_kifu_ready()
        reversible_convert_pivot_to_kifu.reversible_convert_pivot_to_kifu()
        reversible_convert_pivot_to_kifu.reversible_convert_pivot_to_kifu_clean()

    if args.rmout:
        clear_all_records_in_folder('output')

    if args.rmtmp:
        remove_all_temporary()

    if args.rmin:
        remove_all_input()
