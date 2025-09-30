from fastapi import APIRouter
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

from app.services import jagriti_client


router = APIRouter()



class CaseSearchRequest(BaseModel):
   

    commission_id: str
    search_value: str
    search_by: str
    from_date: str
    to_date: str
    order_type: Optional[str] = "DAILY ORDER"
    captcha: Optional[str] = None

    @validator("from_date", "to_date", pre=True)
    def normalize_dates(cls, v):
        try:
           
            if "-" in v and len(v.split("-")[0]) == 4:
                return v
            return datetime.strptime(v, "%d-%m-%Y").strftime("%Y-%m-%d")
        except Exception:
            raise ValueError("Date must be in DD-MM-YYYY or YYYY-MM-DD format")




@router.post("/by-case-number")
async def search_by_case_number(req: CaseSearchRequest):
    """🔎 Search cases by **case number**"""
    return await jagriti_client.search_cases(
        commission_id=req.commission_id,
        search_value=req.search_value,
        serch_type=8,  # api code for case number
        from_date=req.from_date,
        to_date=req.to_date,
        order_type=req.order_type,
        captcha_value=req.captcha
    )


@router.post("/by-complainant")
async def search_by_complainant(req: CaseSearchRequest):
    """🔎 Search cases by **complainant’s name**"""
    return await jagriti_client.search_cases(
        commission_id=req.commission_id,
        search_value=req.search_value,
        serch_type=2,  # api code for complainant
        from_date=req.from_date,
        to_date=req.to_date,
        order_type=req.order_type,
        captcha_value=req.captcha
    )


@router.post("/by-respondent")
async def search_by_respondent(req: CaseSearchRequest):
 
    return await jagriti_client.search_cases(
        commission_id=req.commission_id,
        search_value=req.search_value,
        serch_type=3,  # api code for respondent
        from_date=req.from_date,
        to_date=req.to_date,
        order_type=req.order_type,
        captcha_value=req.captcha
    )


@router.post("/by-complainant-advocate")
async def search_by_complainant_advocate(req: CaseSearchRequest):

    return await jagriti_client.search_cases(
        commission_id=req.commission_id,
        search_value=req.search_value,
        serch_type=4,  # api code for complainant advocate
        from_date=req.from_date,
        to_date=req.to_date,
        order_type=req.order_type,
        captcha_value=req.captcha
    )


@router.post("/by-respondent-advocate")
async def search_by_respondent_advocate(req: CaseSearchRequest):
    """🔎 Search cases by **respondent’s advocate**"""
    return await jagriti_client.search_cases(
        commission_id=req.commission_id,
        search_value=req.search_value,
        serch_type=5,  # api code for respondent advocate
        from_date=req.from_date,
        to_date=req.to_date,
        order_type=req.order_type,
        captcha_value=req.captcha
    )


@router.post("/by-industry-type")
async def search_by_industry_type(req: CaseSearchRequest):
    """🔎 Search cases by **industry type**"""
    return await jagriti_client.search_cases(
        commission_id=req.commission_id,
        search_value=req.search_value,
        serch_type=6,  # api code for industry type
        from_date=req.from_date,
        to_date=req.to_date,
        order_type=req.order_type,
        captcha_value=req.captcha
    )


@router.post("/by-judge")
async def search_by_judge(req: CaseSearchRequest):
    """🔎 Search cases by **judge’s name**"""
    return await jagriti_client.search_cases(
        commission_id=req.commission_id,
        search_value=req.search_value,
        serch_type=7,  # API code for judge
        from_date=req.from_date,
        to_date=req.to_date,
        order_type=req.order_type,
        captcha_value=req.captcha
    )
