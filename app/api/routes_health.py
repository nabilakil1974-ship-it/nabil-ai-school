from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """للتأكد إنو السيرفر شغّال بعد النشر."""
    return {"status": "ok", "service": "NabilAI backend"}
