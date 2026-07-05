# Healthcare Collections Chatbot

A Streamlit-based chatbot that simulates a healthcare debt collection conversation. The chatbot authenticates the customer, discusses the outstanding balance, offers payment plans based on predefined business rules, and generates a structured summary at the end of the conversation.

---

## Features

- Customer authentication using **Name** and **Date of Birth**
- Configurable customer details from the Streamlit sidebar
- Displays outstanding healthcare balance
- Offers payment plans based on business rules
- Uses Groq LLM to generate natural and professional responses
- Displays a structured JSON summary after the conversation
- Reset chat option for starting a new session

---

## Healthcare Journey

1. Customer enters their **Name**
2. Customer enters their **Date of Birth**
3. Chatbot authenticates the customer
4. Outstanding balance is displayed
5. Customer enters the payment amount
6. Chatbot offers an appropriate payment plan
7. Customer accepts or rejects the plan
8. A structured conversation summary is displayed

---

## Payment Rules

| Payment Today | Result |
|---------------|--------|
| Full Amount | Balance cleared immediately |
| Less than $50 | Payment rejected |
| $50 - $99.99 | Remaining balance split into **12 monthly installments** |
| $100 or more | Remaining balance split into **9 monthly installments** |

---

## Project Structure

```
healthcare-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── services/
│   ├── auth.py
│   ├── payment.py
│   └── llm.py
│
└── utils/
    ├── prompts.py
    └── summary.py
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd healthcare-chatbot
```

### 2. Create a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Groq API Key Setup

1. Create a free account at https://console.groq.com/

2. Generate an API Key.

3. Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_api_key_here
```

---

## Run the Application

```bash
streamlit run app.py
```

---

## Sample Conversation

**Assistant**

```
Hello! Welcome to the Healthcare Collections Assistant.

Let's begin by verifying your identity.

What is your full name?
```

**User**

```
Yash Gupta
```

**Assistant**

```
Please enter your Date of Birth.
```

**User**

```
15/12/2004
```

**Assistant**

```
Authentication successful.

Outstanding Balance: $450

How much can you pay today?
```

**User**

```
100
```

**Assistant**

```
You can pay $100 today.

The remaining balance will be divided into 9 monthly installments.

Do you accept this payment plan?
```

**User**

```
Yes
```

**Assistant**

```
Thank you! Your payment plan has been confirmed.
```

---

## Technologies Used

- Python
- Streamlit
- Groq API
- Llama 3.3 70B Versatile
- python-dotenv

---

## Notes

- Authentication is simulated using configurable customer details from the Streamlit sidebar.
- Business rules for payment calculations are implemented in Python.
- The LLM is used only for generating conversational responses, while business logic remains deterministic.
