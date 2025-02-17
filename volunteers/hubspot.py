import requests
import os

# ✅ Securely get HubSpot API Key from environment variable
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY", "pat-na1-5fd03b95-117a-4553-8404-c58c17151388")

def create_hubspot_contact(volunteer):
    url = f"https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "properties": {
            "email": volunteer.email,
            "firstname": volunteer.first_name,
            "lastname": volunteer.last_name,
            "phone": volunteer.phone,
            "role": volunteer.role,
            "availability": volunteer.availability
        }
    }

    print("Sending data to HubSpot:", data)  # ✅ Debugging

    response = requests.post(url, json=data, headers=headers)

    print("HubSpot Response:", response.status_code, response.text)  #  Debugging

    if response.status_code == 201:
        return response.json()  # ✅ Return the created contact info
    else:
        return {"error": response.status_code, "details": response.text}
