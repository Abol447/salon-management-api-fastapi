import requests

from app.core.config import settings


class SMSService:

    @staticmethod
    def send_password(phone_number: str, password: str):

        url = "https://api.iranpayamak.com/ws/v1/sms/simple"

        headers = {
            "Accept": "application/json",
            "Api-Key": settings.FARAZ_SMS_API_KEY,
            "Content-Type": "application/json",
        }

        payload = {
            "text": f"رمز عبور شما: {password}",
            "line_number": "90008361",
            "recipients": [phone_number],
            "number_format": "persian",
            "schedule": None,
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=10,
        )

        print("SMS STATUS:", response.status_code)
        print("SMS RESPONSE:", response.text)

        response.raise_for_status()

        return response.json()
