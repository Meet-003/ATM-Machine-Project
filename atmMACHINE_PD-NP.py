#================== ATM machine using Pandas and Numpy ================================
import numpy as np
import pandas as pd
from datetime import datetime

accounts = pd.DataFrame({
    'Account Number' : [101,102,103],
    'Name' : ['Meet', 'Ankur', 'Sanjiv'],
    'PIN' : ['1234', '5678', '4321'],
    'Balance' : [50000, 70000, 100000],
    'Account Type' : ['Savings', 'Savings', 'Savings']
})

# Define transactions with explicit data types to avoid the FutureWarning
transactions = pd.DataFrame({
    'Account Number': pd.Series(dtype='int'),
    'Type': pd.Series(dtype='str'),
    'Amount': pd.Series(dtype='float'),
    'Date': pd.Series(dtype='str')
})

transactions = pd.DataFrame(columns=['Account Number', 'Type', 'Amount', 'Date'])

def log_transaction(account_num, txn_type, amount):
    global transactions
    new_txn = pd.DataFrame({
        'Account Number' : [account_num],
        'Type' : [txn_type],
        'Amount' : [amount],
        'Date' : [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    })
    transactions = pd.concat([transactions, new_txn], ignore_index=True)

def verify_pin(account_num, pin):
    user = accounts[accounts['Account Number'] == account_num]
    if not user.empty and user.iloc[0]['PIN'] == pin:
        return True
    return False

def check_balance(account_num):
    return accounts.loc[accounts['Account Number'] == account_num, 'Balance'].values[0]

def withdraw_cash(account_num, amount):
    idx = accounts.index[accounts['Account Number'] == account_num][0]
    if accounts.at[idx, 'Balance'] >= amount:
        accounts.at[idx, 'Balance'] -= amount
        log_transaction(account_num, 'Withdraw', amount)
        print(f"Withdrawl Successfull. New Balance: {accounts.at[idx, 'Balance']}")
    else:
        print("Insufficient Balance!!!")

def deposit_cash(account_num, amount):
    idx = accounts.index[accounts['Account Number'] == account_num][0]
    accounts.at[idx, 'Balance'] += amount
    log_transaction(account_num, 'Deposit', amount)
    print(f"Deposit successful. New Balance: {accounts.at[idx, 'Balance']}")

def print_mini_statement(account_num):
    user_txns = transactions[transactions['Account Number'] == account_num].tail(5)
    if user_txns.empty:
        print("No transactions found.")
    else:
        print("\n--- Mini Statement (Last 5 transaction) ---")
        print(user_txns.to_string(index=False))

def change_pin(account_num):
    idx = accounts.index[accounts['Account Number'] == account_num][0]
    new_pin = input("Enter new 4-digit PIN: ")

    if len(new_pin) == 4 and new_pin.isdigit():
        accounts.at[idx, 'PIN'] == new_pin
        print("PIN Updated successfully.")
    else:
        print("Invalid PIN format. Try Again.")

def atm_menu(account_num):
    while True:
        print("\n--- ATM main Menu ---")
        print("1. Check Balance")
        print("2. Withdraw Cash")
        print("3. Deposit Cash")
        print("4. Mini Statement")
        print("5. Change PIN")
        print("6. Exit")

        choice = int(input("Enter your Choice (1-6): "))

        if choice == 1:
            balance = check_balance(account_num)
            print(f"Your Current balance is: ₹{balance}")

        elif choice == 2:
            amount = float(input("Enter amount to Withdraw: ₹"))
            withdraw_cash(account_num, amount)

        elif choice == 3:
            amount = float(input("Enter amount to Deposit: ₹"))
            deposit_cash(account_num, amount)
        
        elif choice == 4:
            print_mini_statement(account_num)

        elif choice == 5:
            change_pin(account_num)

        elif choice == 6:
            print("Thank you for using the ATM. Goodbye!")
            break

        else:
            print("Invalid Choice. Please try again.")

def main():
    print("Welcome to the ATM Machine")

    try:
        account_num = int(input("Enter your Account Number: "))
    except ValueError:
        print('Invalide account number format.')
        return
    
    pin = input("Enter your PIN: ")

    if verify_pin(account_num, pin):
        print(f"Welcome {accounts.loc[accounts['Account Number'] == account_num, 'Name'].values[0]}!")
        atm_menu(account_num)
    else:
        print("Incorrect PIN. Access Denied.")

if __name__ == "__main__":
    main()