from PyQt5 import QtCore, QtGui, QtWidgets
import sys, json

gün_sayısı = 31
ay_sayısı = 12
yıl_sayısı = 2
başlıklar = ["Dep_Airport", "Dep_City", "Dep_Country", "Dep_Code", "Arr_Airport", "Arr_City", "Arr_Country", "Arr_Code", "Dep_Date", "Dep_Time", "Arr_Date", "Arr_Time", "Price", "Currency"]

liste = []

with open("results.json", "r+") as f:
    liste = json.loads(f.read())

satır_sayısı = len(liste)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(683, 515)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(572, 90, 81, 28))
        self.pushButton.setObjectName("pushButton")

        # Baslangic Kısmı

        self.Baslangic_gun = QtWidgets.QComboBox(Dialog)
        self.Baslangic_gun.setGeometry(QtCore.QRect(20, 50, 45, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Baslangic_gun.setFont(font)
        self.Baslangic_gun.setObjectName("Baslangic_gun")
        for i in range(gün_sayısı):
            self.Baslangic_gun.addItem("")

        #------------------------------------------------------------------

        self.Baslangic_ay = QtWidgets.QComboBox(Dialog)
        self.Baslangic_ay.setGeometry(QtCore.QRect(70, 50, 45, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Baslangic_ay.setFont(font)
        self.Baslangic_ay.setObjectName("Baslangic_ay")
        for i in range(ay_sayısı):
            self.Baslangic_ay.addItem("")

        #------------------------------------------------------------------

        self.Baslangic_yil = QtWidgets.QComboBox(Dialog)
        self.Baslangic_yil.setGeometry(QtCore.QRect(120, 50, 73, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Baslangic_yil.setFont(font)
        self.Baslangic_yil.setObjectName("Baslangic_yil")
        for i in range(yıl_sayısı):
            self.Baslangic_yil.addItem("")
        
        #Bitis Kısmı
        
        self.Bitis_gun = QtWidgets.QComboBox(Dialog)
        self.Bitis_gun.setGeometry(QtCore.QRect(270, 50, 45, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Bitis_gun.setFont(font)
        self.Bitis_gun.setObjectName("Bitis_gun")
        for i in range(gün_sayısı):
            self.Bitis_gun.addItem("")

        #------------------------------------------------------------------

        self.Bitis_ay = QtWidgets.QComboBox(Dialog)
        self.Bitis_ay.setGeometry(QtCore.QRect(320, 50, 45, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Bitis_ay.setFont(font)
        self.Bitis_ay.setObjectName("Bitis_ay")
        for i in range(ay_sayısı):
            self.Bitis_ay.addItem("")

        #------------------------------------------------------------------

        self.Bitis_yil = QtWidgets.QComboBox(Dialog)
        self.Bitis_yil.setGeometry(QtCore.QRect(370, 50, 73, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Bitis_yil.setFont(font)
        self.Bitis_yil.setObjectName("Bitis_yil")
        for i in range(yıl_sayısı):
            self.Bitis_yil.addItem("")
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(300, 20, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(520, 20, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        
        #------------------------------------------------------------------

        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 200, 661, 300))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(len(başlıklar))

        # Kaç Satır olacağı bilgisi buradan düzenleniyor
        self.tableWidget.setRowCount(satır_sayısı)

        for i in range(0, len(başlıklar)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)


        # Tablo hücrelerinin yerleri burada oluşturuluyor

        for j in range(0, satır_sayısı):
            for i in range(0, len(başlıklar)):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(j, i, item)


        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(490, 50, 113, 31))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Sorgula"))

        self.label.setText(_translate("Dialog", "ARALIK BAŞLANGICI"))

        for i in range(0, gün_sayısı):
            self.Baslangic_gun.setItemText(i, _translate("Dialog", str(i+1)))

        for i in range(0, ay_sayısı):
            self.Baslangic_ay.setItemText(i, _translate("Dialog", str(i+1)))

        for i in range(0, yıl_sayısı):
            self.Baslangic_yil.setItemText(i, _translate("Dialog", str(2022+i)))
    
        self.label_2.setText(_translate("Dialog", "ARALIK BİTİŞİ"))
        
        for i in range(0, gün_sayısı):
            self.Bitis_gun.setItemText(i, _translate("Dialog", str(i+1)))

        for i in range(0, ay_sayısı):
            self.Bitis_ay.setItemText(i, _translate("Dialog", str(i+1)))

        for i in range(0, yıl_sayısı):
            self.Bitis_yil.setItemText(i, _translate("Dialog", str(2022+i)))


        for i in range(0, len(başlıklar)):
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(_translate("Dialog", başlıklar[i]))

        self.label_3.setText(_translate("Dialog", "BÜTÇE"))


        # Tabloya eleman ekleme işi artık burada

        for j in range(0, satır_sayısı):

            g = list(liste[j].values())


            for i in range(0, len(başlıklar)):
                item = self.tableWidget.item(j, i)
                item.setText(_translate("Dialog", str(g[i])))

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(__sortingEnabled)


app = QtWidgets.QApplication(sys.argv)
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()
sys.exit(app.exec_())
