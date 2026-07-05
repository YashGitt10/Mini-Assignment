import streamlit as st
from datetime import date
from services.auth import authenticate
from services.payment import calculate_payment_plan
from services.llm import get_llm_response
from utils.prompts import SYSTEM_PROMPT
from utils.summary import generate_summary

# Page Config
st.set_page_config(page_title="Healthcare Collections Chatbot")
st.title("Healthcare Collections Chatbot")
st.caption("Authenticate the customer and discuss the outstanding healthcare balance.")

# sidebar
st.sidebar.header("Session Configuration")

customer_name = st.sidebar.text_input("Customer Name", value="Yash Gupta")
customer_dob = st.sidebar.date_input("Date of Birth", value=date(2004, 12, 15), format="DD/MM/YYYY")
due_amount = st.sidebar.number_input("Outstanding Balance ($)", min_value=50.0, value=450.0, step=10.0)

customer = {
    "name": customer_name,
    "dob": customer_dob,
    "due_amount": due_amount
}

if st.sidebar.button("Reset Chat"):
    st.session_state.clear()
    st.rerun()

# session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! Welcome to the Healthcare Collections Assistant.\n\n"
                "Let's begin by verifying your identity.\n\n"
                "What is your full name?"
            )
        }
    ]

if "step" not in st.session_state:
    st.session_state.step = "ASK_NAME"

if "payment_plan" not in st.session_state:
    st.session_state.payment_plan = None

if "summary" not in st.session_state:
    st.session_state.summary = None

# chat 
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Enter your response...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = ""

    # authentication steps
    if st.session_state.step in ["ASK_NAME", "ASK_DOB"]:
        next_step, response = authenticate(
            st.session_state.step,
            user_input,
            customer
        )
        st.session_state.step = next_step

    # payment plan steps
    elif st.session_state.step == "ASK_PAYMENT":
        try:
            payment_today = float(user_input)
            payment_plan = calculate_payment_plan(
                customer["due_amount"],
                payment_today
            )
            st.session_state.payment_plan = payment_plan

            if payment_plan["status"] == "invalid":
                st.session_state.summary = generate_summary(
                    customer,
                    payment_plan,
                    False
                )
                response = get_llm_response(
                    SYSTEM_PROMPT,
                    "The customer proposed a invalid amount. Politely explain that the plan cannot be accepted and close the conversation."
                )
                st.session_state.step = "END"

            elif payment_plan["status"] == "full":
                response = (payment_plan["message"] + 
                            "\n\nDo you accept this payment plan? (Yes/No)")

            elif payment_plan["status"] == "rejected":
                st.session_state.summary = generate_summary(
                    customer,
                    payment_plan,
                    False
                )
                response = get_llm_response(
                    SYSTEM_PROMPT,
                    "The customer proposed a payment below the minimum allowed amount. Politely explain that the plan cannot be accepted and close the conversation."
                )
                st.session_state.step = "END"

            elif payment_plan["status"] == "plan12":
                response = (payment_plan["message"] + 
                            "\n\nDo you accept this payment plan? (Yes/No)")

            else:
                response = (payment_plan["message"] + 
                            "\n\nDo you accept this payment plan? (Yes/No)")
                
            if payment_plan["status"] in ["full", "plan12", "plan9"]:
                st.session_state.step = "CONFIRM"
            else:
                st.session_state.step = "END"
        except ValueError:
            response = "Please enter a valid payment amount."

    # confirmation step
    elif st.session_state.step == "CONFIRM":
        answer = user_input.strip().lower()
        if (answer in ["yes", "y"]):
            st.session_state.summary = generate_summary(
                customer,
                st.session_state.payment_plan,
                True
            )
            response = get_llm_response(
                SYSTEM_PROMPT,
                (
                    "The customer accepted the payment plan. "
                    "Thank them politely and professionally."
                )
            )
            st.session_state.step = "END"
        elif (answer in ["no", "n"]):
            rejected_plan = {
                "status": "rejected_by_customer",
                "payment_today": 0,
                "remaining_balance": customer["due_amount"],
                "installments": 0,
                "monthly_installment": 0,
                "message": "Customer declined the proposed payment plan."
            }
            st.session_state.summary = generate_summary(
                customer,
                rejected_plan,
                False
            )
            response = get_llm_response(
            SYSTEM_PROMPT,
                (
                    "The customer rejected the payment plan. "
                    "Politely close the conversation."
                )
            )
            st.session_state.step = "END"
        else:
            response = "Please reply with Yes or No."

    # End of conversation
    elif st.session_state.step == "END":
        response = (
            "This chat has already ended.\n\n"
            "Click **Reset Chat** to start a new session."
        )

    # add assistant message to the chat history and display it
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# summary display
if st.session_state.summary:
    st.divider()
    st.subheader("Conversation Summary")
    st.json(st.session_state.summary)