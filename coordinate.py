class Coordinate():
    def __init__(self, row=None, col=None, literal=None) -> None:
        self.corresponding_row = {
            "1": 7,
            "2": 6,
            "3": 5,
            "4": 4,
            "5": 3,
            "6": 2,
            "7": 1,
            "8": 0
        }
        self.corresponding_col = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7
        }

        if literal == None:
            def key_from_value(dict, value):
                for key, val in dict.items():
                    if val == value:
                        return key
                return None  # Returnerar None om inget värde matchar
            
            assert col is not None and row is not None, "Literal and either row and col is None"
            self.col = col
            self.row = row
            if self.isInsideBoard():
                self.literal = key_from_value(self.corresponding_col, col) + key_from_value(self.corresponding_row, row)
            else:
                print("Created Coordinate object without literal")
                self.literal = "error"
        else:
            self.literal = literal
            self.col = self.corresponding_col[literal[0]]
            self.row = self.corresponding_row[literal[1]]

    def isInsideBoard(self):
        return self.row >= 0 and self.row < 8 and self.col >= 0 and self.col < 8