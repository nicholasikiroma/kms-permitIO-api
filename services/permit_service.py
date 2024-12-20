from typing import Optional
from fastapi import HTTPException, status
from fastapi.logger import logger
from permit import Permit, TenantRead, UserRead, RoleAssignmentRead, PermitApiError
from .. import settings


permit = Permit(
    pdp="http://localhost:7000",
    token=settings.permit_api_key,
)
permit_client = permit.api


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
    """Checks if user has the right permission to access resource"""
    return await permit.check(
        {"key": user_id}, action, {"type": resource, "tenant": tenant_id}
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
