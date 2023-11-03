from datetime import datetime, timedelta
import os
from typing import Union, Any
from jose import jwt
from uuid import uuid4

from ..core import config
from ..db.db import RedisDB


def generate_jti():
    return str(uuid4().hex)


jti = generate_jti()


