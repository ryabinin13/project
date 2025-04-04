from app.repositories.organization import OrganizationRepository
from app.repositories.organization_membersips import OrganizationMembershipsRepository
from app.schemas.organization import AddOrganizationSchema


class OrganizationService:
    def __init__(self, org_repository: OrganizationRepository, org_memberships_repository: OrganizationMembershipsRepository, app_state):
        self.org_repository = org_repository
        self.org_memberships_repository = org_memberships_repository
        self.app_state = app_state


    async def create_org(self, add_ord_schema: AddOrganizationSchema):
        if not add_ord_schema.parent_id:
            await self.app_state.broker_producer_service.publish_team_id(str(add_ord_schema.team_id) + " " + str(add_ord_schema.name))