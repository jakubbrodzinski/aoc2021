def parse_and_map(path: str,mapper):
    with open(path) as reader:
        return  map(mapper, reader.readlines())

def read_lines(path: str):
    with open(path) as reader:
        return  reader.readlines()
