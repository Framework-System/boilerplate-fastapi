from datetime import datetime
from typing import Dict

from fastapi import APIRouter

# Define the API router for user models.
router = APIRouter()


@router.get("/health-check")
def health_check() -> Dict[str, str]:
    """
    Checks the health of the application.

    :returns: Status of the health check.
    """
    return {
        "message": "Health check successful",
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
    }
