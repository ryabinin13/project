from app.database import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class TeamMemberships(Base):
    
    __tablename__ = "team_memberships"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))