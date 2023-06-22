import maskpass
import json
import re


class Banking:
    __last_account_no = '10000'
    __users_data = {}
    bank_name = ''
    logged_in = False

    def __init__(self, bank_name='XYZ'):
        Banking.bank_name = bank_name
        self.loading_user_data()

        # updating last account numbers to __last_account_no attribute
        try:
            last_user_name = list(Banking.__users_data.keys())[-1]
            Banking.__last_account_no = Banking.__users_data[last_user_name]['account_no']
        except IndexError:
            pass

        Banking.home_screen(self)

    def loading_user_data(self):
        # loading all users' data from text file
        try:
            with open(f"{Banking.bank_name}.txt", "r") as file1:
                Banking.__users_data = json.load(file1)

        except json.JSONDecodeError:
            pass

        except FileNotFoundError:
            with open(f"{Banking.bank_name}.txt", "w") as file1:
                pass

    def updating_user_data(self):
        # overwriting all updated data
        with open(f"{Banking.bank_name}.txt", 'w+') as file3:
            json.dump(Banking.__users_data, file3)

    def home_screen(self):
        print(f'''
            Welcome to {Banking.bank_name} bank...

                1) Login
                2) Sign up
            ''')

        try:
            option = int(input("\nEnter your option (1/2): "))
            assert option in [1, 2], "choose from 1 or 2"
            if option == 1:
                Banking.login(self)
            elif option == 2:
                Banking.sign_up(self)
        except Exception:
            print("Invalid Entry")
            Banking.home_screen(self)

    def acc_overview(self, user):
        acc_overview = {
            1: "deposit",
            2: "withdraw",
            3: "check_balance",
            4: "logout"
        }
        while Banking.logged_in:
            for key, value in acc_overview.items():
                print(f"\t{key}) {value}")
            try:
                option = int(input("Enter your option (1/2/3/4): "))
                assert option in [1, 2, 3, 4], "Select from 1/2/3/4"
                action = acc_overview[option]
                eval("Banking." + action + "(self, user)")

            except Exception:
                print("Invalid entry!")

    def logout(self, user):
        Banking.logged_in = False
        print(f"Thanks for using {Banking.bank_name} bank!\nVisit again...")
        # to append the data to Banking.txt
        Banking.updating_user_data(self)

    def login(self):
        while not Banking.logged_in:
            u1 = input("User name: ")
            u1 = u1.lower()
            # checks if the user-name exists in users-data
            if u1 in list(Banking.__users_data.keys()):
                # pulling out the corresponding password from users-data
                p2 = Banking.__users_data.get(u1).get('password')

                while True:
                    p1 = maskpass.advpass(prompt="Password:", mask="*")
                    if p1 == p2:
                        Banking.logged_in = True
                        print(f'Hello {u1}...')
                        Banking.acc_overview(self, user=u1)
                        return
                    else:
                        print("Incorrect password!")
            else:
                print("Invalid user name")

    def deposit(self, user):
        amount = int(input("Amount: "))
        bal = Banking.__users_data[user]['balance']
        Banking.__users_data[user]['balance'] = str(eval(bal) + amount)
        print(f'Amount "{amount}" successfully deposited!')
        print(f"Your current balance is {Banking.__users_data[user]['balance']}")

    def withdraw(self, user):
        amount = int(input("Amount: "))
        bal = Banking.__users_data[user]['balance']
        if eval(bal) < amount:
            print("insufficient balance")
        else:
            Banking.__users_data[user]['balance'] = str(eval(bal) - amount)
            print(f'Please collect your cash!')
            print(f"Your current balance is {Banking.__users_data[user]['balance']}")

    def check_balance(self, user):
        print(f"Your current balance is {Banking.__users_data[user]['balance']}")

    def sign_up(self):
        first_name = input("\nfirst name\t\t: ")
        last_name = input("last name\t\t: ")
        user_name = self.__user_name()
        email_id = self.__email()
        phone = input("phone no.\t\t: ")
        password = self.__password()
        account_type = input("Account type (Savings/ Current): ")
        account_no = str(eval(Banking.__last_account_no) + 1)
        balance = 0
        initial_dep_amt = int(input("Initial deposit amount: "))
        balance += initial_dep_amt
        print("Account has been created successfully!")
        print(f'Your account number is {account_no}')
        print(f'Your balance for account no {account_no} is {balance}')
        Banking.logged_in = True

        # appending new_user_data to dictionary __user_data
        Banking.__users_data.update({
            user_name: {
                'first_name': first_name,
                'last_name': last_name,
                'user_name': user_name,
                'email_id': email_id,
                'phone_no': phone,
                'password': password,
                'account_no': account_no,
                'account_type': account_type,
                'balance': str(balance)
            }
        })

        # to display account overview menu
        Banking.acc_overview(self, user=user_name)

    def __user_name(self):
        # checks if the user-name does not already exist
        while True:
            u = input("User name\t\t: ")
            if u not in list(Banking.__users_data.keys()):
                return u
            else:
                print("User name already exists. Please enter a unique username.")

    def __password(self):
        def confirm_password():
            p2 = maskpass.advpass(prompt="confirm password\t:", mask="*")
            if p2 == p:
                print("password confirmed!")
                return p
            else:
                print("Password does not match!")
                return confirm_password()

        # to check if the entered password is valid
        try:
            p = maskpass.advpass(prompt="Password\t\t:", mask="*")

            has_8char = len(p) >= 8
            has_lcase = re.search(r'[a-z]', p)
            has_ucase = re.search(r'[A-Z]', p)
            has_numerical = re.search(r'\d', p)
            has_special_char = re.search(r'\W', p)

            # valid only if all 5 variables are true
            valid = has_lcase and has_ucase and has_numerical and has_special_char and has_8char
            assert valid is True, '''
        password must include:

        - minimum of 8 characters
        - atleast 1 uppercase letter
        - atleast 1 lowercase letter
        - atleast 1 numerical digit
        - atleast 1 special character
        '''
            confirm_password()
            return p

        except AssertionError as e:
            print(e)
            self.__password()

    def __email(self):
        # to check if entered email is valid
        valid = False
        while not valid:
            e = input("email\t\t\t: ")
            pattern = '([\w]+)@([\w]+).com'
            match = re.search(pattern, e)
            if match:
                valid = True
            else:
                print("Invalid email address. Please try again.")

        return e


b1 = Banking()


