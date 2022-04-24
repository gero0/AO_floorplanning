import sys

class Port:
    def __init__(self, x, y, p_name, p_type, width, layer):
        self.position = (x,y)
        self.name = p_name
        self.type = p_type
        self.width = width
        self.layer= layer

class Module:
    def __init__(self, name, type, dimensions, ports, networks):
        self.name = name
        self.type = type
        self.dimensions = dimensions
        self.ports = ports
        self.networks = networks

class Network:
    def __init__(self, instance, module, signals):
        self.instance = instance
        self.module = module
        self.signals = signals

def get_dimensions(line):
    tokens = line.strip()[:-1].split(' ')
    
    x1 = int(tokens[1])
    y1 = int(tokens[2])
    x2 = int(tokens[3])
    y2 = int(tokens[4])
    x3 = int(tokens[5])
    y3 = int(tokens[6])
    x4 = int(tokens[7])
    y4 = int(tokens[8])
    return ((x1,y1),(x2,y2),(x3,y3),(x4,y4))

def parse_port(line):
    tokens = line.strip()[:-1].split(' ')
    p_name = tokens[0]
    p_type = tokens[1]
    x = int(tokens[2])
    y = int(tokens[3])
    width = int(tokens[4])
    layer = tokens[5]

    port = Port(x,y,p_name, p_type, width, layer)
    return port

def get_iolist(lines):
    ports = []

    line = lines.pop(0)
    try:
        while not line.strip().startswith("ENDIOLIST"):
            port = parse_port(line)
            ports.append(port)
            line = lines.pop(0)
    except:
        print("Error parsing ports")
        raise Exception

    return ports

def parse_networks(lines):
    line = lines.pop(0)
    network_lines = []
    concat_line=""
    while not line.strip().startswith('ENDNETWORK'):
        concat_line = concat_line + line.strip().rstrip()
        if line.rstrip()[-1] == ';':
            network_lines.append(concat_line[:-1])
            concat_line = ""
        line = lines.pop(0)
    
    networks = []

    for line in network_lines:
        tokens = line.split(' ')
        instance = tokens[0]
        module = tokens[1]
        signals = tokens[2:]

        network = Network(instance, module, signals)
        networks.append(network)

    return networks

def parse_module(line, lines):
    try:
        module_name = line.strip()[:-1].split(' ')[1]
        line = lines.pop(0)
        module_type = line.strip()[:-1].split(' ')[1]
        line = lines.pop(0)

        if line.strip().startswith('DIMENSIONS'):
            module_dims = get_dimensions(line)
        else:
            print("Could not get dimensions")
            raise Exception

        line = lines.pop(0)
        if line.strip().startswith('IOLIST'):
            ports = get_iolist(lines)
        else:
            print("IOLIST parse error")
            raise Exception

        
        networks = None

        line = lines.pop(0)
        if(line.strip().startswith('NETWORK')):
            networks = parse_networks(lines)
            line = lines.pop()
            
            
        if not line.strip().startswith('ENDMODULE'):
            print("Parsing error: end of module missing")
            raise Exception

        module = Module(module_name, module_type, module_dims, ports, networks)
        return module
    except:
        print("Parsing error")
        raise Exception


def parse_file(filename):
    file = None

    try:
        file = open(filename, 'r')
    except:
        print("Error: File not found")
        raise Exception

    lines = file.readlines()
    modules = []

    while True:
        try:
            line = lines.pop(0)
        except:
            print("Reached EOF, parsed modules: {}".format(len(modules)))
            break

        if line.strip().startswith('/') or line.strip().startswith('*'):
            continue

        if line.strip().startswith('MODULE'):
            module = parse_module(line, lines)
            modules.append(module)

    return modules

if __name__ == "__main__":
    filename = None
    try:
        filename = sys.argv[1]
    except:
        print("Error: No file argument passed")
        exit()

    modules = parse_file(filename)
    for module in modules:
        print(module.name)

