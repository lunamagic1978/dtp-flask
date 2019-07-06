from dtp.db.models.project import Project
import json

def post(namespace, body):
    result = Project.create(namespace=namespace, body=body)
    return json.dumps(result, ensure_ascii=False, indent=2)

def get(namespace):
    result = Project.list(namespace)
    return json.dumps(result, ensure_ascii=False, indent=2)

def detail(namespace, project):
    result = Project.project(namespace, project)
    return json.dumps(result, ensure_ascii=False, indent=2)

def update(namespace, project, body):
    result = Project.update(namespace, project, body)
    return json.dumps(result, ensure_ascii=False, indent=2)