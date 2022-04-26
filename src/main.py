import block
import sys
import json
import yal_parser

if __name__ == "__main__":
    filename = None
    try:
        filename = sys.argv[1]
    except:
        print("Error: No file argument passed")
        exit()

    blocks = []
    connections = []

    if len(sys.argv) > 2 and sys.argv[2] == "--yal":
        print("Parsing YAL file...")
        modules = yal_parser.parse_file(filename)
        blocks = [block.block_from_module(m) for m in modules if m.name != "bound"]
    else:
        print("Parsing JSON file...")
        file = open(filename, 'r')
        try:
            data = json.loads(file.read())
            blocks = [block.block_from_JSON(bl) for bl in data['blocks']]
            connections = data['connections']
        except:
            print("Error: Invalid JSON file")
            exit()
    

    for block in blocks:
        print(block.toJSON())
