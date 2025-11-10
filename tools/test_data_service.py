"""Test Data Service (TDS) client for managing test data."""

import requests
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

from configs import get_settings


class TestDataServiceClient:
    """Client for Test Data Service API."""

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize TDS client."""
        settings = get_settings()
        self.base_url = base_url or settings.tds_base_url
        self.api_key = api_key or settings.tds_api_key
        self.timeout = settings.tds_timeout
        
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"X-API-Key": self.api_key})

    def _request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to TDS API."""
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"TDS request failed: {e}")
            raise

    def generate_user(self, profile: str = "default") -> Dict[str, Any]:
        """Generate synthetic user data."""
        return self._request("POST", "/data/user", data={"profile": profile})

    def generate_address(self, country: str = "US") -> Dict[str, Any]:
        """Generate synthetic address data."""
        return self._request("POST", "/data/address", data={"country": country})

    def generate_payment(self, card_type: str = "visa") -> Dict[str, Any]:
        """Generate synthetic payment data."""
        return self._request("POST", "/data/payment", data={"card_type": card_type})

    def lock_data(self, data_type: str, data_id: str, lock_id: str) -> Dict[str, Any]:
        """Lock a data record for exclusive use."""
        return self._request(
            "POST",
            f"/data/{data_type}/{data_id}/lock",
            data={"lock_id": lock_id}
        )

    def release_data(self, data_type: str, data_id: str, lock_id: str) -> Dict[str, Any]:
        """Release a locked data record."""
        return self._request(
            "POST",
            f"/data/{data_type}/{data_id}/release",
            data={"lock_id": lock_id}
        )

    def get_data(self, data_type: str, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Get data records with optional filters."""
        return self._request("GET", f"/data/{data_type}", params=filters)

    def create_data(self, data_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new data record."""
        return self._request("POST", f"/data/{data_type}", data=data)

    def update_data(self, data_type: str, data_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing data record."""
        return self._request("PUT", f"/data/{data_type}/{data_id}", data=data)

    def delete_data(self, data_type: str, data_id: str) -> Dict[str, Any]:
        """Delete data record."""
        return self._request("DELETE", f"/data/{data_type}/{data_id}")


class DataGenerator:
    """Helper class for generating synthetic test data using Faker."""

    def __init__(self):
        """Initialize data generator."""
        from faker import Faker
        self.fake = Faker()

    def generate_user(self) -> Dict[str, Any]:
        """Generate user data."""
        return {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.fake.email(),
            "phone": self.fake.phone_number(),
            "username": self.fake.user_name(),
            "password": self.fake.password(length=12),
        }

    def generate_address(self) -> Dict[str, Any]:
        """Generate address data."""
        return {
            "street": self.fake.street_address(),
            "city": self.fake.city(),
            "state": self.fake.state(),
            "postal_code": self.fake.postcode(),
            "country": self.fake.country_code(),
        }

    def generate_company(self) -> Dict[str, Any]:
        """Generate company data."""
        return {
            "name": self.fake.company(),
            "email": self.fake.company_email(),
            "phone": self.fake.phone_number(),
            "website": self.fake.url(),
        }

    def generate_credit_card(self) -> Dict[str, Any]:
        """Generate credit card data."""
        return {
            "number": self.fake.credit_card_number(),
            "provider": self.fake.credit_card_provider(),
            "expire": self.fake.credit_card_expire(),
            "cvv": self.fake.credit_card_security_code(),
        }
