#Nur Shafa Erinda / 12220150 / UAS

#import data dan modul yang diperlukan
import pandas as pd
import matplotlib.pyplot as plt
import json, requests
import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://i.ibb.co/SNHBPTr/206101.png")
    }
   .sidebar .sidebar-content {
        background: url("https://dyrdkqpaj50j2.cloudfront.net/media/catalog/product/g/s/gsa-101-white_31.jpg")
    }
    </style>
    """,
    unsafe_allow_html=True
)

df = pd.read_csv("https://raw.githubusercontent.com/nurshafa/uaspemkom/main/produksi_minyak_mentah.csv")
url = 'https://raw.githubusercontent.com/nurshafa/uaspemkom/main/kode_negara_lengkap.json'
resp = requests.get(url)
datauas = json.loads(resp.text)

#membuat list yang relevan
listorganisasi = list()
listkodecsv0 = list()
listkodecsv = list()
listkodejson = list()
listkodefix = list()
listtahunfix = list()
listnegarafix = list()

for i in datauas:
    listkodejson.append(i['alpha-3'])

listkodecsv0 = df['kode_negara'].tolist()

for j in listkodecsv0 :
    if j not in listkodecsv :
        listkodecsv.append(j)

for k in listkodecsv :
    if k not in listkodejson :
        listorganisasi.append(k) #list organisasi

for k in listkodecsv :
    if k in listkodejson :
        listkodefix.append(k) #list kode

listkodefix = list(dict.fromkeys(listkodefix))

#Menghapus organisasi pada file csv
for line in listorganisasi :
    df = df[df.kode_negara != line]

#membuat list lainnya yang diperlukan
listtahunfix = df['tahun'].tolist()
listtahunfix = list(dict.fromkeys(listtahunfix))

for line3 in listkodefix:
    dictionarynegarax = next(x for x in datauas if x["alpha-3"] == line3)
    listnegarafix.append(dictionarynegarax['name'])

listnegarafix = list(dict.fromkeys(listnegarafix))

#------------------------------------TITLE-------------------------------------#
st.title("Statistik Produksi Minyak Mentah")
st.markdown("*Dibuat oleh Nur Shafa Erinda (12220150)*")
st.subheader("   ")

#------------------------------------SIDE BAR------------------------------------#
image = Image.open('itb.png')
st.sidebar.image(image, width=150)
st.sidebar.title("Main Menu")
st.sidebar.markdown("Pilih salah satu menu berikut:  ")

list_userchoice = ['Grafik jumlah produksi minyak mentah terhadap waktu suatu negara', 'Grafik negara dengan produksi terbesar pada suatu tahun', 'Grafik negara dengan produksi kumulatif terbesar', 'Summary produksi minyak mentah']
userchoice = st.sidebar.radio('Menu: ',list_userchoice)
if userchoice == list_userchoice[0]:
    userchoice = 1
elif userchoice == list_userchoice[1]:
    userchoice = 2
elif userchoice == list_userchoice[2]:
    userchoice = 3
elif userchoice == list_userchoice[3]:
    userchoice = 4

#---------------------------------MAIN PAGE----------------------------------------#
#SOAL A, B, C, D
if userchoice==1 : #SOAL A
    #input nama negara
    inputnegara1 = st.selectbox("Nama negara", listnegarafix)

    #cari nama negara tersebut di data
    dictionarynegara1 = (next(x for x in datauas if x["name"] == inputnegara1))
    codenegara1 = dictionarynegara1['alpha-3']

    #dari kode negara, bikin data frame tersendiri khusus negara itu
    kumpulandata1 = df.loc[df["kode_negara"] == codenegara1]

    #buat grafiknya
    st.header(f"Produksi Minyak Mentah {inputnegara1}")
    kumpulandata1.plot(kind="line", x="tahun", y="produksi", title="Grafik Produksi Minyak", xlabel="tahun", ylabel='jumlah produksi', color='indigo', marker='o',markerfacecolor='darkorchid', markersize=9)
    a = plt.show()
    plota = st.pyplot(a)

elif userchoice==2 : #SOAL B
    st.markdown("*Disarankan untuk tidak memilih lebih dari 45 besar supaya grafik masih bisa jelas terlihat*")

    #input B,T
    col1, col2 = st.columns(2)
    inputbesar2 = col1.slider('Jumlah negara yang ditampilkan: ', 1, 137)
    inputbesar2 = int(inputbesar2)
    inputtahun2 = col2.selectbox('Tahun: ', listtahunfix)

    st.header(f"Produksi Minyak Mentah Terbesar Tahun {inputtahun2}")
    #dari tahun produksi yang diinput, bikin data frame tersendiri khusus tahun itu
    kumpulandata2 = df.loc[df["tahun"] == inputtahun2]
    kumpulandata22 = (kumpulandata2.sort_values(["produksi"], ascending=False).head(inputbesar2))

    listnegarasoalb = list()
    namanegarasoalb = list()
    listnegarasoalb = kumpulandata22['kode_negara'].tolist()

    for line2 in listnegarasoalb:
        dictionarynegarab = next(x for x in datauas if x["alpha-3"] == line2)
        namanegarasoalb.append(dictionarynegarab['name'])

    kumpulandata22.insert(1, "nama_negara", namanegarasoalb, True)

    #print dataframe yang telah dibuat dan plotnya
    st.subheader("Data")
    st.dataframe(kumpulandata22)
    st.subheader("Grafik")
    kumpulandata22.plot(kind="bar", x="kode_negara", y="produksi", title="Grafik Produksi Minyak Terbesar Pada Tahun Input User", xlabel="negara", ylabel='produksi',color='rebeccapurple')
    b = plt.show()
    plota = st.pyplot(b)

elif userchoice == 3 : #SOAL C
    st.header('Produksi Minyak Mentah Kumulatif Terbesar')
    st.markdown("*Disarankan untuk tidak memilih lebih dari 45 besar supaya grafik masih bisa jelas terlihat*")
    #input user
    inputbesar3 = st.slider('Jumlah negara yang ditampilkan: ', 1, 137)
    inputbesar3 = int(inputbesar3)

    #buat dataframe sesuai keperluan
    kumpulandata3 = df.groupby("kode_negara")["produksi"].sum().to_frame(name = 'produksi_kumulatif').reset_index()
    kumpulandata33 = kumpulandata3.sort_values(["produksi_kumulatif"], ascending=False).head(inputbesar3)

    listnegarasoalc = list()
    namanegarasoalc = list()
    listnegarasoalc = kumpulandata33['kode_negara'].tolist()

    for line2 in listnegarasoalc:
        dictionarynegarac = next(x for x in datauas if x["alpha-3"] == line2)
        namanegarasoalc.append(dictionarynegarac['name'])

    kumpulandata33.insert(1, "nama_negara", namanegarasoalc, True)

    #print dataframe yang sudah dibuat dan plotnya
    st.subheader("Data")
    st.dataframe(kumpulandata33)
    st.subheader("Grafik")
    kumpulandata33.plot(kind="bar", x="kode_negara", y="produksi_kumulatif", title="Grafik Produksi Minyak Kumulatif Terbesar", xlabel="negara", ylabel='produksi kumulatif',color='mediumvioletred')
    c = plt.show()
    plota = st.pyplot(c)

elif userchoice == 4 : #SOAL D
    st.header('Summary Produksi Minyak Mentah')
    #input T
    inputtahun4 = st.selectbox('Tahun: ', listtahunfix)

    #-----------------------------------tabel 1-----------------------------------
    st.subheader("**Produksi Terbesar**")
    col1, col2 = st.columns(2)
    #~~~~~kumulatif~~~~~
    kumpulandatad1 = df.groupby("kode_negara")["produksi"].sum().to_frame(name='produksi_kumulatif').reset_index()
    imax1 = kumpulandatad1["produksi_kumulatif"].idxmax()
    imax1 = int(imax1)
    koded1 = kumpulandatad1.loc[imax1,"kode_negara"]
    prodd1 = kumpulandatad1.loc[imax1, "produksi_kumulatif"]

    col2.markdown(f"**Kode negara (kumulatif)** : {koded1}")
    col2.markdown(f"**Jumlah produksi** : {prodd1}")

    dictionarynegarad1 = (next(x for x in datauas if x["alpha-3"] == kumpulandatad1.loc[imax1,"kode_negara"]))
    namanegarad1 = dictionarynegarad1['name']
    namaregiond1 = dictionarynegarad1['region']
    namasubregiond1 = dictionarynegarad1['sub-region']

    col2.markdown(f"**Nama negara** : {namanegarad1}")
    col2.markdown(f"**Region** : {namaregiond1}")
    col2.markdown(f"**Sub-Region** : {namasubregiond1}")
    col2.markdown("   ")

    #~~~~~tahun T~~~~~
    kumpulandatad1t = df.loc[df["tahun"] == inputtahun4]
    imax2 = kumpulandatad1t["produksi"].idxmax()
    imax2 = int(imax2)
    koded2 = kumpulandatad1t.loc[imax2, "kode_negara"]
    prodd2 = kumpulandatad1t.loc[imax2, "produksi"]

    col1.markdown(f"**Kode negara (tahun {inputtahun4})** : {koded2}")
    col1.markdown(f"**Jumlah produksi** : {prodd2}" )

    dictionarynegarad1t = (next(x for x in datauas if x["alpha-3"] == kumpulandatad1t.loc[imax2, "kode_negara"]))
    namanegarad1t = dictionarynegarad1t['name']
    namaregiond1t = dictionarynegarad1t['region']
    namasubregiond1t = dictionarynegarad1t['sub-region']

    col1.markdown(f"**Nama negara** : {namanegarad1t}")
    col1.markdown(f"**Region** : {namaregiond1t}")
    col1.markdown(f"**Sub-Region** {namasubregiond1t}")
    col1.markdown("   ")

    #-----------------------------------tabel 2-----------------------------------
    st.subheader("**Produksi Terkecil**")
    col1, col2 = st.columns(2)
    #~~~~~kumulatif~~~~~
    #menghilangkan yang value-nya 0 terlebih dahulu
    kumpulandatad2 = kumpulandatad1[kumpulandatad1.produksi_kumulatif != 0]
    imin1 = kumpulandatad2["produksi_kumulatif"].idxmin()
    imin1 = int(imin1)
    koded3 = kumpulandatad2.loc[imin1, "kode_negara"]
    prodd3 = kumpulandatad2.loc[imin1, "produksi_kumulatif"]

    col2.markdown(f"**Kode negara (kumulatif)** : {koded3} " )
    col2.markdown(f"**Jumlah produksi** : {prodd3}")

    dictionarynegarad2 = (next(x for x in datauas if x["alpha-3"] == kumpulandatad2.loc[imin1, "kode_negara"]))
    namanegarad2 = dictionarynegarad2['name']
    namaregiond2 = dictionarynegarad2['region']
    namasubregiond2 = dictionarynegarad2['sub-region']

    col2.markdown(f"**Nama negara** : {namanegarad2}")
    col2.markdown(f"**Region** : {namaregiond2}")
    col2.markdown(f"**Sub-Region** : {namasubregiond2}")
    col2.markdown("   ")

    #~~~~~tahun T~~~~~
    #menghilangkan yang value-nya 0 terlebih dahulu
    kumpulandatad2t = kumpulandatad1t[kumpulandatad1t.produksi != 0]
    imin2 = kumpulandatad2t["produksi"].idxmin()
    imin2 = int(imin2)
    koded4 = kumpulandatad2t.loc[imin2, "kode_negara"]
    prodd4 = kumpulandatad2t.loc[imin2, "produksi"]

    col1.markdown(f"**Kode negara ({inputtahun4}) ** : {koded4}")
    col1.markdown(f"**Jumlah produksi** : {prodd4}")

    dictionarynegarad2t = (next(x for x in datauas if x["alpha-3"] == kumpulandatad2t.loc[imin2, "kode_negara"]))
    namanegarad2t = dictionarynegarad2t['name']
    namaregiond2t = dictionarynegarad2t['region']
    namasubregiond2t = dictionarynegarad2t['sub-region']

    col1.markdown(f"**Nama negara** {namanegarad2t}")
    col1.markdown(f"**Region** : {namaregiond2t}")
    col1.markdown(f"**Sub-Region** : {namasubregiond2t}")
    col1.markdown("   ")

    #-----------------------------------tabel 3-----------------------------------
    st.subheader("**Negara yang Tidak Melakukan Produksi Minyak**")
    #~~~~~tahun T~~~~~
    # membuat data frame berisi data yang hanya berisikan produksi 0 di tahun T
    st.markdown(f"**Data produksi minyak pada tahun {inputtahun4} berjumlah 0:**")
    kumpulandatad3t = kumpulandatad1t[kumpulandatad1t.produksi == 0]

    # membuat list untuk kolom nama asli negara, region, dan sub-region
    listnegaranolt = list()
    namanegarad3t = list()
    namaregiond3t = list()
    namasubregiond3t = list()
    listnegaranolt = kumpulandatad3t['kode_negara'].tolist()

    for line2 in listnegaranolt:
        dictionarynegarad3t = next(x for x in datauas if x["alpha-3"] == line2)
        namanegarad3t.append(dictionarynegarad3t['name'])
        namaregiond3t.append(dictionarynegarad3t['region'])
        namasubregiond3t.append(dictionarynegarad3t['sub-region'])

    kumpulandatad3t.insert(1, "nama_negara", namanegarad3t, True)
    kumpulandatad3t.insert(4, "region", namaregiond3t, True)
    kumpulandatad3t.insert(5, "sub-region", namasubregiond3t, True)
    kumpulandatad3t.drop(columns="produksi",inplace=True)
    st.dataframe(kumpulandatad3t)

    #~~~~~kumulatif~~~~~
    #membuat data frame berisi data yang hanya berisikan produksi kumulatif 0
    st.markdown("**Data produksi minyak kumulatif berjumlah 0**:")
    kumpulandatad3 = kumpulandatad1[kumpulandatad1.produksi_kumulatif == 0]

    #membuat list untuk kolom nama asli negara, region, dan sub-region
    listnegaranol = list()
    namanegarad3 = list()
    namaregiond3 = list()
    namasubregiond3 = list()
    listnegaranol = kumpulandatad3['kode_negara'].tolist()

    for line in listnegaranol :
        dictionarynegarad3 = next(x for x in datauas if x["alpha-3"] == line)
        namanegarad3.append(dictionarynegarad3['name'])
        namaregiond3.append(dictionarynegarad3['region'])
        namasubregiond3.append(dictionarynegarad3['sub-region'])

    kumpulandatad3.insert(1, "nama_negara", namanegarad3, True)
    kumpulandatad3.insert(3, "region", namaregiond3, True)
    kumpulandatad3.insert(4, "sub-region", namasubregiond3, True)
    kumpulandatad3.drop(columns="produksi_kumulatif",inplace=True)
    st.dataframe(kumpulandatad3)