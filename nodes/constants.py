# NAMESPACE
import os
from pathlib import Path

PROJECT_NAME= '2lab'

def get_project_name(name):
    return '{} ({})'.format(name, PROJECT_NAME)

def get_project_category(sub_dirs = None):
    start = "🦊" + PROJECT_NAME
    if sub_dirs is None:
        return start
    else:
        return "{}/{}".format(start,sub_dirs)

# PATH
project_root = Path(__file__).parent.parent
temp_folder = os.path.join(project_root,"temp")
# print("project_root = ",project_root)