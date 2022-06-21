import json
import random
import block

class Connection:
    def __init__(self, first, second) -> None:
        self.first = first
        self.second = second

    def generate_rand_from(blocks):
        def get_rand_block():
            rand = random.randint(0, blocks.count - 1)
            return blocks[rand]

        connections = []
        while connections.count() < blocks.count()*2:
            first = get_rand_block()
            second = get_rand_block()
            connections.append(Connection(first.name, second.name))
        return connections

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)


def connection_from_JSON(json):
    connection = Connection(
        json["first"],
        json["second"]
    )
    return connection
