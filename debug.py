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
        kif2kifu = ReversibleConvertKifToKifu(debug=True)
        kif2kifu.ready_folder()
        for kif_file in kif2kifu.target_files():
            kif2kifu.round_trip_translate(kif_file=kif_file)
            kif2kifu.clean_temporary()
    elif args.tool == "kif2pivot":
        kif2pivot = ReversibleConvertKifToPivot(debug=True)
        kif2pivot.ready_folder()
        for kif_file in kif2pivot.target_files():
            kif2pivot.round_trip_translate(kif_file=kif_file)
        kif2pivot.clean_temporary()
    elif args.tool == "kifu2kif":
        kifu2kif = ReversibleConvertKifuToKif(debug=True)
        kifu2kif.ready_folder()
        for kifu_file in kifu2kif.target_files():
            kifu2kif.round_trip_translate(kifu_file)
        kifu2kif.clean_temporary()
    elif args.tool == "kifu2pivot":
        kifu2pivot = ReversibleConvertKifuToPivot(debug=True)
        kifu2pivot.ready_folder()
        for kifu_file in kifu2pivot.target_files():
            kifu2pivot.round_trip_translate(kifu_file)
        kifu2pivot.clean_temporary()
    elif args.tool == "pivot2kif":
        pivot2kif = ReversibleConvertPivotToKif(
            debug=True)
        pivot2kif.ready_folder()
        for pivot_file in pivot2kif.target_files():
            pivot2kif.round_trip_translate(pivot_file)
        pivot2kif.clean_temporary()
    elif args.tool == "pivot2kifu":
        pivot2kifu = ReversibleConvertPivotToKifu(debug=True)
        pivot2kifu.ready_folder()
        for pivot_file in pivot2kifu.target_files():
            pivot2kifu.round_trip_translate(pivot_file)
        pivot2kifu.clean_temporary()

    if args.rmout:
        clear_all_records_in_folder('output')

    if args.rmtmp:
        remove_all_temporary()

    if args.rmin:
        remove_all_input()
