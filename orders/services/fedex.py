import requests
from django.conf import settings

FEDEX_AUTH_URL = "https://apis-sandbox.fedex.com/oauth/token"
FEDEX_SHIPMENT_URL = "https://apis-sandbox.fedex.com/ship/v1/shipments"

def get_fedex_access_token():
    """
    Obtain OAuth2 access token from FedEx API.
    """
    data = {
        "grant_type": "client_credentials",
        "client_id": settings.FEDEX_API_KEY,
        "client_secret": settings.FEDEX_API_SECRET,
    }
    response = requests.post(FEDEX_AUTH_URL, data=data)
    response.raise_for_status()
    return response.json()["access_token"]


def create_fedex_shipment(shipment_type, service, declared_value, pickup_time, total_weight, length, width, height):
    """
    Create a FedEx shipment (manifest) and return a label and tracking number (test/sandbox version).
    """
    access_token = get_fedex_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "accountNumber": {"value": settings.FEDEX_ACCOUNT_NUMBER},
        "requestedShipment": {
            "shipper": {
                "address": {
                    "streetLines": ["123 Shipper St"],
                    "city": "Memphis",
                    "stateOrProvinceCode": "TN",
                    "postalCode": "38116",
                    "countryCode": "US"
                }
            },
            "recipient": {
                "address": {
                    "streetLines": ["789 Recipient Ave"],
                    "city": "Orlando",
                    "stateOrProvinceCode": "FL",
                    "postalCode": "32801",
                    "countryCode": "US"
                }
            },
            "pickupType": shipment_type,
            "serviceType": service,
            "packagingType": "YOUR_PACKAGING",
            "totalWeight": {
                "units": "KG",
                "value": float(total_weight)
            },
            "declaredValue": {
                "amount": float(declared_value),
                "currency": "USD"
            },
            "shipTimestamp": pickup_time,
            "requestedPackageLineItems": [
                {
                    "weight": {
                        "units": "KG",
                        "value": float(total_weight)
                    },
                    "dimensions": {
                        "length": int(length),
                        "width": int(width),
                        "height": int(height),
                        "units": "CM"
                    }
                }
            ]
        }
    }
    response = requests.post(FEDEX_SHIPMENT_URL, headers=headers, json=payload)
    response.raise_for_status()
    shipment_data = response.json()
    return shipment_data 