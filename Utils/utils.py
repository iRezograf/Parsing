from fake_useragent import UserAgent


def save_file(f_name, src):
    with open(f_name, 'w') as f:
        f.write(src)

def open_file(f_name):
    with open(f_name, 'r') as f:
        src = f.read()
    return src

def get_user_agent():
    ua = UserAgent()
#    return ua.chrome
    return ua.random
