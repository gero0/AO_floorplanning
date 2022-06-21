import json
import random
import block

class Connection:
    def __init__(self, first, second) -> None:
        self.first = first
        self.second = second

    def toJSON(self):
        return '{{ "first": "{first}", "second": "{second}" }}'.format(first=self.first, second=self.second)


def connection_from_JSON(json):
    connection = Connection(
        json["first"],
        json["second"]
    )
    return connection
