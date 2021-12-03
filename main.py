from gui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import re
import sys
import os
from datetime import date, timedelta, datetime
import json


class Ui_MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        f = open('account.json', )
        data = json.load(f)
        f.close()
        self.all_data = data['accounts']

        f = open('books.json', )
        books = json.load(f)
        f.close()
        self.all_books = books['books']

        # setting min max date
        self.today = date.today()
        self.dateEdit.setMinimumDate(self.today)
        self.dateEdit.setMaximumDate(self.today + timedelta(days=10))

        # error messaege
        self.msg = QMessageBox()
        self.msg.setWindowTitle('Warning!')
        self.msg.setIcon(QMessageBox.Critical)

        self.msg_success = QMessageBox()
        self.msg_success.setWindowTitle('Success!')
        self.msg_success.setIcon(QMessageBox.Information)

        # init books
        self.books_for_search = []

        self.loginFrame.show()
        self.userinforFrame.hide()
        self.reserveFrame.hide()
        self.liabilitiesFrame.hide()
        self.homeFrame.hide()
        self.barrowFrame.hide()
        self.returnFrame.hide()
        self.authLABEL.hide()

        self.loginBTN.clicked.connect(self.login)
        self.logoutBTN.clicked.connect(self.logout)

        # login
        self.whoIsUser = None
        self.booksBarrowed_copy = []  # for geting the fines
        self.booksBarrowed = []  # current user barrowed books
        self.booksReserved = []  # current user reserved books
        self.fines = 0

        # home page
        self.searchHOME.textChanged.connect(self.filterSearch)
        self.listHOME.itemClicked.connect(self.whatBookIsSelected)
        # menu
        self.barrowBTN.clicked.connect(self.showBarrowFrame)
        self.returnBTN.clicked.connect(self.showReturnFrame)
        self.reservedBTN.clicked.connect(self.showReservedFrame)
        self.liabilitiesBTN.clicked.connect(self.showLiabilitiesFrame)
        self.userinfoBTN.clicked.connect(self.showUserInfo)

        # barrow page
        self.searchBARROW.textChanged.connect(self.filterSearchBarrow)
        self.listBARROW.itemClicked.connect(self.whatBookIsSelectedBarrow)
        self.backHomeBTN.clicked.connect(self.showHome)
        self.barrowBookBTN.clicked.connect(self.barrowThisBook)
        self.reservedBookBTN.clicked.connect(self.reservedThisBook)
        self.global_i = None  # this is what book did user select in barrow page

        # return page
        self.backHomeBTN_2.clicked.connect(self.showHome)
        self.listRETURN.itemClicked.connect(self.whatBookIsSelectedReturn)
        self.returnBookBTN.clicked.connect(self.returnThisBook)
        self.global_name = None
        self.global_r = None

        # reserve page
        self.backBTN.clicked.connect(self.showHome)

        # liabilities page
        self.payBTN.clicked.connect(self.pay)
        self.goHome.clicked.connect(self.showHome)

        #user info frame
        self.backHome.clicked.connect(self.showHome)

    def showUserInfo(self):
        self.homeFrame.hide()
        self.userinforFrame.hide()
        self.loginFrame.hide()
        self.barrowFrame.hide()
        self.returnFrame.hide()
        self.reserveFrame.hide()
        self.liabilitiesFrame.hide()
        self.userinforFrame.show()
        self.reset()

    def filterSearch(self, keyword):
        datalist = self.books_for_search
        keyword = keyword.upper()
        done_filter = (
            [val for val in datalist if re.search(r'' + keyword, val)])

        self.listHOME.clear()
        for i in range(len(done_filter)):
            self.listHOME.addItem(done_filter[i])

    def filterSearchBarrow(self, keyword):
        datalist = self.books_for_search
        keyword = keyword.upper()
        done_filter = (
            [val for val in datalist if re.search(r'' + keyword, val)])

        self.listBARROW.clear()
        for i in range(len(done_filter)):
            self.listBARROW.addItem(done_filter[i])

    def login(self):
        try:
            user = self.username.text()
            passwrd = self.password.text()
            self.reset()

            for i in range(len(self.all_data)):
                if user == self.all_data[i]["Username"] and passwrd == self.all_data[i]["Password"]:
                    self.username.clear()
                    self.password.clear()
                    self.showHome()
                    self.whoIsUser = i
                    self.booksBarrowed = self.all_data[self.whoIsUser]["barrowBooks"]
                    self.booksReserved = self.all_data[self.whoIsUser]["reservedBooks"]
                    fname = self.all_data[self.whoIsUser]["FirstName"]
                    lname = self.all_data[self.whoIsUser]["LastName"]
                    sr = self.all_data[self.whoIsUser]['Username']
                    m = self.all_data[self.whoIsUser]["MI"]
                    cnumber = self.all_data[self.whoIsUser]["Number"]
                    address = self.all_data[self.whoIsUser]["address"]
                    self.srLABEL.setText(f"SR-Code: {sr}")
                    self.nLABEL.setText(f"Name: {fname} {m} {lname}")
                    self.cLABEL.setText(f"Contact No.: {cnumber}")
                    self.aLABEL.setText(f"Address: {address}")
                    self.label_6.setText(f"Hi, {fname}!")
                    self.fines = self.all_data[self.whoIsUser]["liabilities"]

                else:
                    self.username.clear()
                    self.password.clear()
                    self.authLABEL.show()
            self.listHOME.clear()
            self.listBARROW.clear()
            books = self.all_books
            for i in range(len(books)):
                book = f"{books[i]['Type']} | {books[i]['Title']} | {books[i]['Author']} | {books[i]['DatePublished']}".upper(
                )
                self.listHOME.addItem(book)
                self.listBARROW.addItem(book)
                self.books_for_search.append(book)
        except Exception as e:
            print(f"error in login: {e}")

    def logout(self):
        if self.fines > 0:
            self.msg.setText('Pay your balances in liabilities before leaving')
            self.msg.exec_()
        else:
            self.authLABEL.hide()
            self.homeFrame.hide()
            self.userinforFrame.hide()
            self.loginFrame.show()
            self.barrowFrame.hide()
            self.returnFrame.hide()
            self.reserveFrame.hide()
            self.liabilitiesFrame.hide()

    def showHome(self):
        self.homeFrame.show()
        self.userinforFrame.hide()
        self.loginFrame.hide()
        self.barrowFrame.hide()
        self.returnFrame.hide()
        self.reserveFrame.hide()
        self.liabilitiesFrame.hide()
        self.reset()
        self.calFine()

    def showBarrowFrame(self):
        try:
            self.homeFrame.hide()
            self.loginFrame.hide()
            self.userinforFrame.hide()
            self.barrowFrame.show()
            self.returnFrame.hide()
            self.reserveFrame.hide()
            self.liabilitiesFrame.hide()
            self.reset()
            self.calFine()
            self.totalBarrowedLABEL.setText(
                f"Total Barrowed Books: {len(self.booksBarrowed)}")
            self.totalBarrowedLABEL_2.setText(
                f"Total Barrowed Books: {len(self.booksBarrowed)}")
        except Exception as e:
            print(f"error at showBarrowFrame: {e}")

    def showReturnFrame(self):
        try:
            self.homeFrame.hide()
            self.loginFrame.hide()
            self.userinforFrame.hide()
            self.barrowFrame.hide()
            self.returnFrame.show()
            self.reserveFrame.hide()
            self.liabilitiesFrame.hide()
            self.reset()
            bBooks = self.booksBarrowed
            self.listRETURN.clear()
            self.reset()
            for i in range(len(bBooks)):
                self.listRETURN.addItem(
                    f"{bBooks[i][0][1]} | {bBooks[i][0][2]} | {bBooks[i][0][3]} | {bBooks[i][0][4]}".upper())
                self.calFine()
        except Exception as e:
            print(f"error at showReturnFrame: {e}")

    def showReservedFrame(self):
        try:
            self.homeFrame.hide()
            self.userinforFrame.hide()
            self.loginFrame.hide()
            self.barrowFrame.hide()
            self.returnFrame.hide()
            self.reserveFrame.show()
            self.liabilitiesFrame.hide()

        except Exception as e:
            print(f"error in showReserveFrame: {e}")

    def showLiabilitiesFrame(self):
        try:
            self.homeFrame.hide()
            self.userinforFrame.hide()
            self.loginFrame.hide()
            self.barrowFrame.hide()
            self.returnFrame.hide()
            self.reserveFrame.hide()
            self.liabilitiesFrame.show()
            self.liabilitiesLABEL.setText(f"P {self.fines}.00")

        except Exception as e:
            print(f"error in showLiabilitiesFrame: {e}")

    def whatBookIsSelected(self, book):
        i = self.books_for_search.index(book.text())
        book = self.all_books[i]
        # home page
        self.list_infoHOME.clear()
        self.list_infoHOME.addItem(f"ID: {book['ID']}")
        self.list_infoHOME.addItem(f"Type: {book['Type']}")
        self.list_infoHOME.addItem(f"Title: {book['Title']}")
        self.list_infoHOME.addItem(f"Author: {book['Author']}")
        self.list_infoHOME.addItem(f"Date Published: {book['DatePublished']}")
        self.list_infoHOME.addItem(f"Rack No.: {book['Rack']}")
        self.list_infoHOME.addItem(f"Copies: {book['Copies']}")

    def whatBookIsSelectedBarrow(self, book):
        i = self.books_for_search.index(book.text())
        book = self.all_books[i]
        self.global_i = i
        # barrow page
        self.list_infoBARROW.clear()
        self.list_infoBARROW.addItem(f"ID: {book['ID']}")
        self.list_infoBARROW.addItem(f"Type: {book['Type']}")
        self.list_infoBARROW.addItem(f"Title: {book['Title']}")
        self.list_infoBARROW.addItem(f"Author: {book['Author']}")
        self.list_infoBARROW.addItem(
            f"Date Published: {book['DatePublished']}")
        self.list_infoBARROW.addItem(f"Rack No.: {book['Rack']}")
        self.list_infoBARROW.addItem(f"Copies: {book['Copies']}")

    def whatBookIsSelectedReturn(self, book):
        try:
            i = self.books_for_search.index(book.text())  # for info display
            self.global_name = book.text()
            book = self.all_books[i]

            self.list_infoRETURN.clear()
            self.list_infoRETURN.addItem(f"ID: {book['ID']}")
            self.list_infoRETURN.addItem(f"Type: {book['Type']}")
            self.list_infoRETURN.addItem(f"Title: {book['Title']}")
            self.list_infoRETURN.addItem(f"Author: {book['Author']}")
            self.list_infoRETURN.addItem(
                f"Date Published: {book['DatePublished']}")
            self.list_infoRETURN.addItem(f"Rack No.: {book['Rack']}")
            self.list_infoRETURN.addItem(f"Copies: {book['Copies']}")

            curRow = self.listRETURN.currentRow()
            self.global_r = curRow
            dueDate = self.booksBarrowed[curRow][1]
            self.dueDateLABEL.setText(dueDate)

            # check if overdue
            day = int(dueDate[0:2])
            month = int(dueDate[3:5])
            yr = int(dueDate[-4:])
            newDueDate = date(yr, month, day)

            if newDueDate < self.today:
                self.penaltyLABEL.setText("Over Due: P 10.00")
            else:
                self.penaltyLABEL.setText("No penalty")

        except Exception as e:
            print(f"error in whatBookIsSelectedReturn: {e}")

    def returnThisBook(self):
        try:
            if self.global_r == None:
                self.msg.setText('Please select book first')
                self.msg.exec_()
            else:

                i = self.books_for_search.index(self.global_name)  # index in
                copies = self.all_books[i]["Copies"]
                copies += 1
                self.all_books[i]["Copies"] = copies
                del self.booksBarrowed[self.global_r]

                self.global_name = None
                self.reset()

                bBooks = self.booksBarrowed
                self.listRETURN.clear()
                for i in range(len(bBooks)):
                    self.listRETURN.addItem(
                        f"{bBooks[i][0][1]} | {bBooks[i][0][2]} | {bBooks[i][0][3]} | {bBooks[i][0][4]}".upper())
                self.totalBarrowedLABEL.setText(
                    f"Total Barrowed Books: {len(self.booksBarrowed)}")
                self.totalBarrowedLABEL_2.setText(
                    f"Total Barrowed Books: {len(self.booksBarrowed)}")

                # save in account json file
                self.all_data[self.whoIsUser]["barrowBooks"] = self.booksBarrowed
                # print(self.all_data)
                all_data = {"accounts": self.all_data}
                f = open("account.json", "w")
                json.dump(all_data, f)
                f.close()

        except Exception as e:
            print(f"error in returnThisBook: {e}")

    def barrowThisBook(self):
        try:
            if self.global_i == None:
                self.msg.setText('Please select book first')
                self.msg.exec_()
            else:
                if len(self.booksBarrowed) == 5:
                    self.msg.setText('You can only barrow 5 books.')
                    self.msg.exec_()
                else:
                    books = self.all_books[self.global_i]
                    copies = books["Copies"]
                    if copies == 0:
                        self.msg.setText(
                            'There is no available copies of this book.')
                        self.msg.exec_()
                    else:
                        self.msg_success.setText('Successfully Barrowed!')
                        self.msg_success.exec_()
                        datee = self.dateEdit.date().toString("dd/MM/yyyy")
                        copies -= 1
                        books["Copies"] = copies
                        newList = [[books["ID"], books["Type"], books["Title"], books["Author"],
                                    books["DatePublished"], books["Rack"], books["Copies"]], datee]
                        self.booksBarrowed.append(newList)
                        self.booksBarrowed_copy.append(newList)
                        self.totalBarrowedLABEL.setText(
                            f"Total Barrowed Books: {len(self.booksBarrowed)}")
                        self.totalBarrowedLABEL_2.setText(
                            f"Total Barrowed Books: {len(self.booksBarrowed)}")

                        # save updated copies in book json file
                        self.all_books[self.global_i]["Copies"] = copies
                        all_books = {"books": self.all_books}
                        f = open("books.json", "w")
                        json.dump(all_books, f)
                        f.close()

                        # save in account json file
                        self.all_data[self.whoIsUser]["barrowBooks"] = self.booksBarrowed
                        # print(self.all_data)
                        all_data = {"accounts": self.all_data}
                        f = open("account.json", "w")
                        json.dump(all_data, f)
                        f.close()
                        self.list_infoBARROW.clear()
                        self.global_i = None

        except Exception as e:
            print(f"errow at barrowThisBook: {e}")

    def reservedThisBook(self):
        try:
            if self.global_i == None:
                self.msg.setText('Please select book first')
                self.msg.exec_()
            else:
                books = self.all_books[self.global_i]
                self.msg_success.setText('Successfully reserved!')
                self.msg_success.exec_()
                newList = [books["ID"], books["Type"], books["Title"], books["Author"],
                           books["DatePublished"], books["Rack"], books["Copies"]]
                self.booksReserved.append(newList)
                self.global_i = None
                self.list_infoBARROW.clear()
                # display to reserved list
                self.listReserved.clear()
                books = self.booksReserved
                print(books)
                for i in range(len(books)):
                    book = f"{books[i][1]} | {books[i][2]} | {books[i][3]} | {books[i][4]}"
                    self.listReserved.addItem(book)

                # saved to json file
                self.all_data[self.whoIsUser]["reservedBooks"] = self.booksReserved
                all_data = {"accounts": self.all_data}
                f = open("account.json", "w")
                json.dump(all_data, f)
                f.close()
        except Exception as e:
            print(f"error in reservedThisBook: {e}")

    def reset(self):
        # reset everything
        # home
        self.list_infoHOME.clear()
        self.searchHOME.clear()
        # barrow page
        self.searchBARROW.clear()
        self.list_infoBARROW.clear()
        self.global_i = None
        # return page
        self.list_infoRETURN.clear()
        self.dueDateLABEL.clear()
        self.penaltyLABEL.clear()
        self.global_r = None
        # liabilities page
        self.changeLABEL.clear()
        self.money.clear()
        # USERiNFO

    def calFine(self):
        try:
            self.fines = 0
            allBarrowed = self.booksBarrowed_copy
            for i in range(len(allBarrowed)):
                dueDate = allBarrowed[i][1]
                # check if overdue
                day = int(dueDate[0:2])
                month = int(dueDate[3:5])
                yr = int(dueDate[-4:])
                newDueDate = date(yr, month, day)

                if newDueDate < self.today:
                    self.fines += 10
                    # update and save the data in the json account
                    self.all_data[self.whoIsUser]["liabilities"] = self.fines
                    all_data = {"accounts": self.all_data}
                    f = open("account.json", "w")
                    json.dump(all_data, f)
                    f.close()
        except Exception as e:
            print(f"error in calfines: {e}")

    def pay(self):
        try:
            money = int(self.money.text())
            if money < self.fines:
                self.msg.setText("Your money is not enough!")
                self.msg.exec_()
                self.changeLABEL.setText("Change:")
            else:
                self.msg_success.setText("Thank you for paying!!")
                self.msg_success.exec_()
                self.booksBarrowed_copy = []
                change = money - self.fines
                self.fines = 0
                self.changeLABEL.setText(f"Change: {change}")
                self.liabilitiesLABEL.setText(f"P {self.fines}.00")
                self.money.clear()
                self.all_data[self.whoIsUser]["liabilities"] = self.fines
                all_data = {"accounts": self.all_data}
                f = open("account.json", "w")
                json.dump(all_data, f)
                f.close()
                self.calFine()
        except Exception as e:
            print(f"error in pay: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    iWindow = Ui_MainWindow()
    iWindow.show()
    sys.exit(app.exec_())
