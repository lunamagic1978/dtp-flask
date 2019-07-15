import connexion
from flask_cors import CORS
from dtp.db.models.project import Project  # noqa: F401
from dtp.db.models.namespace import Namespace # noqa: F401
from dtp.db.models.api import Api # noqa: F401
from dtp.db.models.ref import Ref # noqa: F401
from dtp.db.models.env import Env # noqa: F401
from dtp.db.models.envsource import Envsource # noqa: F401
from dtp.db.models.testcase import TestCase # noqa: F401
from dtp.db.db import db


if __name__ == '__main__':
    db.generate_mapping(create_tables=True)
    app = connexion.FlaskApp(__name__, port=9090, specification_dir='specs/')
    CORS(app.app)
    app.add_api('namespace.yaml', arguments={'title': 'namespace'})
    app.run(host='0.0.0.0', debug=True)
