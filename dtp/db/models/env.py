# -*- coding: utf-8 -*-
from dtp.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get)
import uuid
import datetime
from dtp.db.models.namespace import Namespace

class Env(db.Entity):
    _table_ = "dtp_env"

    id = PrimaryKey(int, auto=True)
    uid = Required(uuid.UUID, default=uuid.uuid1, unique=True, index=True)
    env = Required(str, index=True)
    info = Required(Json, index=True)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    user = Required(str, index=True)
    delete_flag = Required(bool, default=False)
    namespace = Required(Namespace)
    source = Set("Envsource")
    testcase = Set("TestCase")

    @classmethod
    @db_session
    def create(cls, namespace, body, info={}):
        env = body.get("name")
        user =body.get("user")
        namespace_obj = Namespace.get(name=namespace, delete_flag=False)
        if namespace_obj:
            env_object = get(a for a in Env if a.env == env and a.delete_flag == "f" and
                             a.namespace.name == namespace and a.namespace.delete_flag == "f")
            if env_object:
                return {
                    "code": 500,
                    "msg": "创建环境已经存在"
                }
            else:
                try:
                    Env(env=env, user=user, info=info, namespace=namespace_obj.id)
                except Exception as e:
                    print(e)
                    return {
                        "code": 500,
                        "msg": "创建环境失败"
                    }
                return {
                    "code": 200,
                    "msg": "创建环境成功"
                }
        else:
            return {
                "code": 500,
                "msg": "Namespace不存在"
            }

    @classmethod
    @db_session
    def list(cls, namespace):
        env_objs = select(a for a in Env if a.namespace.name == namespace and a.namespace.delete_flag == "f")
        data = []
        for env in env_objs:
            tmp = {}
            tmp["env"] = env.env
            tmp["user"] = env.user
            tmp["uid"] = str(env.uid)
            data.append(tmp)
        return {
            "code": 200,
            "data": data,
        }




