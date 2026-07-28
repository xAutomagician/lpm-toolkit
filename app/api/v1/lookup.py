from ipaddress import IPv4Address
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.v1.auth import require_api_token
from app.domain import PrefixInfo
from app.repository import IPrefixRepository


router = APIRouter()


def get_prefix_repository(request: Request) -> IPrefixRepository:
    return request.app.state.prefix_repository


@router.get(
    "/lookup/{ip}",
    response_model=PrefixInfo,
    dependencies=[Depends(require_api_token)],
)
def get_ip_lookup(
    ip: IPv4Address,
    repository: Annotated[IPrefixRepository, Depends(get_prefix_repository)],
) -> PrefixInfo:
    prefix_info = repository.get(str(ip))

    if prefix_info is None:
        raise HTTPException(status_code=404, detail="IP prefix not found")

    return prefix_info
