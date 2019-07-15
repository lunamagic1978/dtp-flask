# -*- coding: utf-8 -*-
from dtp.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, Set, get)
import uuid
import datetime
import json
import yaml
from dtp.db.models.namespace import Namespace



class Project(db.Entity):
    _table_ = "dtp_project"

    id = PrimaryKey(int, auto=True)
    uid = Required(uuid.UUID, default=uuid.uuid1, unique=True, index=True)
    name = Required(str, index=True)
    namespace = Required(Namespace)
    info = Required(Json, index=True)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    user = Required(str, index=True)
    delete_flag = Required(bool, default=False)
    swagger_json = Required(Json, index=True)
    api = Set("Api")
    ref = Set("Ref")


    @classmethod
    @db_session
    def create(cls, namespace, body, info={}):
        try:
            swagger_yaml = body.get("swagger_json")
            swagger = yaml.load(swagger_yaml)
            swagger_json = json.dumps(swagger)
        except Exception as e:
            print(e)
            return {
                "code": 500,
                "msg": "yaml格式不正确，请检查"
            }
        name = swagger.get("info").get("title")
        user = body.get("user")
        namespace_obj = Namespace.get(name=namespace, delete_flag=False)
        if namespace_obj:
            query = Project.get(name=name, namespace=namespace_obj.id, delete_flag=False)
            if query:
                return {
                    "code": 500,
                    "msg": "创建project已经存在"
                }
            else:
                try:
                    Project(name=name, user=user, info=info, namespace=namespace_obj.id, swagger_json=swagger_json)
                    return {
                        "code": 200,
                        "msg": "创建project成功"
                    }
                except Exception as e:
                    print(e)
                    return {
                        "code": 500,
                        "msg": "创建project失败"
                    }
        else:
            return {
                "code": 500,
                "msg": "Namespace不存在"
            }

    @classmethod
    @db_session
    def list(cls, namespace):
        project_objs = select(p for p in Project if p.delete_flag == "f" and p.namespace.name == namespace ).order_by(desc(Project.create_at))
        data = []
        for obj in project_objs:
            tmp = {}
            tmp["name"] = obj.name
            tmp["user"] = obj.user
            data.append(tmp)
        return {
                    "code": 200,
                    "data": data,
                }

    @classmethod
    @db_session
    def project(cls, namespace, project):
        try:
            obj = get(p for p in Project if p.delete_flag == "f" and p.name == project and
                      p.namespace.delete_flag == "f" and p.namespace.name == namespace)
            content = json.loads(obj.swagger_json)
            return {
                "code": 200,
                "data": content
            }
        except Exception as e:
            return {
                "code": 500,
                "msg": "查询的project({})不存在".format(project)
            }


    @classmethod
    @db_session
    def update(cls, namespace, project, body):
        swagger_json = body.get("swagger_json")
        try:
            obj = get(p for p in Project if p.namespace.delete_flag == "f" and p.namespace.name == namespace
                      and p.name == project and p.delete_flag == "f")
        except Exception as e:
            return {
                "code": 500,
                "msg": "Project不存在，请检查"
            }
        content = json.loads(swagger_json)
        name = content.get("info").get("title")

        check_name = get(p for p in Project if p.namespace.delete_flag == "f" and p.namespace.name == namespace
                      and p.name == name and p.delete_flag == "f")

        if check_name:
            obj.swagger_json = swagger_json
            return {
                "code": 200,
                "msg": "编辑成功"
            }
        else:
            obj.swagger_json = swagger_json
            obj.name = name
            return {
                "code": 200,
                "msg": "编辑成功"
            }