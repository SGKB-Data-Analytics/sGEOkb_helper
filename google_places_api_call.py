import requests
import time
import pandas as pd
import csv
import proxysetting as ps
import google_key as gk

#google Stuff
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'

path_to_csv = '../ADRESSEN_ENRICHMENT/DATA/BETRIEB/POS_Stand_20211008.csv'
path_to_csv_out = '../ADRESSEN_ENRICHMENT/OUTPUT/resultat_alle_google_abfragen_20220713.csv'  ##############

adressen = pd.read_csv(path_to_csv, header=0, delimiter=";", quoting=csv.QUOTE_NONE, encoding='utf-8' )
#print(adressen)

alle_google_abfragen = []
for index, row in adressen.head(500).iterrows():  ############
    time.sleep(0.1)
    adresse = row['Ort']
    print(adresse)
    params = {    
        'query': adresse, #'BIBIM SHACK, ZUERICH', # row['Adressen'],
        'key': gk.key
        }

    resp = requests.get(GOOGLE_MAPS_API_URL, params=params, verify=False, proxies={"http":str( ps.proxysetting),"https":str( ps.proxysetting)})
  
    #print(resp.status_code)
    if resp.status_code == 200:
        google_abfrage = resp.json()
        df_google_abfrage = pd.json_normalize(google_abfrage['results'])
        df_google_abfrage['original_input'] = adresse

        alle_google_abfragen.append(df_google_abfrage)

alle_google_abfragen = pd.concat(alle_google_abfragen)

alle_google_abfragen.to_csv(path_to_csv_out)


 
