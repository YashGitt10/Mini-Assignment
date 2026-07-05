def generate_summary(customer, payment_plan, accepted):
    return {
        "customer_name": customer["name"],
        "date_of_birth": customer["dob"].strftime("%d/%m/%Y"),
        "due_amount": customer["due_amount"],
        "payment_plan_accepted": accepted,
        "payment_details": payment_plan
    }