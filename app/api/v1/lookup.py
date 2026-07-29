from fastapi import APIRouter, Request


router = APIRouter()


@router.get("/lookup/{ip}")
def get_ip_lookup(ip: str, request: Request):
    service = request.app.state.lookup_service
    return service.lookup_ip(ip)
