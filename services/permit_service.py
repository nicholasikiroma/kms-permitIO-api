from typing import Optional
from fastapi import HTTPException, status
from fastapi.logger import logger
from permit import Permit, TenantRead, UserRead, RoleAssignmentRead, PermitApiError
from enum import Enum

from .. import settings


permit = Permit(
    pdp=settings.permit_pdp,
    token=settings.permit_api_key,
)
permit_client = permit.api


class Actions(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    PUBLISH = "publish"
    READ = "read"


async def create_permit_user(user_id: str, tenant_id: str, role):
    """Create a user"""
    try:

        new_user: UserRead = await permit.write(
            permit_client.sync_user(
                {"key": user_id, "tenant_id": tenant_id, "role": role}
            ),
            permit_client.assign_role(user_id, role, tenant_id),
        )

    except PermitApiError as e:
        logger.error(msg=e, stack_info=True)
        if e.status_code == 409:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status": "fail",
                    "data": {"key": "A user with this key already exists"},
                },
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Unable to create user or permission",
            },
        )

    return new_user


async def check_user_permission(
    user_id: str,
    action: str,
    tenant_id: str,
    resource: str = "article",
) -> bool:
    """Checks if user has the right permission to access resource.

    Args:
        user_id (str): The unique identifier of the user
        action (str): The action being performed (e.g., "read", "write")
        tenant_id (str): The tenant identifier
        resource (str, optional): The resource type. Defaults to "article"

    Returns:
        bool: True if user has permission, False otherwise

    Raises:
        HTTPException: If permission check fails
    """
    try:
        return await permit.check(
            {"key": user_id}, action, {"type": resource, "tenant": tenant_id}
        )
    except PermitApiError as e:
        logger.error(f"Permission check failed for user {user_id}", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"status": "error", "message": "Permission check failed"},
        )


async def create_tenant(name: str, tenant_id: str, description: Optional[str]):
    """Creates a tenant"""
    try:
        tenant: TenantRead = await permit_client.tenants.create(
            {"key": tenant_id, "name": name, "description": description}
        )
        return tenant

    except PermitApiError as e:
        logger.error(msg=e, stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Unable to create tenant",
            },
        )


async def update_user_role(user_id: str, tenant_id: str, role: str):
    """update user role"""
    try:
        role_assignment: RoleAssignmentRead = await permit_client.users.assign_role(
            user_id, role, tenant_id
        )
        return role_assignment

    except PermitApiError as e:
        logger.error(msg=e, stack_info=True)
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "status": "error",
                "message": e.message,
            },
        )
