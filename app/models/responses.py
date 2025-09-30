from pydantic import BaseModel
from typing import Optional

class CaseResponse(BaseModel):
    """
    Output model for one case entry.
    Matches exactly what we want to expose in API responses.
    """
    case_number: str
    case_stage: Optional[str] = None
    filing_date: Optional[str] = None
    complainant: Optional[str] = None
    complainant_advocate: Optional[str] = None
    respondent: Optional[str] = None
    respondent_advocate: Optional[str] = None
    document_link: Optional[str] = None
