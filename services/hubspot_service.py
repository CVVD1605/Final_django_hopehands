import os
import logging
from typing import Dict, Any
import requests
from django.conf import settings
from hubspot import HubSpot

logger = logging.getLogger(__name__)


class HubSpotService:
    def __init__(self):
        self.api_key = settings.HUBSPOT_API_KEY
        self.base_url = "https://api.hubapi.com"

    def get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
        }

    def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new contact in HubSpot with proper property mapping.
        """
        url = f"{self.base_url}/crm/v3/objects/contacts"

        # Map the properties according to HubSpot's expected format
        properties = {
            "email": contact_data.get("email"),
            "firstname": contact_data.get("first_name"),
            "lastname": contact_data.get("last_name"),
            "phone": contact_data.get("phone"),
            "role": contact_data.get("role"),
            "availability": contact_data.get("availability")
        }
        payload = {"properties": properties}
        try:
            response = requests.post(
                url,
                json=payload,
                params={"hapikey": self.api_key},
                headers=self.get_headers()
            )
            response.raise_for_status()
            logger.info(
                "Successfully created contact in HubSpot: %s", response.json())

            return response.json()

        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error occurred: %s", str(e))
            error_detail = e.response.json() if e.response else {
                "message": str(e)}
            raise ValueError(
                f"HubSpot API error: {error_detail.get('message', str(e))}"
            ) from e

        except Exception as e:
            logger.error("Error creating contact in HubSpot: %s", str(e))
            print(f"HUBSPOT_API_KEY: {settings.HUBSPOT_API_KEY}")
            raise ValueError(f"Failed to create contact: {str(e)}") from e
