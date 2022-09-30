from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def index():
    return {"api": "v1"}


@router.get("/health")
def api_health():
    return {"health": True}
