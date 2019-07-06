# -*- coding: utf-8 -*-
from dtp.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, get)
import uuid
import datetime
import json
import yaml
from dtp.db.models.project import Project
from dtp.db.models.namespace import Namespace

class Ref(db.Entity):
    _table_ = "dtp_ref"

    id = PrimaryKey(int, auto=True)
    uid = Required(uuid.UUID, default=uuid.uuid1, unique=True, index=True)
    name = Required(str, index=True)
    swagger_type = Required(str, index=True)
    project = Required(Project)
    info = Required(Json, index=True)
    path = Required(str, index=True)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    user = Required(str, index=True)
    delete_flag = Required(bool, default=False)
    swagger_json = Required(Json, index=True)
    ref_json = Required(Json, index=True)


    @classmethod
    @db_session
    def create(cls, namespace, project, body, info={}):
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
        user = body.get("user")
        for first , v1 in swagger.items():
            for second , v2 in v1.items():
                for third , v3 in v2.items():
                    path = "{}/{}/{}".format(first, second, third)
                    ref_query = get(a for a in Ref if a.delete_flag == "f" and a.project.name == project
                                and a.project.delete_flag =="f" and a.project.namespace.name == namespace
                                and a.project.namespace.delete_flag == "f" and a.path == path )
                    if ref_query:
                        print("need updata")
                    else:
                        try:
                            project_obj = get(p for p in Project if p.delete_flag == "f" and p.name == project and
                                              p.namespace.name == namespace and p.namespace.delete_flag == "f")
                            Ref(name=path, swagger_type=body.get("swagger_type"), project=project_obj.id, info=info,
                                path=path, user=user, swagger_json=swagger_json, ref_json=v3)
                        except Exception as e:
                            print(e)
                            return {
                                "code": 500,
                                "msg": "创建ref失败"
                            }
        return{"code": 200,
               "msg": "创建ref成功"}

    @classmethod
    @db_session
    def list(cls, namespace, project, info={}):
        ref_query = select(a for a in Ref if a.delete_flag == "f" and a.project.name == project
                           and a.project.delete_flag == "f" and a.project.namespace.name == namespace
                           and a.project.namespace.delete_flag == "f")
        data = []
        for ref in ref_query:
            tmp = {}
            tmp["path"] = ref.path
            content = json.dumps(ref.ref_json)
            tmp["content"] = yaml.safe_dump(json.loads(content), default_flow_style=False)
            data.append(tmp)
        return {
            "code": 200,
            "data": data,
        }