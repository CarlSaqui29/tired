from ui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import re
import sys
import os
from datetime import date, timedelta,datetime


class Ui_MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.today = date.today()
        # self.date.setMinimumDate(self.today)
        self.date.setMaximumDate(self.today + timedelta(days=10))

        self.msg = QMessageBox()
        self.msg.setWindowTitle('Warning!')
        self.msg.setText('Pay your balances in liabilities before leaving')
        self.msg.setIcon(QMessageBox.Critical)

        # init accs
        self.accounts = []
        self.barrowers = []  # who baroowed the books
        self.allBarrowedBooks = []  # allbooks that is barrowed 2d array
        self.barrowedBooks_User = []  # current user barrowed books
        self.reservedBooks_User = []  # current user reserved books
        self.currentUser = ''
        self.selectedBook = []
        self.indexofSelectedBook = ''
        self.selectedBookIDX = ''

        # init books
        self.allBooks = []
        self.bookListAll = []
        self.strings = []

        # login init
        self.loginFrame.show()
        self.labelWrongCredential.hide()
        self.loginBTN.clicked.connect(self.login)

        # init home
        self.homeFrame.hide()
        self.searchBook.textChanged.connect(self.filter_search)
        self.bookList.itemClicked.connect(self.what_book_selected)
        self.labelINFO.setText(
            "Subject:\nTitle:\nAuthor:\nDate:\nRack No.:\nCopies:")
        self.barrowBookBTN.clicked.connect(self.showBarrowFrame)
        self.logoutBTN.clicked.connect(self.logout)

        # init barrow
        self.barrowFrame.hide()
        self.backHome_barrow.clicked.connect(self.showHomeFrame)
        self.searchBook_barrow.textChanged.connect(self.filter_search)
        self.bookList_barrow.itemClicked.connect(self.what_book_selected)
        self.signal = False
        self.barrowThis.clicked.connect(self.barrowBook)

        # init return
        self.returnFrame.hide()
        self.bookList_return.clear()
        self.returnBookBTN.clicked.connect(self.showReturnFrame)
        self.backHome_return.clicked.connect(self.showHomeFrame)
        self.dateBarrowed.setText("")
        self.bookList_return.itemClicked.connect(self.what_book_selected)
        self.returnThis.clicked.connect(self.returnBook)

        # init liabilities
        self.liabilities.hide()
        self.liabilitiesBTN.clicked.connect(self.showliabilitiesFrame)
        self.backHome_liabilities.clicked.connect(self.showHomeFrame)
        self.sendPaymentBTN.clicked.connect(self.pay)
        self.tf = 0

        # init reserved
        self.reservedFrame.hide()
        self.reservedBookBTN.clicked.connect(self.showReservedFrame)
        self.backHome_reserved.clicked.connect(self.showHomeFrame)
        self.reservedBooks = []
        self.reservedThis.clicked.connect(self.reserved)


    def login(self):
        self.change.clear()
        username = self.username.text()
        password = self.password.text()
        bookFile = open('accounts.txt', 'r')
        Lines = bookFile.readlines()
        for line in Lines:
            newList = line.strip()
            newList = list(newList.split("|"))
            self.accounts.append(newList)
        for i in range(len(self.accounts)):
            if username == self.accounts[i][0] and password == self.accounts[i][1]:
                # if username == '':
                self.user.setText(f"Hello, {self.accounts[i][2]}")
                self.showHomeFrame()
                self.initBookList()
                self.currentUser = username
        else:
            self.labelWrongCredential.show()

    def showHomeFrame(self):
        self.loginFrame.hide()
        self.barrowFrame.hide()
        self.homeFrame.show()
        self.liabilities.hide()
        self.reservedFrame.hide()
        self.returnFrame.hide()
        self.searchBook.clear()
        self.labelINFO.setText(
            "Subject:\nTitle:\nAuthor:\nDate:\nRack No.:\nCopies:")
        # ID-RACK-SUBJECT-TITLE-AUTHOR-DATE-COPIES
        self.calFines()

    def showBarrowFrame(self):
        self.loginFrame.hide()
        self.barrowFrame.show()
        self.homeFrame.hide()
        self.liabilities.hide()
        self.reservedFrame.hide()
        self.returnFrame.hide()
        self.searchBook_barrow.clear()
        self.labelINFO_barrow.setText(
            "Subject:\nTitle:\nAuthor:\nDate:\nRack No.:\nCopies:")
        self.selectedBook = []
        self.label_18.setText(f"Total barrowed book: {len(self.strings)}")
        # self.signal = False
        # if self.signal == False:
        #     self.reservedThis.setEnabled(False)
        #     self.barrowThis.setEnabled(False)

    def showliabilitiesFrame(self):
        self.change.clear()
        self.loginFrame.hide()
        self.barrowFrame.hide()
        self.homeFrame.hide()
        self.liabilities.show()
        self.reservedFrame.hide()
        self.returnFrame.hide()
        self.calFines()

    def showReservedFrame(self):
        self.loginFrame.hide()
        self.barrowFrame.hide()
        self.homeFrame.hide()
        self.liabilities.hide()
        self.reservedFrame.show()
        self.returnFrame.hide()

    def showReturnFrame(self):
        self.loginFrame.hide()
        self.barrowFrame.hide()
        self.homeFrame.hide()
        self.liabilities.hide()
        self.reservedFrame.hide()
        self.returnFrame.show()
        self.dateBarrowed.clear()
        self.fineAmount.setText("0")
        self.labelINFO_return.setText(
            "Subject:\nTitle:\nAuthor:\nDate:\nRack No.:\nCopies:")
        self.returnThis.setEnabled(False)
        self.calFines()

    def initBookList(self):
        bookFile = open('books.txt', 'r')
        Lines = bookFile.readlines()

        for line in Lines:
            newList = line.strip()
            newList = list(newList.split("|"))
            self.allBooks.append(newList)

        self.bookList.clear()
        self.bookList_barrow.clear()
        for i in range(len(self.allBooks)):
            book = f"{self.allBooks[i][2]} | {self.allBooks[i][3]} | {self.allBooks[i][4]} | {self.allBooks[i][5]}"
            book = book.upper()

            self.bookList.addItem(book)
            self.bookList_barrow.addItem(book)
            self.bookListAll.append(book)

    def filter_search(self, keyword):
        datalist = self.bookListAll
        keyword = keyword.upper()
        done_filter = (
            [val for val in datalist if re.search(r'' + keyword, val)])

        self.bookList.clear()
        self.bookList_barrow.clear()
        for i in range(len(done_filter)):
            self.bookList.addItem(done_filter[i])
            self.bookList_barrow.addItem(done_filter[i])

    def what_book_selected(self, book):

        try:
            i = self.bookListAll.index(book.text().upper())
            a = self.allBooks[i]
            self.selectedBook = a
            self.indexofSelectedBook = i
            self.labelINFO.setText(
                f"Subject: {a[2]}\nTitle: {a[3]}\nAuthor: {a[4]}\nDate: {a[5]}\nRack No.: {a[1]}\nCopies: {a[6]}")
            self.labelINFO_barrow.setText(
                f"Subject: {a[2]}\nTitle: {a[3]}\nAuthor: {a[4]}\nDate: {a[5]}\nRack No.: {a[1]}\nCopies: {a[6]}")
            self.labelINFO_return.setText(
                f"Subject: {a[2]}\nTitle: {a[3]}\nAuthor: {a[4]}\nDate: {a[5]}\nRack No.: {a[1]}\nCopies: {a[6]}")

            if len(self.strings) > 0:
                # string = f"{a[2]} | {a[3]} | {a[4]} | {a[5]}"
                date = self.barrowedBooks_User[self.bookList_return.currentRow()][1]
                fine = self.barrowedBooks_User[self.bookList_return.currentRow()][-1]
                self.dateBarrowed.setText(date)
                self.fineAmount.setText(str(fine))
                print(self.bookList_return.currentRow())
                self.selectedBookIDX = self.bookList_return.currentRow()

            if len(self.strings) == 4:
                self.barrowThis.setEnabled(False)
                self.date.setEnabled(False)
            else:
                self.barrowThis.setEnabled(True)

            self.signal = True
            self.reservedThis.setEnabled(True)
            self.returnThis.setEnabled(True)

        except Exception as e:
            print(e)

    def barrowBook(self):
        self.barrowers.append(self.currentUser)

        datee = self.date.date().toString("dd/MM/yyyy")
        if len(self.strings) == 4:
            self.barrowThis.setEnabled(False)
            self.date.setEnabled(False)
        else:
            self.barrowThis.setEnabled(True)

        try:
            string = f"{self.selectedBook[2]} | {self.selectedBook[3]} | {self.selectedBook[4]} | {self.selectedBook[5]}"
            self.strings.append(string)
            print(self.strings)
            self.label_18.setText(f"Total barrowed book: {len(self.strings)}")
            print(f"self.strings {self.strings}")
            barrowInfo = [self.selectedBook, datee, self.currentUser, 0]
            self.barrowedBooks_User.append(barrowInfo)
            barrower = [self.currentUser, self.selectedBook[3]]
            self.allBarrowedBooks.append(barrower)
            print(f"all barrowers: {self.barrowers}")
            print(f"barrow by user {self.barrowedBooks_User}")
            print(f"all barrowed books w/ barrower {self.barrowedBooks_User}")
            self.displayBarrowedBooks()
        except Exception as e:
            print(e)

    def displayBarrowedBooks(self):
        a = self.barrowedBooks_User
        self.bookList_return.clear()
        for i in range(len(a)):
            self.bookList_return.addItem(f"{a[i][0][2]} | {a[i][0][3]} | {a[i][0][4]} | {a[i][0][5]}".upper())

    def calFines(self):
        try:
            if len(self.barrowedBooks_User) > 0:
                for i in range(len(self.barrowedBooks_User)):
                    datei = self.barrowedBooks_User[i][1]
                    print(datei)
                    day = int(datei[0:2])
                    month = int(datei[3:5])
                    yr = int(datei[-4:])

                    dateee = date(yr, month, day)
                    if dateee < self.today:
                        fine = 10
                        self.barrowedBooks_User[i][3] = fine
                        fine = 0

                print(self.barrowedBooks_User)
                tFine = 0
                for i in range(len(self.barrowedBooks_User)):
                    f = self.barrowedBooks_User[i][3]
                    tFine += f
                self.tf = tFine
                self.labelFine.setText(f"P {tFine}.00")
        except Exception as e:
            print(e)

    def returnBook(self):
        try:
            self.dateBarrowed.clear()
            self.fineAmount.setText("0")
            self.labelINFO_return.setText(
                "Subject:\nTitle:\nAuthor:\nDate:\nRack No.:\nCopies:")
            del self.barrowedBooks_User[self.selectedBookIDX]
            del self.strings[self.selectedBookIDX]
            self.displayBarrowedBooks()
        except Exception as e:
            print(e)

    def logout(self):
        try:
            if self.tf > 0:
                self.msg.setText('Pay your balances in liabilities before leaving')
                self.msg.exec_()
            else:
                self.loginFrame.show()
                self.homeFrame.hide()
                self.barrowFrame.hide()
                self.returnFrame.hide()
                self.reservedFrame.hide()
                self.username.clear()
                self.password.clear()
                self.labelWrongCredential.hide()

        except Exception as e:
            print(e)

    def pay(self):
        try:
            print(type(self.money.text()))
            money = self.money.text()
            money = int(money)
            print(self.tf)
            if int(self.money.text()) < self.tf:
                self.msg.setText("Your money is not enough")
                self.msg.exec_()
                self.money.clear()
            else:
                self.money.clear()
                change = money - self.tf
                self.change.setPlaceholderText(f"P {change}.00")
                self.labelFine.setText(f"P 0.00")
                self.tf = 0
                for i in range(len(self.barrowedBooks_User)):
                    self.barrowedBooks_User[i][3] = 0
                print(self.barrowedBooks_User)
        except Exception as e:
            print(e)


    def reserved(self):
        self.bookList_reserved.clear()
        self.reservedBooks.append(self.selectedBook)
        a = self.reservedBooks
        for i in range(len(a)):
            self.bookList_reserved.addItem(f"{a[i][2]} | {a[i][3]} | {a[i][4]} | {a[i][5]}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    iWindow = Ui_MainWindow()
    iWindow.show()
    # iWindow.showMaximized()
    sys.exit(app.exec_())
