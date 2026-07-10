import re
import pandas as pd
from datetime import datetime

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)
VALIDATION_RULES = {
    "EORI Number": {
        "required": True,
        "regex": r"^[A-Z]{2}[A-Za-z0-9]{1,15}$",
        "message": "Invalid EORI format"
    },

    "Declarant Legal Name": {
        "required": True,
        "max_length": 255
    },

    "Declarant Address": {
        "required": True,
        "max_length": 500
    },

    "Contact Person": {
        "required": True,
        "type": "email"
    },

    "Competent Authority": {
        "required": True,
        "max_length": 100
    },

    "CBAM Account Number": {
        "required": True,
        "max_length": 100
    },

    "Data Owner": {
        "required": True,
        "type": "email"
    },

    "TARIC Code": {
        "required": False,
        "regex": r"^\d{10}$",
        "message": "Must contain exactly 10 digits"
    },

    "CN Code": {
        "required": True,
        "regex": r"^\d{8}$",
        "message": "Must contain exactly 8 digits"
    },

    "Goods Description": {
        "required": True,
        "max_length": 500
    },

    "Sector Category": {
        "required": True
    },

    "Product Type": {
        "required": True
    },

    "Import Volume": {
        "required": True,
        "type": "number",
        "min": 0
    },

    "Date of importation": {
        "required": True,
        "type": "date"
    },

    "Country of Origin": {
        "required": True
    },

    "Customs Declaration Ref": {
        "required": True
    },

    "Supplier Name": {
        "required": True
    },

    "Notes / Comments": {
        "required": False
    }

}

def clean_value(value):
    if pd.isna(value):
        return None
    return value

def validate_row(row, row_number):

    errors = []

    for column, rules in VALIDATION_RULES.items():

        value = row[column]

        # obligatorio

        if rules.get("required"):

            if pd.isna(value) or str(value).strip() == "":

                errors.append({
                    "row": row_number,
                    "field": column,
                    "value": clean_value(value),
                    "message": "Required field"
                })

                continue

        # si es opcional y viene vacío

        if pd.isna(value) or str(value).strip() == "":
            continue

        value = str(value).strip()

        # regex

        if "regex" in rules:

            if not re.match(rules["regex"], value):

                errors.append({
                    "row": row_number,
                    "field": column,
                    "value": clean_value(value),
                    "message": rules["message"]
                })

        # longitud máxima

        if "max_length" in rules:

            if len(value) > rules["max_length"]:

                errors.append({
                    "row": row_number,
                    "field": column,
                    "value": clean_value(value),
                    "message": f"Maximum length is {rules['max_length']}"
                })

        # número

        if rules.get("type") == "number":

            try:

                number = float(value)

                if number < rules.get("min", 0):

                    errors.append({
                        "row": row_number,
                        "field": column,
                        "value": clean_value(value),
                        "message": f"Must be greater than {rules['min']}"
                    })

            except:

                errors.append({
                    "row": row_number,
                    "field": column,
                    "value": clean_value(value),
                    "message": "Must be numeric"
                })

        # fecha

        if rules.get("type") == "date":

            try:

                pd.to_datetime(value)

            except:

                errors.append({
                    "row": row_number,
                    "field": column,
                    "value": clean_value(value),
                    "message": "Invalid date"
                })

        if rules.get("type") == "email":
            if not EMAIL_REGEX.match(value):
                errors.append({
                    "row": row_number,
                    "field": column,
                    "value": clean_value(value),
                    "message": "Debe ser un correo electrónico válido."
                })

    return errors