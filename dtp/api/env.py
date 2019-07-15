from dtp.db.models.env import Env
from dtp.db.models.envsource import Envsource
import json

def get(namespace):
    result = Env.list(namespace=namespace)
    return json.dumps(result, ensure_ascii=False, indent=2)

def post(namespace, body):
    result = Env.create(namespace=namespace, body=body)
    return json.dumps(result, ensure_ascii=False, indent=2)


def globalsourcecreate(namespace, env, body):
    result = Envsource.create_global_source(namespace=namespace, env=env, body=body)
    return json.dumps(result, ensure_ascii=False, indent=2)

def globalsourceget(namespace, env):
    result = Envsource.get_global_source(namespace=namespace, env=env)
    return json.dumps(result, ensure_ascii=False, indent=2)

def projectsourcecreate(namespace, project, env, body):
    result = Envsource.create_project_source(namespace=namespace, project=project, env=env, body=body)
    return json.dumps(result, ensure_ascii=False, indent=2)

def projectsourceget(namespace, project, env):
    result = Envsource.get_project_source(namespace=namespace, project=project, env=env)
    return json.dumps(result, ensure_ascii=False, indent=2)