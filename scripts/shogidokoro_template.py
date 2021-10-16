class ShogidokoroTemplate():
    def __init__(self):
        pass

    def comment_row(self, row_data):
        s = ""

        if "indent" in row_data:
            s += row_data["indent"]

        return f'{s}#{row_data["comment"]}\n'

    def explain_row(self, row_data):
        s = ""

        if "indent" in row_data:
            s += row_data["indent"]

        s += f'*{row_data["explain"]}'

        if "comment" in row_data:
            s += f'#{row_data["comment"]}'

        return f'{s}\n'

    def bookmark_row(self, row_data):
        s = ""

        if "indent" in row_data:
            s += row_data["indent"]

        s += f'&{row_data["bookmark"]}'

        if "comment" in row_data:
            s += f'#{row_data["comment"]}'

        return f'{s}\n'

    def moves_header_row(self, row_data):
        s = row_data["movesHeader"]

        if "comment" in row_data:
            s += f'#{row_data["comment"]}'

        return f"{s}\n"
