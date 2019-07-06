
from dtp.db.models.namespace import Namespace # noqa: F401
from dtp.db.models.project import Project  # noqa: F401

from dtp.db.db import db


if __name__ == "__main__":
    db.generate_mapping(create_tables=True)