from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, EmailStr, field_validator


class CbamImportCreate(BaseModel):
    eori_number: str = Field(
        ...,
        min_length=4,
        max_length=17,
        description="Código EORI"
    )

    declarant_legal_name: str = Field(..., min_length=1)

    declarant_address: str = Field(..., min_length=1)

    contact_person: EmailStr

    competent_authority: str = Field(..., min_length=1)

    cbam_account_number: str = Field(...)

    data_owner: EmailStr

    taric_code: str | None = Field(
        default=None,
        pattern=r"^\d{10}$"
    )

    cn_code: str = Field(
        ...,
        pattern=r"^\d{8}$"
    )

    goods_description: str

    sector_category: str

    product_type: Literal["Simple", "Complex"]

    import_volume: Decimal = Field(..., gt=0)

    date_of_importation: date

    country_of_origin: str

    customs_declaration_ref: str

    supplier_name: str

    notes_comments: str | None = None

    @field_validator("eori_number")
    @classmethod
    def validate_eori(cls, value: str):
        import re

        pattern = r"^[A-Z]{2}[A-Za-z0-9]{1,15}$"

        if not re.match(pattern, value):
            raise ValueError(
                "El EORI debe comenzar con 2 letras y continuar con caracteres alfanuméricos."
            )

        return value
