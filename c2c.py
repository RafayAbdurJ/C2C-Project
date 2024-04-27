import unittest
import mysql.connector
import random
import unittest
from unittest.mock import patch


def bank():
    # this is connecting my database 
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "MySQL*1234",
    database = "Bank"
    )

    mycursor = mydb.cursor()

    

    balance = 0
    accN = random.randint(100000,999999)
    while True:
        # this gives user the menu options
        print('Hello User welcome to Bank XYZ')
        print('Choose from this menu')
        options = ['1. Create new Bank account', '2. Check Balance', '3. Transfer money', '4. Deposit money',
                   '5. Modify account details', '6. Delete account', '7. Exit']
        for option in options:
            print(option)
        # if user chooses 1 all of this happens
        choice = input("Enter your choice: ")
        if choice == "1":
            print('Creating a new Bank account')
            name = input('Enter Your full legal Name: ')
            age = input('Enter Your Age: ')
            idNum = input('Enter Your DL NUM: ')
            ssn = input('Enter Your SSN num: ')
            nationality = input('Enter Your Nationality: ')
            balance = input('Your Starting balance: ')
            # this is adding data to db 
            sql = "INSERT INTO onlineBank(accNum, name, age, SSN, nationality, balance) VALUES (%s,%s, %s, %s, %s,%s)"
            values = (accN, name, age, ssn, nationality, balance)
            mycursor.execute(sql, values)
            mydb.commit()
            
            print("Bank account successfully created!")
        # if user chooses 2 all of this happens
        elif choice == "2":
            print("Checking balance...")
            print("Enter account details to check balance:")
            name = input('Enter Your full legal Name: ')
            # this is pulling out data from db
            sql = "SELECT balance FROM onlineBank WHERE name = %s"
            mycursor.execute(sql, (name,))
            result = mycursor.fetchone()
            if result:
                print(f"Your current balance is: ${result[0]}")
            else:
                print("Account not found.")
        # if user chooses 3 all of this happens
        elif choice == "3":
            print("Transfer Money")
            name = input('Enter Your full legal Name: ')
            sql = "SELECT balance FROM onlineBank WHERE name = %s"
            mycursor.execute(sql, (name,))
            result = mycursor.fetchone()
            if result:
                current_balance = float(result[0])
                money = float(input('Enter the amount you want to transfer: $'))
                if money <= current_balance:
                    print(f"Transferring ${money}...")
                    # this is updating data 
                    new_balance = current_balance - money
                    sql_update = "UPDATE onlineBank SET balance = %s WHERE name = %s"
                    mycursor.execute(sql_update, (new_balance, name))
                    mydb.commit()
                    print("Transfer successful!")
                else:
                    print("Insufficient funds!")
            else:
                print("Account not found.")

        # if user chooses 4 all of this happens
        elif choice == "4":
            print("Deposit Money")
            ssn = input('Enter Your last digits of SSN ')
            sql = "SELECT balance FROM onlineBank WHERE SSN = %s"
            mycursor.execute(sql, (ssn,))
            result = mycursor.fetchone()
            if result:
                current_balance = float(result[0])
                deposit_amount = float(input("Enter the amount you want to deposit: $"))
                new_balance = current_balance + deposit_amount
                # this is updating data
                sql_update = "UPDATE onlineBank SET balance = %s WHERE SSN = %s"
                mycursor.execute(sql_update, (new_balance, ssn))
                mydb.commit()
                print("Deposit successful! New balance:", new_balance)
            else:
                print("Account not found.")
            
                
        # if user chooses 5 all of this happens
        elif choice == "5":
            print("Modify account details")
            print("Enter account details to modify:")
            name = input('Enter Your full legal Name: ')
            ssn = input ('Enter Last 4 digits of your SSN: ')
            
            sql = "SELECT name FROM onlineBank WHERE SSN = %s"
            mycursor.execute(sql, (ssn,))
            result = mycursor.fetchone()

            if result:
                newName = input('Enter your new username: ')
                sql_update = "UPDATE onlineBank SET name = %s WHERE SSN = %s"
                # this is updating data 
                mycursor.execute(sql_update, (newName, ssn))
                mydb.commit()
                print("Username updated successfully!")
            else:
                print("Account not found.")
        # if user chooses 6 all of this happens
        elif choice == "6":
            print("Delete account")
            print("Enter account details to delete:")
            name = input('Enter Your full legal Name: ')
            ssn = input('Enter last 4 Digits of your SSN: ')
            # this is deleting data
            sql = 'DELETE FROM onlineBank WHERE SSN = %s;'
    
            mycursor.execute(sql, (ssn,))
            
            
            if mycursor.rowcount > 0:
                print("Account successfully deleted!")
            else:
                print("Account not found.")
        # if user chooses 7 all of this happens
        # this stops the program
        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

        yn = input("Do you want to perform another action? (yes/no): ")
        if yn.lower() != "yes":
            print("Exiting...")
            break

    mydb.close()
bank()
# unittests
class TestBankFunctions(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', 'John Doe', '25', '1234', '123-45-6789', 'USA', '1000', 'no'])
    def test_create_account(self, mock_input):
        
        bank()  
        

    @patch('builtins.input', side_effect=['2', 'John Doe', 'no'])
    def test_check_balance(self, mock_input):
        
        bank()
if __name__ == '__main__':
    unittest.main()
