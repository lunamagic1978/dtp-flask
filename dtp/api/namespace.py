# -*- coding: utf-8 -*-
from dtp.db.models.namespace import Namespace
import json

def post(body):
    result = Namespace.create(body)
    return json.dumps(result, ensure_ascii=False, indent=2)

def get():
    result = Namespace.list()
    return json.dumps(result, ensure_ascii=False, indent=2)