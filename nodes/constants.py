NAMESPACE='2lab'

def get_name(name):
    return '{} ({})'.format(name, NAMESPACE)

def get_category(sub_dirs = None):
    start = "🦊"+NAMESPACE
    if sub_dirs is None:
        return start
    else:
        return "{}/{}".format(start,sub_dirs)