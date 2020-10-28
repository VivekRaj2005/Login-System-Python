# Importing all dependencies
from tkinter import *
import sqlite3
import os


# Variables
Account = [""]
dummyUser = "hello"
dummyPass = "1234"


# Check Equality in Objects
def CheckEquality(obj1, obj2) -> bool:
    return obj1 == obj2


# Class for return type of checkLogin (68,4) Function
class CheckLog:
    def __init__(self, status, code):
        self.status = status
        self.code = code


# Class for controlling Login.db
class Database:
    def __init__(self, database="Login.db"):
        # Connecting The Database if Login.db already exist
        if os.path.exists(database):
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()
        # Connecting the Database if Login.db do not exist
        else:
            # Creating the database with an account (ADMIN)
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()
            # Creating The Table
            self.cursor.execute("CREATE TABLE Login ('NAME' Text ,'PASSWORD' Text)")
            self.cursor.execute("CREATE TABLE BioData ('NAME' Text ,'EMAIL' Text,'PASS1' Text,'PASS2' Text)")
            # Creating a Sample Account
            self.cursor.execute("INSERT INTO Login VALUES ('ADMIN','1234')")
            self.cursor.execute("INSERT INTO BioData VALUES ('ADMIN','','1234','1234')")
            self.connection.commit()

    # Function to help to change the password
    def ChangePass(self, user, password):
        bio_data = self.fetchCurrentBioData(user)
        print(bio_data)
        self.cursor.execute(f"DELETE FROM Login WHERE NAME = '{user}'")
        self.cursor.execute(f"DELETE FROM BioData WHERE NAME = '{user}'")
        self.cursor.execute(f"INSERT INTO Login VALUES ('{user}','{password}')")
        self.cursor.execute(f"INSERT INTO BioData VALUES ('{user}','{bio_data[1]}','{password}','{password}')")
        self.connection.commit()

    # Function To Help to create a new Account
    def NewAccount(self, username, email, pass1, pass2) -> bool:
        try:
            self.cursor.execute(f"INSERT INTO Login VALUES ('{username}','{pass1}')")
            self.cursor.execute(f"INSERT INTO BioData VALUES ('{username}','{email}','{pass1}','{pass2}')")
            self.connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    # Function To Fetch The Login data
    def fetchLoginData(self) -> []:
        self.cursor.execute(f"SELECT * FROM Login")
        return self.cursor.fetchall()

    # Function To Fetch The Bio data
    def fetchBioData(self) -> []:
        self.cursor.execute(f"SELECT * FROM BioData")
        return self.cursor.fetchall()

    # Function To Check Authorisation
    def checkLogin(self, username, password) -> CheckLog:
        data = self.fetchLoginData()
        for bits in data:
            if CheckEquality(bits[0], username):
                if CheckEquality(bits[1], password):
                    return CheckLog(True, 0)
                else:
                    return CheckLog(False, 1)
        return CheckLog(False, 2)

    # Function To Fetch The Bio data of a particular user
    def fetchCurrentBioData(self, user):
        self.cursor.execute(f"SELECT * FROM BioData WHERE NAME = '{user}'")
        one = self.cursor.fetchall()
        one = one[0]
        return one


# Screen after Login
class MainWindow:
    def __init__(self):
        data = Database()
        bio_data = data.fetchCurrentBioData(Account[0])
        # Creating The main Window Screen
        self.screen = Tk()
        self.screen.title("WELCOME")
        # Creating The main Window Components
        self.WelcomeMessage = Label(self.screen, text=f"Welcome,{Account[0]}")
        self.NameLab = Label(self.screen, text="Username")
        self.NameLabel = Label(self.screen, text=bio_data[0])
        self.EmailLab = Label(self.screen, text="Email")
        self.EmailLabel = Label(self.screen, text=bio_data[1])
        self.PassLab = Label(self.screen, text="Password")
        self.PassLabel = Label(self.screen, text=bio_data[2])
        self.ChangePassword = Button(self.screen, text="Change Password", command=self.ChangePass)
        self.QuitButton = Button(self.screen, text="Quit", command=self.screen.quit)
        # Creating The main Window Spacing Labels
        label1 = Label(self.screen, pady=10)
        label2 = Label(self.screen, padx=1)
        # Putting the components on the screen
        self.WelcomeMessage.grid(row=0, column=0, columnspan=3)
        self.NameLab.grid(row=1, column=0)
        self.NameLabel.grid(row=1, column=2)
        self.EmailLab.grid(row=2, column=0)
        self.EmailLabel.grid(row=2, column=2)
        self.PassLab.grid(row=3, column=0)
        self.PassLabel.grid(row=3, column=2)
        label1.grid(row=4, column=0, columnspan=3)
        self.ChangePassword.grid(row=5, column=0)
        label2.grid(row=5, column=1)
        self.QuitButton.grid(row=5, column=2)

    # Function to run the class
    def run(self):
        self.screen.mainloop()

    # Function to change the window
    def ChangePass(self):
        self.screen.destroy()
        d = ChangePass()
        d.run()


