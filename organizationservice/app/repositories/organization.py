from app.models.organization import Organization


class OrganizationRepository:
    def __init__(self, session):
        self.session = session



    async def create(self, data: dict):
        async with self.session as db:
            org = Organization(**data)
            db.add(org)

            await db.commit() 

            return org.id