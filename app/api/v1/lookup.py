from ipaddress import IPv4Address

from fastapi import APIRouter, Depends, HTTPException, Request

from app.repository import IPrefixRepository
from app.schemas import PrefixInfo

router = APIRouter(prefix="/lookup")


def get_prefix_repository(request: Request) -> IPrefixRepository:
    return request.app.state.prefix_repository


@router.get("/{ip}", response_model=PrefixInfo)
def get_ip_lookup(
    ip: IPv4Address,
    repository: IPrefixRepository = Depends(get_prefix_repository),
) -> PrefixInfo:
    prefix_info = repository.get(str(ip))
    if prefix_info is None:
        raise HTTPException(status_code=404, detail="IP prefix not found")
    return prefix_info