# Screen to change the Password
class ChangePass:
    def __init__(self):
        # Creating The main Window Screen
        self.screen = Tk()
        self.screen.title("Change Password")
        # Creating The main Window Components
        self.Pass1Label = Label(self.screen, text="Password:")
        self.Pass2Label = Label(self.screen, text="Retype Password")
        self.Pass1Input = Entry(self.screen)
        self.Pass2Input = Entry(self.screen)
        self.Ok = Button(self.screen, text="OK", command=self.ChangePass)
        # Putting the components on the screen
        self.Pass1Label.grid(row=0, column=0)
        self.Pass1Input.grid(row=0, column=1)
        self.Pass2Label.grid(row=1, column=0)
        self.Pass2Input.grid(row=1, column=1)
        self.Ok.grid(row=2, column=0, columnspan=2)

    # Function to run the class
    def run(self):
        self.screen.mainloop()

    # Function to change the window
    def login(self):
        self.screen.destroy()
        d = LoginScreen()
        d.run()

    def ChangePass(self):
        data = Database()
        pass1 = self.Pass1Input.get()
        if CheckEquality(pass1, self.Pass2Input.get()):
            data.ChangePass(Account[0], self.Pass1Input.get())
            print("Submitted")
            self.login()

        else:
            print("Failed")


# Screen for signing up
class NewAccount:
    def __init__(self):
        # Creating The main Window Screen
        self.screen = Tk()
        self.screen.title("New Account")
        # Creating The main Window Components
        self.userLabel = Label(self.screen, text="Username")
        self.UsernameInput = Entry(self.screen)
        self.EmailLabel = Label(self.screen, text="Email")
        self.EmailInput = Entry(self.screen)
        self.PassLabel = Label(self.screen, text="Password")
        self.PasswordInput = Entry(self.screen)
        self.PassRetypeLabel = Label(self.screen, text="Retype Password")
        self.PassRetype = Entry(self.screen)
        self.OKButton = Button(self.screen, text="OK", command=self.submit)
        self.ExitButton = Button(self.screen, text="QUIT", command=self.screen.quit)
        # Creating The main Window Spacing Labels
        label1 = Label(self.screen, padx=2)
        label2 = Label(self.screen, padx=2)
        label3 = Label(self.screen, padx=2)
        # Putting the components on the screen
        self.userLabel.grid(row=1, column=0)
        self.UsernameInput.grid(row=1, column=1)
        label1.grid(row=2, column=0, columnspan=2)
        self.EmailLabel.grid(row=3, column=0)
        self.EmailInput.grid(row=3, column=1)
        label2.grid(row=4, column=0, columnspan=2)
        self.PassLabel.grid(row=5, column=0)
        self.PasswordInput.grid(row=5, column=1)
        label3.grid(row=6, column=0, columnspan=2)
        self.PassRetypeLabel.grid(row=7, column=0)
        self.PassRetype.grid(row=7, column=1)
        label = Label(self.screen, padx=2)
        label.grid(row=8, column=0, columnspan=2)
        self.OKButton.grid(row=9, column=0)
        self.ExitButton.grid(row=9, column=1)

    # Function to run the class
    def run(self):
        self.screen.mainloop()

    def submit(self):
        user_ = self.UsernameInput.get()
        email = self.EmailInput.get()
        pass1 = self.PasswordInput.get()
        pass2 = self.PassRetype.get()
        if CheckEquality(pass2, pass1):
            b = Database()
            b.NewAccount(user_, email, pass1, pass2)
            print("Submitted")
            # changing the window
            self.screen.destroy()
            c = LoginScreen()
            c.run()
        else:
            print("Error")


# Screen For Login
class LoginScreen:
    def __init__(self):
        # Creating The main Window Screen
        self.screen = Tk()
        self.screen.title("Login")
        # Creating The main Window Components
        self.userLabel = Label(self.screen, text="Username")
        self.UsernameInput = Entry(self.screen)
        self.PassLabel = Label(self.screen, text="Password")
        self.PasswordInput = Entry(self.screen)
        self.OKButton = Button(self.screen, text="OK", command=self.runCheck)
        self.ExitButton = Button(self.screen, text="QUIT", command=self.screen.quit)
        self.NewAccount = Button(self.screen, text="New Account", command=self.NewAccountWindow)
        # Creating The main Window Spacing Labels
        label1 = Label(self.screen, padx=2)
        label2 = Label(self.screen, padx=2)
        label3 = Label(self.screen, padx=2)
        # Putting the components on the screen
        self.userLabel.grid(row=1, column=0)
        self.PassLabel.grid(row=3, column=0)
        self.UsernameInput.grid(row=1, column=1)
        label1.grid(row=2, column=0, columnspan=2)
        self.PasswordInput.grid(row=3, column=1)
        label2.grid(row=4, column=0, columnspan=2)
        self.OKButton.grid(row=5, column=0)
        label3.grid(row=6, column=0, columnspan=2)
        self.ExitButton.grid(row=7, column=0, columnspan=2)
        self.NewAccount.grid(row=5, column=1)

    # Function to run the class
    def run(self):
        self.screen.mainloop()

    # Function to change the window
    def NewAccountWindow(self):
        new = NewAccount()
        self.screen.destroy()
        new.run()

    # Function to change the window
    def loginSuccess(self):
        main = MainWindow()
        self.screen.destroy()
        main.run()

    def runCheck(self):
        data = Database()
        response = data.checkLogin(self.UsernameInput.get(), self.PasswordInput.get())
        if CheckEquality(response.status, True):
            Account[0] = self.UsernameInput.get()
            print(data.fetchCurrentBioData(Account[0]))
            self.loginSuccess()
        else:
            if CheckEquality(response.code, 1):
                print("Password Incorrect")
            else:
                print("Account not Found")


if __name__ == '__main__':
    LoginScreen().run()

