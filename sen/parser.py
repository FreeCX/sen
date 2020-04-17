SPACE = ' '
COLON = ':'
SEP = [COLON, SPACE]
TAB = '\t'


def split(item, separators):
    for sep in separators:
        if sep in item:
            items = list(map(str.strip, item.split(sep)))
            if COLON in item and len(items) == 2:
                return {items[0]: split(items[1], SEP)}
            return items
    return item


def flatten(lst):
    result = {} 
    for item in lst:
        if len(item) == 1:
            k = list(item.keys())[0]
            result[k] = item[k]
    return result

def normalize(data):
    return {
        'import': data.get('import'),
        'configuration': flatten(data.get('configuration', [])),
        'element': flatten(data.get('element', [])),
        'connection': data.get('connection', []),
        'test': data.get('test', [])
    }


def loads(lines):
    block_name = ''
    block = {}
    buff = []
    for index, line in enumerate(lines):
        if line.startswith(':'):
            if len(buff) > 0:
                block[block_name] = buff
                buff = []
            block_name = line.strip().replace(COLON, '')
        else:
            val = line.strip()
            if len(val) > 0:
                buff.append(split(val, SEP))
    return normalize(block)


def load(fd):
    lines = fd.readlines()
    return loads(lines)