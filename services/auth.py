from datetime import datetime
from services.llm import get_llm_response
from utils.prompts import SYSTEM_PROMPT

def verify_name(user_name, actual_name):
    return user_name.strip().lower() == actual_name.strip().lower()


def verify_dob(user_dob, actual_dob):
    try:
        entered_dob = datetime.strptime(user_dob, "%d/%m/%Y").date()
        return entered_dob == actual_dob
    except ValueError:
        return False


def authenticate(step, user_input, customer):
    if step == "ASK_NAME":
        if verify_name(user_input, customer["name"]):
            response = get_llm_response(
                SYSTEM_PROMPT,
                (
                    "The customer's name has been verified. "
                    "Thank them politely and ask for their date of birth "
                    "in DD/MM/YYYY format."
                )
            )
            return ("ASK_DOB", response)
        response = get_llm_response(
            SYSTEM_PROMPT,
            (
                "The customer's name did not match the records. "
                "Politely ask them to re-enter their full name."
            )
        )
        return ("ASK_NAME",response)
    
    elif step == "ASK_DOB":
        if verify_dob(user_input, customer["dob"]):
            response = get_llm_response(
                SYSTEM_PROMPT,
                (
                    f"The customer has been authenticated successfully.\n"
                    f"Outstanding balance is ${customer['due_amount']:.2f}.\n"
                    "Politely inform the customer and ask how much they can pay today."
                )
            )
            return ("ASK_PAYMENT", response)
        response = get_llm_response(
            SYSTEM_PROMPT,
            (
                "The customer's dob did not match the records. "
                "Politely ask them to re-enter again (DD/MM/YYYY)."
            )
        )
        return ("ASK_DOB", response)

    return step, ""