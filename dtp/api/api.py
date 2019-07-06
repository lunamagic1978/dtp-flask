from dtp.db.models.api import Api
import json

def post(namespace, project, body):
    result = Api.create(namespace=namespace, project=project, body=body)
    return json.dumps(result, ensure_ascii=False, indent=2)

def get(namespace, project):
    result = Api.list(namespace=namespace, project=project)
    return json.dumps(result, ensure_ascii=False, indent=2)

def detail(namespace, project, path, method):
    result = Api.detail(namespace=namespace, project=project, path=path, method=method)
    return json.dumps(result, ensure_ascii=False, indent=2)

def demo(namespace, project, path, method):
    result = Api.demo(namespace, project, path, method)
    return json.dumps(result, ensure_ascii=False, indent=2)