from app.models.team_memberships import TeamMemberships


class TeamMembershipRepository:

    def __init__(self, session):
        self.session = session

    async def create(self, data: dict):
        async with self.session as db:
            team = TeamMemberships(**data)
            db.add(team)

            await db.commit() 

            return team.user_id