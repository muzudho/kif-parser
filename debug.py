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
from scripts.change_place import change_place
from scripts.copy_file import copy_file
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

    conv = None

    if args.tool == "kif2kifu":
        # KIF to KIFU
        conv = ReversibleConvertKifToKifu(debug=True)
    elif args.tool == "kif2pivot":
        conv = ReversibleConvertKifToPivot(debug=True)
    elif args.tool == "kifu2kif":
        conv = ReversibleConvertKifuToKif(debug=True)
    elif args.tool == "kifu2pivot":
        conv = ReversibleConvertKifuToPivot(debug=True)
    elif args.tool == "pivot2kif":
        conv = ReversibleConvertPivotToKif(debug=True)
    elif args.tool == "pivot2kifu":
        conv = ReversibleConvertPivotToKifu(debug=True)

    if conv:
        conv.clean_last_layer_folder()

        for input_file in conv.outside_input_files():
            copy = change_place(conv.layer2_folder, input_file)
            copy_file(input_file, copy, debug=True)

        for input_file in conv.target_files():
            conv.round_trip_translate(input_file)
        conv.clean_temporary()

    if args.rmout:
        clear_all_records_in_folder('output')

    if args.rmtmp:
        remove_all_temporary()

    if args.rmin:
        remove_all_input()
