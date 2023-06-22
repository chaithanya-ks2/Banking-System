class Banking:
    __account_no = ['10000']
    __users_data = {}
    bank_name = ''
    logged_in = True

    def __init__(self, bank_name='XYZ'):
        Banking.bank_name = bank_name
        self.loading_user_data()
        self.home_screen()

    def loading_user_data(self):
        # loading all users' data from text file
        try:
            with open(f"{Banking.bank_name}.txt", "r") as file1:
                # splitting data into individual users
                __data = file1.read().split('\n')

                for i in __data:
                    # stripping {} from both ends
                    # splitting data into features
                    features = i[1:-1].split(",")

                    # converting it to dictionary format
                    __user_data = {}
                    # splitting features to key and value
                    for j in features:
                        j = j.split(':')
                        __user_data.update({j[0].strip().strip("'"): j[1].strip().strip("'")})

                    # updating details of each individual to __users_data attribute
                    Banking.__users_data.update({__user_data.get('user_name'): __user_data})

                    # updating all account numbers to __account_no attribute
                    Banking.__account_no.append(__user_data.get('account_no'))
        except FileNotFoundError:
            with open(f"{Banking.bank_name}.txt", "w") as file1:
                pass

    def home_screen(self):
        print(f'''
            Welcome to {Banking.bank_name} bank...
        
                1) Login
                2) Sign up
            ''')
        while Banking.logged_in:
            try:
                option = int(input("\nEnter your option (1/2): "))
                assert option in [1, 2], "choose from 1 or 2"
                if option == 1:
                    Banking.login(self)
                elif option == 2:
                    Banking.sign_up(self)
            except AssertionError as e:
                print(e)
            except ValueError:
                print("choose from 1 or 2")

    def acc_overview(self, user):
        while Banking.logged_in:
            print("""
                1) Deposit
                2) Withdraw
                3) Check balance
                4) Log out
                """)
            try:
                option = int(input("Enter your option (1/2/3/4): "))
                if option == 1:
                    Banking.deposit(self, user)
                elif option == 2:
                    Banking.withdraw(self, user)
                elif option == 3:
                    Banking.check_balance(self, user)
                elif option == 4:
                    Banking.logged_in = False
                    print(f"Thanks for using {Banking.bank_name} bank!\nVisit again...")
                    # to append the data to Banking.txt
                    Banking.updating_user_data(self)
                    break
                else:
                    print("Invalid option!!")
            except ValueError:
                print("Invalid entry!")

    def login(self):
        while True:
            u1 = input("User name: ")
            u1 = u1.lower()
            # checks if the user-name exists in users-data
            if u1 in list(Banking.__users_data.keys()):
                # pulling out the corresponding password from users-data
                p2 = Banking.__users_data.get(u1).get('password')

                while True:
                    p1 = input("Password: ")
                    if p1 == p2:
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
        account_no = str(eval(Banking.__account_no[-1]) + 1)
        balance = 0
        initial_dep_amt = int(input("Initial deposit amount: "))
        balance += initial_dep_amt
        print("Account has been created successfully!")
        print(f'Your account number is {account_no}')
        print(f'Your balance for account no {account_no} is {balance}')

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
            p2 = input("Confirm password: ")
            if p2 == p:
                print("password confirmed!")
                return p
            else:
                print("Password does not match!")
                return confirm_password()

        # to check if the entered password is valid
        try:
            lcase = list("abcdefghijklmnopqrstuvwxyz")
            ucase = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            numerical = list("0123456789")
            special_char = list("!@#$%^&*")

            p = input("password\t\t: ")

            has_8char = len(p) >= 8
            has_lcase = False
            has_ucase = False
            has_numerical = False
            has_special_char = False

            for i in p:
                if i in lcase:
                    has_lcase = True
                elif i in ucase:
                    has_ucase = True
                elif i in numerical:
                    has_numerical = True
                elif i in special_char:
                    has_special_char = True

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
        try:
            e = input("email\t\t\t: ")

            valid = False
            has_at = False
            has_dotcom = False

            for i in list(e):
                if i == '@':
                    has_at = True
            if e[-4:] == '.com':
                has_dotcom = True

            # to split mail id to user_name & domain_name
            if has_at and has_dotcom:
                user_name = ''
                domain_name = ''
                for i in range(len(e)):
                    if e[i] == '@':
                        user_name = (e[:i])
                        domain_name = (e[i:])
                        break

                # checks if user_name is not empty
                # checks if domain_name includes domain + extension. ie, domain.com
                valid = len(user_name) != 0 and len(domain_name) > 4

            assert valid is True, 'email id not found!'
        except AssertionError as er:
            print(er)
            self.__email()
        return e

    def updating_user_data(self):
        # overwriting all updated data
        with open(f"{Banking.bank_name}.txt", 'w') as file3:
            data = Banking.__users_data.values()
            data_i = (map(str, data))
            file3.write('\n'.join(data_i))


b1 = Banking('ABC')
