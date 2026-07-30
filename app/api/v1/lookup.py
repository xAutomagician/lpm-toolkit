from fastapi import APIRouter, HTTPException, Request


router = APIRouter()


@router.get("/lookup/{ip}")
def get_ip_lookup(ip: str, request: Request):
    repository = request.app.state.prefix_repository

    try:
        prefix_info = repository.get(ip)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if prefix_info is None:
        raise HTTPException(status_code=404, detail="IP prefix not found")

    return prefix_info.to_dict()
