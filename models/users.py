from sqlalchemy import Boolean, Column, String, DateTime, func, ForeignKey, Enum, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from enum import Enum as PyEnum

from ..models.tenants import Tenants  # Assuming tenants are still in use
from .base import BaseModel


class UserRoles(PyEnum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class Users(BaseModel):
    __tablename__ = "users"

    workspaces = Column(ARRAY(UUID(as_uuid=True)), nullable=False)
    active_workspace = Column(
        UUID(as_uuid=True),
        ForeignKey(Tenants.id),
        nullable=False,
    )
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRoles), name="user_roles", default=UserRoles.VIEWER)

    # Relationships
    knowledge_articles = relationship(
        "KnowledgeArticles", back_populates="author", cascade="all, delete-orphan"
    )

    # Utility Methods
    def set_active_workspace(self, workspace_id):
        """Set the active workspace for the user."""
        if workspace_id in self.workspaces:
            self.active_workspace = workspace_id
        else:
            raise ValueError("Workspace ID is not associated with this user.")

    def add_workspace(self, workspace_id):
        """Add a new workspace to the user's list."""
        if workspace_id not in self.workspaces:
            self.workspaces.append(workspace_id)

    def remove_workspace(self, workspace_id):
        """Remove a workspace from the user's list."""
        if workspace_id in self.workspaces:
            self.workspaces.remove(workspace_id)
            # Reset active workspace if the removed workspace was active
            if self.active_workspace == workspace_id:
                self.active_workspace = self.workspaces[0] if self.workspaces else None
        else:
            raise ValueError("Workspace ID is not associated with this user.")
