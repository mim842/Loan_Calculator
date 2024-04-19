import streamlit as st

def calculate_remaining_loan_time(interest_rate, principal, monthly_payment):
    monthly_interest_rate = interest_rate / 12
    months_remaining = 0
    total_interest_paid = 0

    while principal > 0:
        interest_for_this_month = principal * monthly_interest_rate
        principal_payment = monthly_payment - interest_for_this_month

        if principal_payment <= 0:
            raise ValueError("Monthly payment is too low to cover the interest. Please check your inputs.")
        
        principal -= principal_payment
        months_remaining += 1
        total_interest_paid += interest_for_this_month

        if principal < monthly_payment:
            break
        
    return months_remaining, total_interest_paid

def calculate_remaining_payments(principal, monthly_interest_rate, modified_monthly_payment):
    remaining_payments = 0
    current_balance = principal
    total_interest_paid = 0

    while current_balance > 0:
        interest_for_the_month = current_balance * monthly_interest_rate
        principal_payment = modified_monthly_payment - interest_for_the_month
        current_balance -= principal_payment
        remaining_payments += 1
        total_interest_paid += interest_for_the_month

        if current_balance < 0:
            current_balance = 0

    return remaining_payments, total_interest_paid

st.title("Loan Calculator Dashboard")

existing_loan = st.radio("Do you want to calculate for an existing loan?", ('Yes', 'No'))

if existing_loan == 'Yes':
    principal = st.number_input("Enter your current principal remaining:", min_value=0.01)
    interest_rate = st.number_input("Enter your current interest rate (as a decimal):", min_value=0.0, max_value=1.0, value=0.05, step=0.001, format="%.4f")
    monthly_payment = st.number_input("Enter your current monthly loan payment:", min_value=0.01)
    additional_payment = st.number_input("Enter the additional monthly principal payment:", min_value=0.0)

    if st.button("Calculate Loan Details"):
        months_remaining, total_interest_paid = calculate_remaining_loan_time(interest_rate, principal, monthly_payment)
        st.write(f"Time remaining on your loan: {months_remaining//12} years and {months_remaining%12} months")
        st.write(f"Total interest paid: ${total_interest_paid:,.2f}")

        modified_monthly_payment = monthly_payment + additional_payment
        new_number_of_payments, new_total_interest_paid = calculate_remaining_payments(principal, interest_rate / 12, modified_monthly_payment)
        modified_total_cost = modified_monthly_payment * new_number_of_payments
        st.write(f"Total cost with additional \${additional_payment} monthly payment: ${modified_total_cost:,.2f}")
        st.write(f"Time required to pay off the loan with additional principal payments: {int(new_number_of_payments / 12)} years or {new_number_of_payments} months")
        st.write(f"New total interest paid with additional payment: ${new_total_interest_paid:,.2f}")

else:
    purchase_price = st.number_input("Enter the total purchase price:", min_value=0.01)
    down_payment = st.number_input("Enter the down payment:", min_value=0.0)
    interest = st.number_input("Enter the annual interest rate (as a decimal, e.g., 0.05 for 5%):", min_value=0.01)
    term_years = st.number_input("Enter the term of the loan in years:", min_value=1, format='%d')
    additional_payment = st.number_input("Enter the additional monthly principal payment:", min_value=0.0)

    if st.button("Calculate New Purchase Loan Details"):
        principal = purchase_price - down_payment
        term_months = term_years * 12
        monthly_interest_rate = interest / 12
        monthly_payment = principal * monthly_interest_rate / (1 - (1 / ((1 + monthly_interest_rate) ** term_months)))
        final_total_cost = down_payment + monthly_payment * term_months

        st.write(f"Your monthly payment (Interest + Principal) is: ${monthly_payment:,.2f}")
        st.write(f"Total cost based on a {term_years}-Year Loan: ${final_total_cost:,.2f}")

        modified_monthly_payment = monthly_payment + additional_payment
        new_number_of_payments, new_total_interest_paid = calculate_remaining_payments(principal, monthly_interest_rate, modified_monthly_payment)
        modified_total_cost = (modified_monthly_payment * new_number_of_payments) + down_payment 

        st.write(f"Total cost with additional \${additional_payment} monthly payment: ${modified_total_cost:,.2f}")
        st.write(f"Total interest paid over the new loan period with additional payment: ${new_total_interest_paid:,.2f}")
        st.write(f"Time required to pay off the loan with additional principal payments: {int(new_number_of_payments / 12)} years or {new_number_of_payments} months")

#run: streamlit run "c:\Users\musta\Downloads\Loan_Calculation_Streamlit.py"