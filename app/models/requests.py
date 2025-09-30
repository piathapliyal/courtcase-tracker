from pydantic import BaseModel

class CaseSearchRequest(BaseModel):
  
    commission_id: str
    search_value: str
    state: str | None = None
    commission: str | None = None
