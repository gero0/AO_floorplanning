import json


class Block:
    def __init__(self, name, w, h, rotated = False) -> None:
        self.name = name
        self.width = w
        self.height = h
        self.rotated = rotated

    def rotate(self):
        self.rotated = not self.rotated
        w = self.width
        self.width = self.height
        self.height = w

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)


def block_from_module(module):
    width = module.dimensions[1][0] - module.dimensions[2][0]
    height = module.dimensions[1][1] - module.dimensions[0][1]
    block = Block(module.name, width, height)
    return block


def block_from_JSON(json):
    block = Block(json["name"], json["width"], json["height"], json["rotated"])
    return block
