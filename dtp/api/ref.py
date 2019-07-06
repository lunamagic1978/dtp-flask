from dtp.db.models.ref import Ref
import json

def post(namespace, project, body):
    result = Ref.create(namespace=namespace, project=project, body=body)
    return json.dumps(result, ensure_ascii=False, indent=2)

def get(namespace, project):
    result = Ref.list(namespace=namespace, project=project)
    return json.dumps(result, ensure_ascii=False, indent=2)