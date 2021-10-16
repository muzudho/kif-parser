class ShogidokoroTemplate():
    def __init__(self):
        pass

    def comment_row(self, row_data):
        s = ""

        if "indent" in row_data:
            s += row_data["indent"]

        return f'{s}#{row_data["comment"]}\n'
