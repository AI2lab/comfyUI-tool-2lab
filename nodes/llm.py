import hashlib
import json

from .caller import submit
from .constants import get_project_name, get_project_category, read_user_key,PROJECT_NAME

NODE_CATEGORY = get_project_category("llm")
