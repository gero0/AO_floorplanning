import json


class Block:
    def __init__(self, name, w, h, rotated=False, positionX=0, positionY=0) -> None:
        self.name = name
        self.width = w
        self.height = h
        self.rotated = rotated
        self.positionX = positionX
        self.positionY = positionY

    def rotate(self):
        self.rotated = not self.rotated
        w = self.width
        self.width = self.height
        self.height = w

    def get_mid_point(self):
        return [self.positionX + self.width / 2, self.height / 2 + self.positionY]
    @staticmethod
    def default():
        return Block("XDXDXD",0,0)
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)


def block_from_module(module):
    width = module.dimensions[1][0] - module.dimensions[2][0]
    height = module.dimensions[1][1] - module.dimensions[0][1]
    block = Block(module.name, width, height)
    return block


def block_from_JSON(json):
    block = Block(
        json["name"],
        json["width"],
        json["height"],
        json["rotated"],
        json["positionX"],
        json["positionY"],
    )
    return block

