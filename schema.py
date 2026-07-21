from pydantic import BaseModel, Field
from typing import Optional


class RateConfirmation(BaseModel):
    """Data model representing extracted Rate Confirmation details."""

    # Broker & Reference Info
    broker_name: Optional[str] = Field(
        default=None, description="Name of the freight broker or logistics company"
    )
    load_number: Optional[str] = Field(
        default=None, description="Load, Order, or Reference Number"
    )

    # Financials
    line_haul_rate: float = Field(
        default=0.0, description="Base line-haul rate in USD"
    )
    fuel_surcharge: float = Field(
        default=0.0, description="Fuel surcharge amount in USD"
    )
    total_pay: float = Field(
        default=0.0, description="Total gross pay amount in USD"
    )

    # Route & Load Specifications
    origin: Optional[str] = Field(
        default=None, description="Pickup location (City, State / Zip)"
    )
    destination: Optional[str] = Field(
        default=None, description="Delivery location (City, State / Zip)"
    )
    total_miles: Optional[int] = Field(
        default=None, description="Total trip mileage"
    )
    commodity: Optional[str] = Field(
        default=None, description="Type of freight/goods being transported"
    )
    equipment_type: Optional[str] = Field(
        default=None, description="Required equipment (e.g., Dry Van, Reefer, Flatbed)"
    )