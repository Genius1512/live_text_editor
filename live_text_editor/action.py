import config


class Action:
    def __init__(self, from_string: str):
        self.char = from_string.split(config.sep)[0]
        self.pos = from_string.split(config.sep)[1]
        self.line = int(self.pos.split(".")[0]) - 1
        self.char_index = int(from_string.split(config.sep)[1].split(".")[1])

    def insert_to_text(self, text) -> str:
        text = text.split("\n") 
        
        if self.char == "<-":
            text[self.line] = text[self.line][:self.char_index-1] + text[self.line][self.char_index:]
        else:
            text[self.line] = text[self.line][:self.char_index] + self.char + text[self.line][self.char_index:]

        _text = ""
        for x in text:
            _text += x + "\n"
        text = _text[:-1]

        return text

    def __repr__(self):
        return f"Char '{self.char}' at line {self.line} in column {self.char_index}"


if __name__ == "__main__":
    action = Action(
        "a-s-1.1"
    )
    text = """Lorem ipsum
dolor sit amet"""
    print(action.insert_to_text(text))
