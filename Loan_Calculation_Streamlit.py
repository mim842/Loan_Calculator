import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def generate_amortization_schedule(principal, annual_interest_rate, monthly_payment, additional_payment=0.0):
    monthly_interest_rate = annual_interest_rate / 12
    total_interest_paid = 0.0
    payment_number = 0

    df = pd.DataFrame(columns=["Principal ($)", "Interest ($)", "Accrued Interest ($)", "Remaining Balance ($)"])

    while principal > 0:
        payment_number += 1
        interest_payment = principal * monthly_interest_rate
        principal_payment = monthly_payment + additional_payment - interest_payment
        principal_payment = min(principal_payment, principal)
        principal -= principal_payment
        total_interest_paid += interest_payment

        df.loc[payment_number] = [
            round(principal_payment, 2),
            round(interest_payment, 2),
            round(total_interest_paid, 2),
            round(principal, 2)
        ]

        if principal <= 0:
            break

    df.index.name = "Payment Number"
    return df

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

def plot_payment_impact(principal, interest_rate, base_monthly_payment, additional_payment):
    additional_payments = [0, additional_payment]
    colors = ['blue', 'green']
    labels = ['Standard Payment', f'Additional +${additional_payment}']

    total_amounts = []
    payment_counts = []

    plt.figure(figsize=(6, 4))
    bars = []
    for i, add_pay in enumerate(additional_payments):
        modified_monthly_payment = base_monthly_payment + add_pay
        n_payments, total_interest_paid = calculate_remaining_payments(principal, interest_rate / 12, modified_monthly_payment)
        total_paid = n_payments * modified_monthly_payment + total_interest_paid
        total_amounts.append(total_paid)
        payment_counts.append(n_payments)
        bar = plt.bar(i, n_payments, color=colors[i], width=0.4)
        bars.append(bar)

    for i in range(len(total_amounts)):
        plt.text(i, payment_counts[i], f'Total: ${total_amounts[i]:,.0f}', ha='center', va='bottom')
        # Position month text in the center of the bar
        plt.text(i, payment_counts[i]/2, f'{payment_counts[i]} months', ha='center', va='center', color='white', fontweight='bold')

    plt.ylabel('Number of Payments')
    plt.title('Impact of Additional Payments Payments on Loan Term')
    plt.xticks(range(len(additional_payments)), labels)

    plt.legend([bars[0][0], bars[1][0]], [labels[0], labels[1]], loc='center')

    plt.tight_layout()
    st.pyplot(plt)


st.title("Loan Calculator Dashboard")

new_loan = st.radio("Do you want to calculate for a new loan?", ('Yes', 'No'))

if new_loan == 'No':
    principal = st.number_input("Enter your current principal remaining:", min_value=0.01)
    interest_rate = st.number_input("Enter your current interest rate (as a decimal):", min_value=0.0, max_value=1.0, value=0.05, step=0.001, format="%.4f")
    monthly_payment = st.number_input("Enter your current monthly loan payment:", min_value=0.01)
    additional_payment = st.number_input("Enter the additional monthly principal payment:", min_value=0.0)

    if st.button("Calculate Loan Details"):
        modified_monthly_payment = monthly_payment + additional_payment
        new_number_of_payments, new_total_interest_paid = calculate_remaining_payments(principal, interest_rate / 12, modified_monthly_payment)
        
        st.write(f"Time remaining on your loan with additional payment: {new_number_of_payments//12} years and {new_number_of_payments%12} months")
        st.write(f"New total interest paid with additional payment: ${new_total_interest_paid:,.2f}")
        modified_total_cost = modified_monthly_payment * new_number_of_payments
        st.write(f"Total cost with additional \${additional_payment:,.2f} monthly payment: ${modified_total_cost:,.2f}")       
        detailed_schedule = generate_amortization_schedule(principal, interest_rate, monthly_payment, additional_payment)
        st.write("Monthly Amortization Schedule:")
        st.dataframe(detailed_schedule)
        plot_payment_impact(principal, interest_rate, monthly_payment, additional_payment)

else:
    purchase_price = st.number_input("Enter the total purchase price:", min_value=0.01)
    down_payment = st.number_input("Enter the down payment:", min_value=0.0)
    interest = st.number_input("Enter the annual interest rate (as a decimal, e.g., 0.05 for 5%):", min_value=0.0, max_value=1.0, value=0.05, step=0.001, format="%.4f")
    term_years = st.number_input("Enter the term of the loan in years:", min_value=1.0, format="%.4f")
    additional_payment = st.number_input("Enter the additional monthly principal payment:", min_value=0.0)
    
    if st.button("Calculate New Purchase Loan Details"):
        principal = purchase_price - down_payment
        term_months = term_years * 12
        monthly_interest_rate = interest / 12
        monthly_payment = principal * monthly_interest_rate / (1 - (1 / ((1 + monthly_interest_rate) ** term_months)))
        final_total_cost = down_payment + monthly_payment * term_months
        
        detailed_schedule = generate_amortization_schedule(principal, interest, monthly_payment, additional_payment)
        st.write(f"Your monthly payment (Interest + Principal) is: ${monthly_payment:,.2f}")
        st.write(f"Total cost based on a {term_years}-Year Loan: ${final_total_cost:,.2f}")

        modified_monthly_payment = monthly_payment + additional_payment
        new_number_of_payments, new_total_interest_paid = calculate_remaining_payments(principal, monthly_interest_rate, modified_monthly_payment)
        modified_total_cost = (modified_monthly_payment * new_number_of_payments) + down_payment 

        st.write(f"Total cost with additional \${additional_payment} monthly payment: ${modified_total_cost:,.2f}")
        st.write(f"Total interest paid over the new loan period with additional payment: ${new_total_interest_paid:,.2f}")
        st.write(f"Time required to pay off the loan with additional principal payments: {int(new_number_of_payments / 12)} years or {new_number_of_payments} months")
        st.write("Monthly Amortization Schedule:")
        st.dataframe(detailed_schedule)
        plot_payment_impact(principal, interest, monthly_payment, additional_payment)
#streamlit run "c:\Users\musta\Downloads\Loan_Calculation_Streamlit.py"
