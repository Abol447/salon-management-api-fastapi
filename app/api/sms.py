from fastapi import APIRouter
import requests

router = APIRouter(prefix="/sms", tags=["SMS"])


@router.post("/test")
def send_test_sms():

    url = "https://api.iranpayamak.com/ws/v1/sms/simple"

    headers = {
        "Accept": "application/json",
        "Api-Key": "jPBGZGZgfcC5VdetjHC6gCgTRu6HwT1mG0wly9kvTxgGBpFBtv",
    }

    payload = {
        "text": "سلام، این یک پیامک آزمایشی است.",
        "line_number": "90008361",
        "recipients": ["09054414023"],
        "number_format": "english",
        "schedule": None,
    }

    response = requests.post(url, json=payload, headers=headers)

    return {
        "status_code": response.status_code,
        "response": response.json() if response.text else None,
    }
