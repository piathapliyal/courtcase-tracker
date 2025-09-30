import httpx
import logging
import json
from pathlib import Path
import base64

# -------------------------------------------------
# Setup
# -------------------------------------------------
# Logger for this module
logger = logging.getLogger(__name__)

# Base URL for the Jagriti API
BASE_URL = "https://e-jagriti.gov.in/services"

# Local JSON file used as fallback if API blocks requests
COMMISSIONS_FILE = Path(__file__).resolve().parent.parent / "data" / "commissions.json"


# -------------------------------------------------
# Utility: Load commissions from local JSON
# -------------------------------------------------
def load_commissions_from_file(state_id: str):
    """
    Reads commissions.json and returns all commissions for a given state.
    This is a fallback option if API requests are blocked (403).
    """
    try:
        with open(COMMISSIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(state_id, [])
    except Exception as e:
        logger.error(f"Couldn’t load commissions.json: {e}")
        return []


# -------------------------------------------------
# 1. Fetch all States
# -------------------------------------------------
async def get_states():
    """
    Get a list of all states from Jagriti API.
    Returns: list of {state_id, state_name}
    """
    url = f"{BASE_URL}/getStateCommissionAndCircuitBench"

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)

            # Handle blocked request
            if resp.status_code == 403:
                logger.error("Access denied (403) while fetching states.")
                return {"error": "403 Forbidden – API blocked the request"}

            # Parse response
            try:
                data = resp.json()
            except Exception as e:
                snippet = resp.text[:200]
                logger.error(f"Invalid JSON while fetching states: {e}")
                return {"error": "Invalid response format from Jagriti", "raw_preview": snippet}

            # Extract states
            states = [
                {"state_id": item.get("commissionId"), "state_name": item.get("stateName")}
                for item in data
            ]
            logger.info(f"Fetched {len(states)} states successfully")
            return states

    except Exception as e:
        logger.exception("Unexpected error while fetching states")
        return {"error": f"Unexpected error in get_states(): {e}"}


# -------------------------------------------------
# 2. Fetch commissions for a state
# -------------------------------------------------
async def get_commissions(state_id: str):
    """
    Get all district commissions for a given state.
    Input: state_id (string, e.g. "11280000")
    Returns: list of {commission_id, commission_name}
    """
    url = f"{BASE_URL}/report/report/getDistrictCommissionByCommissionId"
    params = {"commissionId": state_id}

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)

           
            if resp.status_code == 403:
                logger.warning(f"API blocked. Using local commissions.json for state {state_id}")
                return load_commissions_from_file(state_id)

            try:
                data = resp.json()
            except Exception as e:
                snippet = resp.text[:200]
                logger.error(f"Invalid JSON while fetching commissions: {e}")
                return {"error": "Invalid response format from Jagriti", "raw_preview": snippet}

            commissions = [
                {"commission_id": item.get("commissionId"), "commission_name": item.get("commissionName")}
                for item in data
            ]
            logger.info(f"Fetched {len(commissions)} commissions for state {state_id}")
            return commissions

    except Exception as e:
        logger.exception("Unexpected error while fetching commissions")
        return {"error": f"Unexpected error in get_commissions(): {e}"}




async def search_cases(
    commission_id: str,
    search_value: str,
    from_date="01-01-2025",
    to_date="30-09-2025",
    serch_type=2, 
    order_type="DAILY ORDER",
    captcha_value="ABC123" 
):
    """
    Search cases in a specific commission by complainant/respondent name.
    
    Args:
        commission_id: ID of the commission (int/string).
        search_value: Name or value to search for.
        from_date, to_date: Filter by case filing date range.
        serch_type: What to search by (2=complainant, 3=respondent, etc.)
        order_type: Filter for type of order (default "DAILY ORDER").
        captcha_value: Placeholder (not currently used, Jagriti needs manual CAPTCHA).
    
    Returns:
        List of formatted case dictionaries with details and document links.
    """
    url = f"{BASE_URL}/case/caseFilingService/v2/getCaseDetailsBySearchType"

    payload = {
        "commissionId": int(commission_id),
        "page": 0,
        "size": 30,
        "fromDate": from_date,
        "toDate": to_date,
        "dateRequestType": 1,  
        "judgeId": "",
        "serchType": serch_type,
        "serchTypeValue": search_value
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json",
        "Referer": "https://e-jagriti.gov.in/advance-case-search",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        logger.debug(f"Sending payload: {json.dumps(payload, indent=2)}")

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, json=payload, headers=headers)

            if resp.status_code == 403:
                return {"error": "403 Forbidden – API blocked the request"}
            if resp.status_code == 400:
                return {"error": "400 Bad Request – Check payload fields"}

           
            try:
                json_resp = resp.json()
                raw_data = json_resp.get("data", []) if isinstance(json_resp, dict) else json_resp
                if raw_data is None:
                    raw_data = []
            except Exception as e:
                snippet = resp.text[:200]
                logger.error(f"Invalid JSON in search_cases: {e}")
                return {"error": "Invalid response format from Jagriti", "raw_preview": snippet}

            logger.info(f"Found {len(raw_data)} records (type={serch_type}, value={search_value})")

            formatted = []
            for item in raw_data:
                if isinstance(item, dict):
                    # only keep if document exists (pdf or base64)
                    if not (item.get("orderDocumentPath") or item.get("documentBase64")):
                        continue

                    formatted.append({
                        "case_number": item.get("caseNumber"),
                        "case_stage": item.get("caseStageName"),
                        "filing_date": item.get("caseFilingDate"),
                        "complainant": item.get("complainantName"),
                        "complainant_advocate": item.get("complainantAdvocateName"),
                        "respondent": item.get("respondentName"),
                        "respondent_advocate": item.get("respondentAdvocateName"),
                        "document_link": item.get("orderDocumentPath"),  # pdf link if available
                    })
                else:
                    formatted.append({"raw": item}) 

            return formatted

    except Exception as e:
        logger.exception("Unexpected error in search_cases")
        return {"error": f"Unexpected error in search_cases(): {e}"}
