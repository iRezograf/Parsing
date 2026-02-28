def save_file(f_name, src):
    with open(f_name, 'w') as f:
        f.write(src)

def open_file(f_name):
    with open(f_name, 'r') as f:
        src = f.read()
    return src