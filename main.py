import decimal

from flask import Flask , request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

##############DB-Konfiguration###########
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_rechnung'

mysql = MySQL(app)


###########################  INDEX  ################
@app.route('/')
def index():
    return render_template('index.html')



#######################  Kunden #################################
@app.route('/kunde')
def kunde():
    #Verbindung zur Datenbank herstellen
    cursor = mysql.connection.cursor()

    query = '''
            SELECT  tbl_kunden.*,
		            tbl_staaten.*,
                    tbl_rechnung.*
            FROM tbl_kunden
            LEFT JOIN tbl_staaten on tbl_kunden.FID_Staaten = tbl_staaten.ID_Staaten
            LEFT JOIN tbl_rechnung on tbl_kunden.ID_Kunde = tbl_rechnung.FID_Kunde
    '''
    cursor.execute(query)
    kunden = cursor.fetchall()


    abfrage = '''
                SELECT tbl_warenkorb.*,
		tbl_produkte.*,
        tbl_steuersatz.*
        FROM tbl_warenkorb 
        Left JOIN tbl_produkte on tbl_produkte.ID_Produkt = tbl_warenkorb.FID_Produkt
        LEFT JOIN tbl_steuersatz on tbl_steuersatz.ID_Steuersatz = tbl_produkte.FID_Steuersatz
        
    '''

    cursor.execute(abfrage)
    produkte = cursor.fetchall()

    result = []
    for i in produkte:
        a = i[7]
        b = i[1]
        c = i[11]
        preis = (a * b) + c
        results = i + (preis,)
        result.append(results)



    abfrage = '''
                SELECT 	tbl_rechnung.FID_Kunde,
		tbl_zahlungsarten.Bezeichnung,
        tbl_versandarten.Bezeichnung,
        tbl_versandpaket.Preis
        FROM tbl_rechnung
        Left JOIN tbl_zahlungsarten on tbl_zahlungsarten.ID_Zahlungsarten = tbl_rechnung.FID_Zahlungsart
        Left JOIN tbl_versandpaket on tbl_versandpaket.ID_Versandpaket = tbl_rechnung.FID_Versandpaket
        LEFT JOIN tbl_versandarten on tbl_versandpaket.FID_Versandart = tbl_versandarten.ID_Versandarten
        WHERE tbl_rechnung.FID_Kunde = 1
            '''
    cursor.execute(abfrage)
    produkte = cursor.fetchall()
    print(produkte)
    return render_template('kunde.html',kunden=kunden,result=result,produkte=produkte)



if __name__ == '__main__':
    app.run(debug=True)