from fastapi import APIRouter
from app.services import jagriti_client

router = APIRouter()


@router.get("/")
async def list_states():

  
    return await jagriti_client.get_states()


@router.get("/{state_id}/commissions")
async def list_commissions(state_id: str):

    return await jagriti_client.get_commissions(state_id)
