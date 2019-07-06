# -*- coding: utf-8 -*-
from dtp.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set)
import uuid
import datetime


class Namespace(db.Entity):
    _table_="dtp_namespace"

    id = PrimaryKey(int, auto=True)
    uid = Required(uuid.UUID, default=uuid.uuid1, unique=True, index=True)
    name = Required(str, index=True)
    info = Required(Json, index=True)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    user = Required(str, index=True)
    delete_flag = Required(bool, default=False)
    project = Set("Project")


    @classmethod
    @db_session
    def create(cls, body, info={}):
        name = body.get("name")
        user = body.get("user")
        query = Namespace.get(name=name, delete_flag=False)
        if query:
            return  {
                    "code": 500,
                    "msg": "创建namespace已经存在"
                }
        else:
            try:
                Namespace(name=name, user=user, info=info)
                return {
                    "code": 200,
                    "msg": "创建namespace成功"
                }
            except Exception as e:
                print(e)
                return {
                    "code": 500,
                    "msg": "创建namespace失败"
                }

    @classmethod
    @db_session
    def list(cls):
        query = Namespace.select(lambda name: name.delete_flag == "f").order_by(desc(Namespace.create_at))
        data = []
        for obj in query:
            tmp = {}
            tmp["name"] = obj.name
            tmp["user"] = obj.user
            data.append(tmp)
        return {
                    "code": 200,
                    "data": data,
                }
