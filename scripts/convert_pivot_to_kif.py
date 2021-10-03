from pivot_to_kifu import convert_pivot_to_kifu
from kifu_to_kif import convert_kifu_to_kif


def convert_pivot_to_kif(pivotFile, output_folder='temporary/kif'):
    kifuFile, donePivotFile = convert_pivot_to_kifu(pivotFile)
    if kifuFile is None:
        return None, None

    # kifu to kif
    kifFile, _doneKifuFile = convert_kifu_to_kif(
        kifuFile, output_folder=output_folder)
    return kifFile, donePivotFile
