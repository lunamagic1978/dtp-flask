# -*- coding: utf-8 -*-
from dtp.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get)
import uuid
import datetime
from dtp.db.models.env import Env
from dtp.db.models.project import Project
import json

class Envsource(db.Entity):
    _table_ = "dtp_envsource"

    id = PrimaryKey(int, auto=True)
    uid = Required(uuid.UUID, default=uuid.uuid1, unique=True, index=True)
    info = Required(Json, index=True)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    user = Required(str, index=True)
    delete_flag = Required(bool, default=False)
    env= Required(Env)
    env_data = Required(Json, index=True)
    env_metadata = Required(Json, index=True)
    env_type = Required(int, index=True)

    @classmethod
    @db_session
    def create_global_source(cls, namespace, env, body, info={}):
        user = body.get("user")
        metadate = body.get("metadate")
        json_metadate = json.loads(metadate)
        data = {}
        for date in json_metadate:
            if date.get("selected"):
                data[date.get("key")] = date.get("value")
        global_obj = get(a for a in Envsource if a.env.env == env and a.env.delete_flag == 'f' and
                         a.env.namespace.name == namespace and a.env.namespace.delete_flag == 'f' and
                         a.env_type == 0)
        env_obj = get(a for a in Env if a.env == env and a.delete_flag == 'f' and
                      a.namespace.name == namespace and a.namespace.delete_flag == 'f')
        if global_obj:
            try:
                global_obj.env_data = data
                global_obj.env_metadata = metadate
                return {
                    "code": 200,
                    "msg": "更新{}环境的全局变量成功".format(env)
                }
            except Exception as e:
                print(e)
                return {
                    "code": 500,
                    "msg": "更新{}环境的全局变量失败".format(env)
                }
        else:
            try:
                Envsource(info=info, user=user, env=env_obj.id, env_data=data, env_metadata=metadate, env_type=0)
                return {
                    "code": 200,
                    "msg": "创建{}环境的全局变量成功".format(env)
                }
            except Exception as e:
                print(e)
                return {
                    "code": 500,
                    "msg": "创建{}环境的全局变量失败".format(env)
                }

    @classmethod
    @db_session
    def get_global_source(cls, namespace, env):
        global_obj = get(a for a in Envsource if a.env.env == env and a.env.delete_flag == 'f' and
                         a.env.namespace.name == namespace and a.env.namespace.delete_flag == 'f' and
                         a.env_type == 0)
        if global_obj:
            metadate = global_obj.env_metadata
            data = json.loads(metadate)
        else:
            data = []

        return {
                    "code": 200,
                    "data": data
                }

    @classmethod
    @db_session
    def create_project_source(cls, namespace, project, env, body, info={}):
        user = body.get("user")
        metadate = body.get("metadate")
        json_metadate = json.loads(metadate)
        data = {}
        for date in json_metadate:
            if date.get("selected"):
                data[date.get("key")] = date.get("value")

        project_obj = get(a for a in Project if a.name == project and a.delete_flag == 'f' and
                          a.namespace.name == namespace and a.namespace.delete_flag == 'f')
        global_obj = get(a for a in Envsource if a.env.env == env and a.env.delete_flag == 'f' and
                         a.env.namespace.name == namespace and a.env.namespace.delete_flag == 'f' and
                         a.env_type == project_obj.id)
        env_obj = get(a for a in Env if a.env == env and a.delete_flag == 'f' and
                      a.namespace.name == namespace and a.namespace.delete_flag == 'f')
        if global_obj:
            try:
                global_obj.env_data = data
                global_obj.env_metadata = metadate
                return {
                    "code": 200,
                    "msg": "更新{}环境的全局变量成功".format(env)
                }
            except Exception as e:
                print(e)
                return {
                    "code": 500,
                    "msg": "更新{}环境的全局变量失败".format(env)
                }
        else:
            try:
                Envsource(info=info, user=user, env=env_obj.id, env_data=data, env_metadata=metadate, env_type=project_obj.id)
                return {
                    "code": 200,
                    "msg": "创建{}环境的全局变量成功".format(env)
                }
            except Exception as e:
                print(e)
                return {
                    "code": 500,
                    "msg": "创建{}环境的全局变量失败".format(env)
                }

    @classmethod
    @db_session
    def get_project_source(cls, namespace, project, env):
        project_obj = get(a for a in Project if a.name == project and a.delete_flag == 'f' and
                          a.namespace.name == namespace and a.namespace.delete_flag == 'f')
        global_obj = get(a for a in Envsource if a.env.env == env and a.env.delete_flag == 'f' and
                         a.env.namespace.name == namespace and a.env.namespace.delete_flag == 'f' and
                         a.env_type == project_obj.id)
        if global_obj:
            metadate = global_obj.env_metadata
            data = json.loads(metadate)
        else:
            data = []

        return {
                    "code": 200,
                    "data": data
                }
