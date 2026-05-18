from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    product_ids: list[str] = Field(..., description="List of product IDs included in the order.")

class PaymentRequest(BaseModel):
    order_id: str = Field(..., description="The ID of the order to be paid.")
    payment_method: str = Field(..., description="The method of payment (e.g., 'credit_card', 'paypal').")