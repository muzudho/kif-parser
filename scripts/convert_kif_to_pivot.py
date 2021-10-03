from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot
from kif_to_kifu import convert_kif_to_kifu


def convert_kif_to_pivot(kif_file, output_folder='temporary/pivot'):
    kifu_file, doneKifFile = convert_kif_to_kifu(kif_file)
    if kifu_file is None:
        return None, None

    pivot_file = convert_kifu_to_pivot(
        kifu_file, output_folder=output_folder)
    if pivot_file is None:
        return None, None

    # print(f'kifu_file={kifu_file} pivot_file={pivot_file}')
    return pivot_file, doneKifFile
