import requests
from django.conf import settings
import json

FEDEX_AUTH_URL = settings.FEDEX_AUTH_URL
FEDEX_SHIPMENT_URL = settings.FEDEX_SHIPMENT_URL

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
    access_token = get_fedex_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "accountNumber": {"value": settings.FEDEX_ACCOUNT_NUMBER},
        "requestedShipment": {
            "shipper": {
                "contact": {
                    "personName": "Your Real Name",
                    "phoneNumber": "Your Real Phone"
                },
                "address": {
                    "streetLines": ["Your Real Address"],
                    "city": "Your City",
                    "stateOrProvinceCode": "Your State",
                    "postalCode": "Your Postal",
                    "countryCode": "US"
                }
            },
            "recipient": {
                "contact": {
                    "personName": "Recipient Name",
                    "phoneNumber": "Recipient Phone"
                },
                "address": {
                    "streetLines": ["Recipient Address"],
                    "city": "Recipient City",
                    "stateOrProvinceCode": "Recipient State",
                    "postalCode": "Recipient Postal",
                    "countryCode": "US"
                }
            },
            "pickupType": shipment_type,
            "serviceType": service,
            "packagingType": "FEDEX_BOX",
            "paymentType": "SENDER",
            "shippingChargesPayment": {
                "paymentType": "SENDER",
                "payor": {
                    "responsibleParty": {
                        "accountNumber": {"value": settings.FEDEX_ACCOUNT_NUMBER},
                        "countryCode": "US"
                    }
                }
            },
            "labelSpecification": {
                "labelFormatType": "COMMON2D",
                "imageType": "PDF",
                "labelStockType": "PAPER_4X6"
            },
            "rateRequestType": ["ACCOUNT"],
            "totalWeight": {"units": "KG", "value": float(total_weight)},
            "shipTimestamp": pickup_time,
            "requestedPackageLineItems": [
                {
                    "weight": {"units": "KG", "value": float(total_weight)},
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
    return response.json() 