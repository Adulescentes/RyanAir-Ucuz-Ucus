from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, json, requests
import mysql.connector

mydb = mysql.connector.connect(
        host ="127.0.0.1",
        user="root",
        password="123456",
        database="mydatabase"
)

mycursor = mydb.cursor()

gün_sayısı = 31
ay_sayısı = 12
yıl_sayısı = 2
başlıklar = ["Dep_Airport", "Dep_City", "Dep_Country", "Arr_Airport", "Arr_City", "Arr_Country", "Dep_Date", "Dep_Time", "Arr_Date", "Arr_Time", "Price", "Currency"]

with open("veritabani.json", "r+") as f:
    data = json.loads(f.read())

def sorgula(where_part):
    mycursor.execute(
    "select DISTINCT h.iata"+ " "+
    "FROM mydatabase.havalimanları h, mydatabase.şehirler ş, mydatabase.ülkeler ü"+ " "+
    "where " + where_part)
    return mycursor.fetchall()

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.model = QStandardItemModel()
        Dialog.setObjectName("Ucuz Uçuş Bul")
        Dialog.resize(683, 515)

        self.pushButton = QPushButton(Dialog)
        self.pushButton.setGeometry(QRect(572, 90, 81, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.btnstate)

        # Baslangic Kısmı

        self.Baslangic_gun = QComboBox(Dialog)
        self.Baslangic_gun.setGeometry(QRect(20, 50, 45, 31))
        font = QFont()
        font.setPointSize(8)
        self.Baslangic_gun.setFont(font)
        self.Baslangic_gun.setObjectName("Baslangic_gun")
        for i in range(gün_sayısı):
            self.Baslangic_gun.addItem("")

        #------------------------------------------------------------------

        self.Baslangic_ay = QComboBox(Dialog)
        self.Baslangic_ay.setGeometry(QRect(70, 50, 45, 31))
        font = QFont()
        font.setPointSize(8)
        self.Baslangic_ay.setFont(font)
        self.Baslangic_ay.setObjectName("Baslangic_ay")
        for i in range(ay_sayısı):
            self.Baslangic_ay.addItem("")

        #------------------------------------------------------------------

        self.Baslangic_yil = QComboBox(Dialog)
        self.Baslangic_yil.setGeometry(QRect(120, 50, 73, 31))
        font = QFont()
        font.setPointSize(8)
        self.Baslangic_yil.setFont(font)
        self.Baslangic_yil.setObjectName("Baslangic_yil")
        for i in range(yıl_sayısı):
            self.Baslangic_yil.addItem("")
        
        #Bitis Kısmı
        
        self.Bitis_gun = QComboBox(Dialog)
        self.Bitis_gun.setGeometry(QRect(270, 50, 45, 31))
        font = QFont()
        font.setPointSize(8)
        self.Bitis_gun.setFont(font)
        self.Bitis_gun.setObjectName("Bitis_gun")
        for i in range(gün_sayısı):
            self.Bitis_gun.addItem("")

        #------------------------------------------------------------------

        self.Bitis_ay = QComboBox(Dialog)
        self.Bitis_ay.setGeometry(QRect(320, 50, 45, 31))
        font = QFont()
        font.setPointSize(8)
        self.Bitis_ay.setFont(font)
        self.Bitis_ay.setObjectName("Bitis_ay")
        for i in range(ay_sayısı):
            self.Bitis_ay.addItem("")

        #------------------------------------------------------------------

        self.Bitis_yil = QComboBox(Dialog)
        self.Bitis_yil.setGeometry(QRect(370, 50, 73, 31))
        font = QFont()
        font.setPointSize(8)
        self.Bitis_yil.setFont(font)
        self.Bitis_yil.setObjectName("Bitis_yil")
        for i in range(yıl_sayısı):
            self.Bitis_yil.addItem("")

        #------------------------------------------------------------------

        self.dep_countries = QComboBox(Dialog)
        self.dep_countries.setGeometry(20, 120, 90, 22)
        font = QFont()
        font.setPointSize(8)
        self.dep_countries.setFont(font)
        self.dep_countries.setObjectName("Ulkeler_combobox")
        self.dep_countries.setModel(self.model)

        self.dep_cities = QComboBox(Dialog)
        self.dep_cities.setGeometry(120, 120, 90, 22)
        self.dep_cities.setFont(font)
        self.dep_cities.setObjectName("Sehirler_combobox")
        self.dep_cities.setModel(self.model)

        self.model.appendRow(QStandardItem("Hepsi"))
        for k in data:
            state = QStandardItem(k)
            self.model.appendRow(state)
            state.appendRow(QStandardItem("Hepsi"))
            for value in data[k]:
                city = QStandardItem(value)
                state.appendRow(city)

        self.dep_countries.currentIndexChanged.connect(self.updateCombo_Dep)
        self.updateCombo_Dep(0)

        #------------------------------------------------------------------

        self.arr_countries = QComboBox(Dialog)
        self.arr_countries.setGeometry(270, 120, 90, 22)
        font = QFont()
        font.setPointSize(8)
        self.arr_countries.setFont(font)
        self.arr_countries.setObjectName("Ulkeler_combobox2")
        self.arr_countries.setModel(self.model)

        self.arr_cities = QComboBox(Dialog)
        self.arr_cities.setGeometry(370, 120, 90, 22)
        self.arr_cities.setFont(font)
        self.arr_cities.setObjectName("Sehirler_combobox2")
        self.arr_cities.setModel(self.model)

        for k in data:
            state = QStandardItem(k)
            self.model.appendRow(state)
            state.appendRow(QStandardItem("Hepsi"))
            for value in data[k]:
                city = QStandardItem(value)
                state.appendRow(city)

        self.arr_countries.currentIndexChanged.connect(self.updateCombo_Arr)
        self.updateCombo_Arr(0)

        #------------------------------------------------------------------
        
        self.label = QLabel(Dialog)
        self.label.setGeometry(QRect(20, 20, 161, 21))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QLabel(Dialog)
        self.label_2.setGeometry(QRect(300, 20, 111, 21))
        font = QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.label_3 = QLabel(Dialog)
        self.label_3.setGeometry(QRect(520, 20, 61, 21))
        font = QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.label_4 = QLabel(Dialog)
        self.label_4.setGeometry(QRect(120, 90, 91, 21))
        self.label_4.setObjectName("label_4")

        self.label_5 = QLabel(Dialog)
        self.label_5.setGeometry(QRect(20, 90, 91, 21))
        self.label_5.setObjectName("label_5")

        self.label_6 = QLabel(Dialog)
        self.label_6.setGeometry(QRect(370, 90, 91, 21))
        self.label_6.setObjectName("label_6")

        self.label_7 = QLabel(Dialog)
        self.label_7.setGeometry(QRect(270, 90, 91, 21))
        self.label_7.setObjectName("label_7")
        
        #------------------------------------------------------------------

        self.tableWidget = QTableWidget(Dialog)
        self.tableWidget.setGeometry(QRect(20, 200, 661, 300))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(len(başlıklar))

        # Kaç Satır olacağı bilgisi buradan düzenleniyor
        # self.tableWidget.setRowCount(satır_sayısı)

        # for i in range(0, len(başlıklar)):
        #     item = QTableWidgetItem()
        #     self.tableWidget.setHorizontalHeaderItem(i, item)

        # # Tablo hücrelerinin yerleri burada oluşturuluyor

        # for j in range(0, satır_sayısı):
        #     for i in range(0, len(başlıklar)):
        #         item = QTableWidgetItem()
        #         self.tableWidget.setItem(j, i, item)

        self.budget_box = QLineEdit(Dialog)
        self.budget_box.setGeometry(QRect(490, 50, 113, 31))
        self.budget_box.setObjectName("budget_box")

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def tabloya_veri_ekle(self, eklenecek_liste):
        _translate = QCoreApplication.translate
        satır_sayısı = len(eklenecek_liste)

        self.tableWidget.setRowCount(satır_sayısı)

        # Tablo hücrelerinin yerleri burada oluşturuluyor

        for j in range(0, satır_sayısı):
            for i in range(0, len(başlıklar)):
                item = QTableWidgetItem()
                self.tableWidget.setItem(j, i, item)

        # Tabloya eleman ekleme işi artık burada


        header_list = ["departure_airport", "departure_city", "departure_country", "arrival_airport", "arrival_city", "arrival_country", "departure_date", "departure_time", "arrival_date", "arrival_time", "price", "currency"]
        for j in range(0, satır_sayısı):
            json_var = eklenecek_liste[j]
            
            for i in range(len(header_list)):
                item = self.tableWidget.item(j,i)
                item.setText(_translate("Dialog", str(json_var[header_list[i]])))

        #-------------------------------------
            g = list(eklenecek_liste[j].values())
            for i in range(0, len(başlıklar)):
                
                item = self.tableWidget.item(j, i)
                item.setText(_translate("Dialog", str(g[i])))

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
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
            item = QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)

        for i in range(0, len(başlıklar)):
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(_translate("Dialog", başlıklar[i]))

        self.label_3.setText(_translate("Dialog", "BÜTÇE"))
        self.label_4.setText(_translate("Dialog", "KALKIŞ ŞEHİR"))
        self.label_5.setText(_translate("Dialog", "KALKIŞ ÜLKE"))
        self.label_6.setText(_translate("Dialog", "VARIŞ ŞEHİR"))
        self.label_7.setText(_translate("Dialog", "VARIŞ ÜLKE"))

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(__sortingEnabled)

    def main_function(v, departure_airport, date_from, date_to, budget):
        url = "https://www.ryanair.com/api/farfnd/3/oneWayFares?&departureAirportIataCode="+str(departure_airport)+"&language=en&limit=16&market=en-gb&offset=0&outboundDepartureDateFrom="+str(date_from)+"&outboundDepartureDateTo="+str(date_to)+"&priceValueTo="+str(budget)
        req = requests.get(url)

        all_results = []

        result = json.loads(req.text)
        result = result["fares"]

        for i in result:
                current_result = {
                        "departure_airport":i["outbound"]["departureAirport"]["iataCode"],
                        "departure_city":i["outbound"]["departureAirport"]["city"]["name"],
                        "departure_country": i["outbound"]["departureAirport"]["countryName"],

                        "arrival_airport":i["outbound"]["arrivalAirport"]["iataCode"],
                        "arrival_city":i["outbound"]["arrivalAirport"]["city"]["name"],
                        "arrival_country":i["outbound"]["arrivalAirport"]["countryName"],

                        "departure_date": i["outbound"]["departureDate"].split("T")[0],
                        "departure_time":i["outbound"]["departureDate"].split("T")[1],

                        "arrival_date":i["outbound"]["arrivalDate"].split("T")[0],
                        "arrival_time":i["outbound"]["arrivalDate"].split("T")[1],

                        "price":i["outbound"]["price"]["value"],
                        "currency": i["outbound"]["price"]["currencyCode"]
                }
                all_results.append(current_result)

        return all_results

    def btnstate(self):
        dep_country = self.dep_countries.currentText()
        dep_city = self.dep_cities.currentText()

        arr_country = self.arr_countries.currentText()
        arr_city = self.arr_cities.currentText()

        baslangic_gun = self.Baslangic_gun.currentText().zfill(2)
        baslangic_ay = self.Baslangic_ay.currentText().zfill(2)
        baslangic_yil = self.Baslangic_yil.currentText()

        bitis_gun = self.Bitis_gun.currentText().zfill(2)
        bitis_ay = self.Bitis_ay.currentText().zfill(2)
        bitis_yil = self.Bitis_yil.currentText()
        butce = self.budget_box.text()
        if(butce == ""):
            butce = 500

        if(dep_country == "Hepsi"):
            veri = sorgula("h.cityName = ş.code and ş.countryCode = ü.countryCode")
        else:
            # Bu noktada bir ülke seçilmiş demektir
            if(dep_city == "Hepsi"):
                veri = sorgula(f"h.cityName = ş.code and ş.countryCode = ü.countryCode and ü.name = '{dep_country}'")
            else:
                veri = sorgula(f"h.cityName = ş.code and ş.countryCode = ü.countryCode and ş.name = '{dep_city}'")


        raw_all_flights = []
        for i in veri:
            a = self.main_function(i[0], f"{baslangic_yil}-{baslangic_ay}-{baslangic_gun}", f"{bitis_yil}-{bitis_ay}-{bitis_gun}", butce)
            raw_all_flights.extend(a)

        if(arr_country == "Hepsi"):
            self.tabloya_veri_ekle(raw_all_flights)
        else:
            all_flights = []
            if(arr_city == "Hepsi"):
                for i in raw_all_flights:
                    if(i["arrival_country"] == arr_country):
                        all_flights.append(i)

            else:
                for i in raw_all_flights:
                    if(i["arrival_city"] == arr_city):
                        all_flights.append(i)

            self.tabloya_veri_ekle(all_flights)
    

    def updateCombo_Dep(self, index):
        indx = self.model.index(index, 0, self.dep_countries.rootModelIndex())
        self.dep_cities.setRootModelIndex(indx)
        self.dep_cities.setCurrentIndex(0) 

    def updateCombo_Arr(self, index):
        indx = self.model.index(index, 0, self.arr_countries.rootModelIndex())
        self.arr_cities.setRootModelIndex(indx)
        self.arr_cities.setCurrentIndex(0) 
    
app = QApplication(sys.argv)
Dialog = QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()
sys.exit(app.exec_())
