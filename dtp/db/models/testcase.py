# -*- coding: utf-8 -*-
from dtp.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, get)
import uuid
import datetime
from dtp.db.models.api import Api
from dtp.db.models.env import Env

class TestCase(db.Entity):
    _table_ = "dtp_testcase"

    id = PrimaryKey(int, auto=True)
    uid = Required(uuid.UUID, default=uuid.uuid1, unique=True, index=True)
    name = Required(str, index=True)
    api = Required(Api)
    env = Required(Env)