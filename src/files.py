import block
import sys
import json
import yal_parser
import connection

def load_file():
    filename = None
    try:
        filename = sys.argv[1]
    except:
        print("Error: No file argument passed")
        raise Exception

    if len(sys.argv) > 2 and "--yal" in sys.argv:
        return load_yal(filename)
    else:
        return load_json(filename)


def load_yal(filename):
    print("Parsing YAL file...")
    modules = yal_parser.parse_file(filename)
    blocks = [block.block_from_module(m) for m in modules if m.name != "bound"]
    return (blocks, [])


def load_json(filename):
    print("Parsing JSON file...")
    file = open(filename, "r")
    try:
        data = json.loads(file.read())
        blocks = [block.block_from_JSON(bl) for bl in data["blocks"]]
        connections = [connection.connection_from_JSON(cn) for cn in data["connections"]]
        return (blocks, connections)
    except:
        print("Error: Invalid JSON file")
        raise Exception
