from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, json, requests
from datetime import datetime
import mysql.connector
# python -m PyQt5.uic.pyuic -x untitled.ui -o a.py 
mydb = mysql.connector.connect(
        host ="127.0.0.1",
        user="root",
        password="123456",
        database="mydatabase"
)

mycursor = mydb.cursor()

today = datetime.now()

number_of_years = 2
# How much year we display, including current one
başlıklar = ["Dep_Airport", "Dep_City", "Dep_Country", "Arr_Airport", "Arr_City", "Arr_Country", "Dep_Date", "Dep_Time", "Arr_Date", "Arr_Time", "Price", "Currency"]

months = {
    1:31, # Ocak
    2:28, # Şubat
    3:31, # Mart
    4:30, # Nisan
    5:31, # Mayıs
    6:30, # Haziran
    7:31, # Temmuz
    8:31, # Ağustos
    9:30, # Eylül
    10:31, # Ekim
    11:30, # Kasım
    12:31 # Aralık
}

dumb = requests.get("https://api.exchangerate.host/latest?base=TRY&symbols=EUR,CHF,CZK,DKK,GBP,HUF,MAD,NOK,PLN,SEK,TRY")
dumb = json.loads(dumb.text)
dumb = dumb["rates"]

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
        self.model_baslangic = QStandardItemModel()
        self.model_bitis = QStandardItemModel()
        Dialog.setObjectName("Ucuz Uçuş Bul")
        Dialog.resize(683, 515)

        self.pushButton = QPushButton(Dialog)
        self.pushButton.setGeometry(QRect(572, 90, 81, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.btnstate)

        # Baslangic Kısmı

        self.initial_day = QComboBox(Dialog)
        self.initial_day.setGeometry(QRect(20, 50, 45, 31))
        font = QFont()
        font.setPointSize(8)
        self.initial_day.setFont(font)
        self.initial_day.setObjectName("initial_day")
        self.initial_day.setModel(self.model_baslangic)

        #------------------------------------------------------------------

        self.initial_month = QComboBox(Dialog)
        self.initial_month.setGeometry(QRect(70, 50, 45, 31))
        font = QFont()
        font.setPointSize(8)
        self.initial_month.setFont(font)
        self.initial_month.setObjectName("initial_month")
        self.initial_month.setModel(self.model_baslangic)

        #------------------------------------------------------------------

        self.initial_year = QComboBox(Dialog)
        self.initial_year.setGeometry(QRect(120, 50, 73, 31))
        font = QFont()
        font.setPointSize(8)
        self.initial_year.setFont(font)
        self.initial_year.setObjectName("initial_year")
        self.initial_year.setModel(self.model_baslangic)

        #------------------- Açılır kutuların interaktif olması için gereken kod -----------

        self.month_starts_from = 0
        self.days_starts_from = 0

        for j in range(today.year, today.year + number_of_years):
            item = QStandardItem(str(j))
            self.model_baslangic.appendRow(item)

            if( j == today.year):
                self.month_starts_from = today.month
            else:
                self.month_starts_from = 1

            for i in range(self.month_starts_from, len(months)+1):
                k = months[i]
                state = QStandardItem(str(i))
                item.appendRow(state)

                if(i == today.month):
                    self.days_starts_from = today.day
                else:
                    self.days_starts_from = 1
                
                for value in range(self.days_starts_from, k+1):
                    city = QStandardItem(str(value))
                    state.appendRow(city)
                
        self.initial_year.currentIndexChanged.connect(self.from_month_update)
        self.from_month_update(0)
        self.initial_month.currentIndexChanged.connect(self.from_day_update)
        self.from_day_update(0)
        
        self.initial_day.currentIndexChanged.connect(self.update_final)

        #------------------------------------------------------------------

        #Bitis Kısmı
        
        self.Bitis_gun = QComboBox(Dialog)
        self.Bitis_gun.setGeometry(QRect(270, 50, 45, 31))
        font = QFont()
        font.setPointSize(8)
        self.Bitis_gun.setFont(font)
        self.Bitis_gun.setObjectName("Bitis_gun")
        self.Bitis_gun.setModel(self.model_bitis)

        #------------------------------------------------------------------

        self.final_month = QComboBox(Dialog)
        self.final_month.setGeometry(QRect(320, 50, 45, 31))
        font = QFont()
        font.setPointSize(8)
        self.final_month.setFont(font)
        self.final_month.setObjectName("final_month")
        self.final_month.setModel(self.model_bitis)

        #------------------------------------------------------------------

        self.Bitis_yil = QComboBox(Dialog)
        self.Bitis_yil.setGeometry(QRect(370, 50, 73, 31))
        font = QFont()
        font.setPointSize(8)
        self.Bitis_yil.setFont(font)
        self.Bitis_yil.setObjectName("Bitis_yil")
        self.Bitis_yil.setModel(self.model_bitis)

        self.temp_func()
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

        self.dep_countries.currentIndexChanged.connect(self.update_dep_cities)
        self.update_dep_cities(0)

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

        self.arr_countries.currentIndexChanged.connect(self.update_arr_cities)
        self.update_arr_cities(0)

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
        self.label_3.setGeometry(QRect(505, 20, 61, 21))
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

        self.currency_select = QComboBox(Dialog)
        self.currency_select.setGeometry(QRect(580, 50, 61, 22))
        self.currency_select.setObjectName("currency_select")
        for i in range(len(dumb)):
            self.currency_select.addItem("")

        self.budget_box = QLineEdit(Dialog)
        self.budget_box.setGeometry(QRect(490, 50, 81, 31))
        self.budget_box.setObjectName("budget_box")

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def tabloya_veri_ekle(self, eklenecek_liste, currency):

        header_list = ["departure_airport", "departure_city", "departure_country", "arrival_airport", "arrival_city", "arrival_country", "departure_date", "departure_time", "arrival_date", "arrival_time", "price", "currency"]
        _translate = QCoreApplication.translate
        satır_sayısı = len(eklenecek_liste)

        self.tableWidget.setRowCount(satır_sayısı)

        # Tablo hücrelerinin yerleri burada oluşturuluyor

        for j in range(0, satır_sayısı):
            # Satır sayısı kadar döngü çalışır
            for i in range(0, len(header_list)):
                # Sütun sayısı kadar döngü çalışır
                item = QTableWidgetItem()
                self.tableWidget.setItem(j, i, item)

        # Tabloya eleman ekleme işi artık burada

        for j in range(0, satır_sayısı):
            json_var = eklenecek_liste[j]

            # Tablodaki hücrelerin yerleri oluşturuluyor 
            for i in range(len(header_list)):
                item = self.tableWidget.item(j,i)
                item.setText(_translate("Dialog", str(json_var[header_list[i]])))

        #-------------------------------------
            # print(eklenecek_liste[j])
            values = list(eklenecek_liste[j].values())
            keys = list(eklenecek_liste[j].keys())
            # print(values)
            # print(keys)
            x = 0
            for i in range(0, len(header_list)):
                # Tabloya ekleme burada yapılıyor
                
                item = self.tableWidget.item(j, i)

                local_val = header_list[i]

                if(local_val == "price"):
                    orijinal_birim = dumb[eklenecek_liste[j]["currency"]]
                    multiplier = orijinal_birim / dumb[currency] 

                    item.setText(_translate("Dialog", str(
                        round(values[i] * float((1 / multiplier)), 2)
                    )))
                    continue
                if(local_val == "currency"):
                    item.setText(_translate("Dialog", currency))
                    continue

                if(local_val == keys[x]):
                    # print(local_val)
                    item.setText(_translate("Dialog", str(values[i])))
                    # Demektir ki bu bilgiyi başlıkta istemişiz
                    #işlemlerin ardından başlıkta istenen bir sonraki indise geçiş
                    x += 1
                else:
                    # demektir ki bu bilgiyi istemiyoruz
                    continue


    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Sorgula"))

        self.label.setText(_translate("Dialog", "ARALIK BAŞLANGICI"))
    
        self.label_2.setText(_translate("Dialog", "ARALIK BİTİŞİ"))

        for i in range(0, len(başlıklar)):
            item = QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)

        for i in range(0, len(başlıklar)):
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(_translate("Dialog", başlıklar[i]))

        l = list(dumb.keys())
        for i in range(0, len(dumb)):
            self.currency_select.setItemText(i, _translate("Dialog", l[i]))
        self.currency_select.setCurrentIndex(l.index("EUR"))

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

    def key_func(b, a):
        return a["price"]

    def btnstate(self):
        dep_country = self.dep_countries.currentText()
        dep_city = self.dep_cities.currentText()

        arr_country = self.arr_countries.currentText()
        arr_city = self.arr_cities.currentText()

        baslangic_gun = self.initial_day.currentText().zfill(2)
        baslangic_ay = self.initial_month.currentText().zfill(2)
        baslangic_yil = self.initial_year.currentText()

        bitis_gun = self.Bitis_gun.currentText().zfill(2)
        bitis_ay = self.final_month.currentText().zfill(2)
        bitis_yil = self.Bitis_yil.currentText()
        butce = self.budget_box.text()
        currency = self.currency_select.currentText()
        # print(currency)
        
        if(butce == ""):
            butce = 500
        else:
            try:
                butce = int(butce)
            except:
                self.budget_box.setStyleSheet("border: 1px solid red;")
                return 0
            self.budget_box.setStyleSheet("border: 1px solid green;")

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

        raw_all_flights.sort(key=self.key_func)

        if(arr_country == "Hepsi"):
            self.tabloya_veri_ekle(raw_all_flights, currency)
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

            self.tabloya_veri_ekle(all_flights, currency)
    
    def update_final(self):
        self.model_bitis.removeRows(0, self.model_bitis.rowCount())
        year = int(self.initial_year.currentText())
        month = int(self.initial_month.currentText())
        day = int(self.initial_day.currentText())
        for j in range(year, today.year + number_of_years):
            item = QStandardItem(str(j))
            self.model_bitis.appendRow(item)

            if( j <= year):
                month_starts_from = month
            else:
                month_starts_from = 1

            for i in range(month_starts_from, len(months)+1):
                k = months[i]
                state = QStandardItem(str(i))
                item.appendRow(state)

                if(i <= month):
                    if(j <= year):
                        days_starts_from = day
                    else:
                        days_starts_from = 1
                else:
                    days_starts_from = 1
                
                for value in range(days_starts_from, k+1):
                    city = QStandardItem(str(value))
                    state.appendRow(city)

        self.Bitis_yil.currentIndexChanged.connect(self.to_month_update)
        self.to_month_update(0)
        self.final_month.currentIndexChanged.connect(self.to_day_update)
        self.to_day_update(0)

    def update_dep_cities(self, index):
        indx = self.model.index(index, 0, self.dep_countries.rootModelIndex())
        self.dep_cities.setRootModelIndex(indx)
        self.dep_cities.setCurrentIndex(0) 

    def update_arr_cities(self, index):
        indx = self.model.index(index, 0, self.arr_countries.rootModelIndex())
        self.arr_cities.setRootModelIndex(indx)
        self.arr_cities.setCurrentIndex(0)

    def from_day_update(self, index):
        indx = self.model_baslangic.index(index, 0, self.initial_month.rootModelIndex())
        self.initial_day.setRootModelIndex(indx)
        self.initial_day.setCurrentIndex(0)

    def from_month_update(self, index):
        indx = self.model_baslangic.index(index, 0, self.initial_year.rootModelIndex())
        self.initial_month.setRootModelIndex(indx)
        self.initial_month.setCurrentIndex(0)
        
    def to_day_update(self, index):
        indx = self.model_bitis.index(index, 0, self.final_month.rootModelIndex())
        self.Bitis_gun.setRootModelIndex(indx)
        self.Bitis_gun.setCurrentIndex(0)

    def to_month_update(self, index):
        indx = self.model_bitis.index(index, 0, self.Bitis_yil.rootModelIndex())
        self.final_month.setRootModelIndex(indx)
        self.final_month.setCurrentIndex(0)

    def temp_func(self):
        for j in range(today.year, today.year + number_of_years):
            item = QStandardItem(str(j))
            self.model_bitis.appendRow(item)

            if( j == today.year):
                month_starts_from = today.month
            else:
                month_starts_from = 1

            for i in range(month_starts_from, len(months)+1):
                k = months[i]
                state = QStandardItem(str(i))
                item.appendRow(state)

                if(i == today.month):
                    days_starts_from = today.day
                else:
                    days_starts_from = 1
                
                for value in range(days_starts_from, k+1):
                    city = QStandardItem(str(value))
                    state.appendRow(city)

        self.Bitis_yil.currentIndexChanged.connect(self.to_month_update)
        self.to_month_update(0)
        self.final_month.currentIndexChanged.connect(self.to_day_update)
        self.to_day_update(0)
        
        
    
app = QApplication(sys.argv)
Dialog = QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()
sys.exit(app.exec_())
