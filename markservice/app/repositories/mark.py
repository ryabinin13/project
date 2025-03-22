from sqlalchemy import delete, select
from app.models.mark import Mark


class MarkRepository:

    def __init__(self, session):
        self.session = session