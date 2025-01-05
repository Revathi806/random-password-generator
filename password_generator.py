from PyQt5.QtWidgets import QApplication,QMainWindow,QLabel,QPushButton,QWidget,QVBoxLayout,QStackedWidget,QLineEdit,QRadioButton,QButtonGroup,QMessageBox,QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QFont
import sys
import random
import string

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PASSWORD GENERATOR")
        self.setGeometry(0,0,500,500)
        self.initUI()
        

    def initUI(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.pwdpage = QWidget()
        self.pwdlayout=QVBoxLayout()
        self.pwdpage.setLayout(self.pwdlayout)

        
        self.length=QLineEdit(self)
        self.letterA=QLineEdit(self)
        self.lettera=QLineEdit(self)
        self.number=QLineEdit(self)
        self.special=QLineEdit(self)
        self.avoid=QLineEdit(self)
        enter_length=QLabel("ENTER LENGTH:",self)
        enter_lettersA=QLabel("HOW MANY UPPERCASE LETTERS:",self)
        enter_lettersa=QLabel("HOW MANY LOWERCASE LETTERS:",self)
        enter_numbers=QLabel("HOW MANY DIGITS:",self)
        enter_special=QLabel("HOW MANY SPECIAL CHARACTERS:",self)
        enter_avoid=QLabel("ENTER ANY CHARACTERS YOU WANT TO AVOID: ",self)
        enter_length.setFont(QFont("Arial",20))
        enter_lettersA.setFont(QFont("Arial",20))
        enter_lettersa.setFont(QFont("Arial",20))
        enter_numbers.setFont(QFont("Arial",20))
        enter_special.setFont(QFont("Arial",20))
        enter_avoid.setFont(QFont("Arial",20))

        generate = QPushButton("Generate Password", self)
        generate.setFont(QFont("Arial", 20))
        generate.clicked.connect(self.on_generate)

        self.copy = QPushButton("Copy", self)
        self.copy.setFont(QFont("Arial", 20))
        self.copy.clicked.connect(self.copy_to_clipboard)
        self.copy.setEnabled(False)

        self.pwdlayout.addWidget(enter_length)
        self.pwdlayout.addWidget(self.length)
        self.pwdlayout.addWidget(enter_lettersA)
        self.pwdlayout.addWidget(self.letterA)
        self.pwdlayout.addWidget(enter_lettersa)
        self.pwdlayout.addWidget(self.lettera)
        self.pwdlayout.addWidget(enter_numbers)
        self.pwdlayout.addWidget(self.number)
        self.pwdlayout.addWidget(enter_special)
        self.pwdlayout.addWidget(self.special)
        self.pwdlayout.addWidget(enter_avoid)
        self.pwdlayout.addWidget(self.avoid)
        self.pwdlayout.addWidget(generate)

        self.result_label = QLabel("", self)
        self.result_label.setFont(QFont("Arial", 20))
        self.pwdlayout.addWidget(self.result_label)

        self.pwdlayout.addWidget(self.copy)

        self.stacked_widget.addWidget(self.pwdpage)
    def on_generate(self):
        self.result_label.setText("")
        self.copy.setEnabled(False)
        try:
            length = int(self.length.text())
            letterA = int(self.letterA.text())
            lettera = int(self.lettera.text())
            number = int(self.number.text())
            special = int(self.special.text())
            avoid = self.avoid.text() 
            if length <0 or letterA<0 or lettera<0 or number<0 or special<0:
                raise ValueError("All values must be non-negative.")

            self.generatePwd(length, letterA, lettera, number, special,avoid)
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))


    def generatePwd(self, length, letterA, lettera, number, special,avoid):
        sum=letterA+lettera+number+special
        if sum>length:
            QMessageBox.warning(self, "Input Error", "The total number of characters exceeds the specified length.")
            return
        else:
            password_characters = []
            uppercase_letters = string.ascii_uppercase
            lowercase_letters = string.ascii_lowercase
            digits = string.digits 
            special_characters = string.punctuation
            if avoid:
                for char in avoid:
                    uppercase_letters = uppercase_letters.replace(char,'')
                    lowercase_letters = lowercase_letters.replace(char,'')
                    digits = digits.replace(char,'')
                    special_characters = special_characters.replace(char,'')

            if letterA > 0:
                password_characters.extend(random.choice(uppercase_letters) for _ in range(letterA))

            if lettera > 0:  
                password_characters.extend(random.choice(lowercase_letters) for _ in range(lettera))

            if number > 0:
                password_characters.extend(random.choice(digits) for _ in range(number))

            if special > 0:
                password_characters.extend(random.choice(special_characters) for _ in range(special))

            if len(password_characters) < length:
                all_characters = uppercase_letters + len(lowercase_letters) + digits + special_characters
                password_characters.extend(random.choice(all_characters) for _ in range(length - len(password_characters)))

            random.shuffle(password_characters)
            password = ''.join(password_characters)
            self.result_label.setText(password)
            self.copy.setEnabled(True)

    def copy_to_clipboard(self):
        clipboard=QApplication.clipboard()
        clipboard.setText(self.result_label.text())
        
def main():
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__=="__main__":
    main()