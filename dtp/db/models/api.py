# -*- coding: utf-8 -*-
from dtp.db.db import db
from pony.orm import (Json, PrimaryKey, Required, db_session, select, desc, get)
import uuid
import datetime
import json
import yaml
from dtp.db.models.project import Project
from dtp.db.models.namespace import Namespace
from dtp.db.models.ref import Ref

class Api(db.Entity):
    _table_ = "dtp_api"

    id = PrimaryKey(int, auto=True)
    uid = Required(uuid.UUID, default=uuid.uuid1, unique=True, index=True)
    name = Required(str, index=True)
    swagger_type = Required(str, index=True)
    project = Required(Project)
    info = Required(Json, index=True)
    path = Required(str, index=True)
    method = Required(str, index=True)
    create_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    update_at = Required(datetime.datetime, default=datetime.datetime.utcnow(), index=True)
    user = Required(str, index=True)
    delete_flag = Required(bool, default=False)
    swagger_json = Required(Json, index=True)
    api_json = Required(Json, index=True)

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
        for path ,v  in swagger.get("paths").items():
            for method, swagger_content in v.items():
                api_query = get(a for a in Api if a.delete_flag == "f" and a.project.name == project
                                and a.project.delete_flag =="f" and a.project.namespace.name == namespace
                                and a.project.namespace.delete_flag == "f" and a.path == path and
                                a.method == method)
                if api_query:
                    print("need updata")
                else:
                    api_name = swagger_content.get("summary")

                    try:
                        project_obj = get(p for p in Project if p.delete_flag == "f" and p.name == project and
                                          p.namespace.name == namespace and p.namespace.delete_flag == "f")
                        Api(name=api_name, user=user, project=project_obj.id, path=path, method=method,
                            swagger_json=swagger_json, swagger_type=body.get("swagger_type"), info=info,
                            api_json = swagger_content)

                    except Exception as e:
                        print(e)
                        return {
                            "code": 500,
                            "msg": "创建api失败"
                        }
        return {
            "code": 200,
            "msg": "创建api成功"
        }

    @classmethod
    @db_session
    def list(cls, namespace, project, info={}):
        api_query = select(a for a in Api if a.delete_flag == "f" and a.project.name == project
                           and a.project.delete_flag =="f" and a.project.namespace.name == namespace
                           and a.project.namespace.delete_flag == "f")
        data = []
        for api in api_query:
            tmp = {}
            tmp["name"] = api.name
            tmp["path"] = api.path
            tmp["mehtod"] = api.method
            tmp["uid"] = str(api.uid)
            data.append(tmp)
        return {
                    "code": 200,
                    "data": data,
                }

    @classmethod
    @db_session
    def one(cls, namespace, project, api_uid):
        uid = uuid.UUID(api_uid)
        api_query = get(a for a in Api if a.delete_flag == "f" and a.project.name == project and a.uid == uid
                           and a.project.delete_flag =="f" and a.project.namespace.name == namespace
                           and a.project.namespace.delete_flag == "f")
        tmp = json.dumps(api_query.api_json)
        content = json.loads(tmp)



        def swagger_ref(content):
            if isinstance(content, dict):
                for k, v in content.items():
                    if isinstance(v, dict):
                        tmp = v.get("$ref")
                        if tmp:
                            ref_name = tmp[2:]
                            ref = get(a for a in Ref if a.delete_flag == "f" and a.project.name == project
                                         and a.project.delete_flag == "f" and a.project.namespace.name == namespace
                                         and a.project.namespace.delete_flag == "f" and a.name == ref_name)
                            content[k] = ref.ref_json
                    swagger_ref(v)
        swagger_ref(content=content)
        return {
                    "code": 200,
                    "data": content,
                }

    @classmethod
    @db_session
    def detail(cls, namespace, project, path, method):

        api_query = get(a for a in Api if a.delete_flag == "f" and a.project.name == project and a.path == path
                           and a.project.delete_flag =="f" and a.project.namespace.name == namespace
                           and a.project.namespace.delete_flag == "f" and a.method == method)
        tmp = json.dumps(api_query.api_json)
        content = json.loads(tmp)



        def swagger_ref(content):
            if isinstance(content, dict):
                for k, v in content.items():
                    if isinstance(v, dict):
                        tmp = v.get("$ref")
                        if tmp:
                            ref_name = tmp[2:]
                            ref = get(a for a in Ref if a.delete_flag == "f" and a.project.name == project
                                         and a.project.delete_flag == "f" and a.project.namespace.name == namespace
                                         and a.project.namespace.delete_flag == "f" and a.name == ref_name)
                            content[k] = ref.ref_json
                    swagger_ref(v)
        swagger_ref(content)
        return {
                    "code": 200,
                    "data": content,
                }

    @classmethod
    @db_session
    def demo(cls, namespace,  project, path, method):
        print(namespace, project, path, method)
        re_dict = {}
        project_query = get(a for a in Project if a.delete_flag == "f" and a.name == project
                            and a.namespace.delete_flag == "f" and a.namespace.name == namespace)
        tmp = json.loads(project_query.swagger_json)
        re_dict.update(tmp)
        api_query = get(a for a in Api if a.project.delete_flag == "f" and a.project.name == project and
                        a.project.namespace.name == namespace and a.project.namespace.delete_flag == "f" and
                        a.delete_flag == "f" and a.path == path and a.method == method)
        tmp = json.dumps(api_query.api_json)
        tmp = json.loads(tmp)
        tmp_dict = {"paths": { path: { method: tmp}}}
        re_dict.update(tmp_dict)

        ref_querys = select(a for a in Ref if a.project.delete_flag == "f" and a.project.name == project and
                        a.project.namespace.name == namespace and a.project.namespace.delete_flag == "f" and
                        a.delete_flag == "f")
        ref_querys.show()
        tmp_dict = {"components": {"schemas": {}}}
        for ref in ref_querys:
            tmp_name = ref.name
            tmp_name_list = tmp_name.split("/")
            tmp_dict["components"]["schemas"][tmp_name_list[2]] = ref.ref_json
        re_dict.update(tmp_dict)
        return re_dict



