#Nur Shafa Erinda / 12220150 / UAS

#import data dan modul yang diperlukan
import pandas as pd
import matplotlib.pyplot as plt
import json
import streamlit as st

df = pd.read_csv("D:/0 Sekolah/0 Kuliah/Semester 3/Pemkom/UAS/produksi_minyak_mentah.csv")
with open("D:/0 Sekolah/0 Kuliah/Semester 3/Pemkom/UAS/kode_negara_lengkap.json") as f:
    datauas = json.load(f)

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
st.set_page_config(layout="wide")
st.title("Statistik Produksi Minyak Mentah")
st.markdown("*Dibuat oleh Nur Shafa Erinda (12220150*")

#------------------------------------SIDE BAR------------------------------------#
st.sidebar.title("Main Menu")
st.sidebar.markdown("Pilih salah satu menu berikut:  ")

list_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
bulan = st.sidebar.selectbox("Pilih bulan", list_bulan)
list_userchoice = ['Gratik jumlah produksi minyak mentah terhadap waktu suatu negara', 'Grafik negara dengan produksi terbesar pada suatu tahun', 'Grafik negara dengan produksi kumulatif terbesar', 'Summary produksi minyak mentah']
userchoice = st.radio("Menu: ", list_userchoice)
if userchoice == list_userchoice[0]:
    userchoice = 1
elif userchoice == list_userchoice[1]:
    userchoice = 2
elif userchoice == list_userchoice[2]:
    userchoice = 3
elif userchoice == list_userchoice[3]:
    userchoice = 4

#SOAL A, B, C, D
if userchoice==1 : #SOAL A
    #input nama negara
    inputnegara1 = input('Masukkan nama negara: ')
    inputnegara1 = inputnegara1.title()

    #cari nama negara tersebut di data
    dictionarynegara1 = (next(x for x in datauas if x["name"] == inputnegara1))
    codenegara1 = dictionarynegara1['alpha-3']

    #dari kode negara, bikin data frame tersendiri khusus negara itu
    kumpulandata1 = df.loc[df["kode_negara"] == codenegara1]

    #buat grafiknya
    kumpulandata1.plot(kind="line", x="tahun", y="produksi", title="Grafik Produksi Minyak", xlabel="tahun", ylabel='jumlah produksi')
    plt.show()

elif userchoice==2 : #SOAL B
    #input B,T
    inputtahun2 = input('Masukkan tahun: ')
    inputtahun2 = int(inputtahun2)
    inputbesar2 = input('Jumlah negara yang ditampilkan: ')
    inputbesar2 = int(inputbesar2)

    #dari tahun produksi yang diinput, bikin data frame tersendiri khusus tahun itu
    kumpulandata2 = df.loc[df["tahun"] == inputtahun2]
    kumpulandata22 = (kumpulandata2.sort_values(["produksi"], ascending=False).head(inputbesar2))

    #print dataframe yang telah dibuat dan plotnya
    print(kumpulandata22)
    kumpulandata22.plot(kind="bar", x="kode_negara", y="produksi", title="Grafik Produksi Minyak Terbesar Pada Tahun Input User", xlabel="tahun", ylabel='jumlah produksi')
    plt.show()

elif userchoice == 3 : #SOAL C
    #input user
    inputbesar3 = input('Jumlah negara yang ditampilkan: ')
    inputbesar3 = int(inputbesar3)

    #buat dataframe sesuai keperluan
    kumpulandata3 = df.groupby("kode_negara")["produksi"].sum().to_frame(name = 'produksi_kumulatif').reset_index()
    kumpulandata33 = kumpulandata3.sort_values(["produksi_kumulatif"], ascending=False).head(inputbesar3)

    #print dataframe yang sudah dibuat dan plotnya
    print(kumpulandata33)
    kumpulandata33.plot(kind="bar", x="kode_negara", y="produksi_kumulatif", title="Grafik Produksi Minyak Kumulatif Terbesar", xlabel="tahun", ylabel='jumlah produksi')
    plt.show()

elif userchoice == 4 : #SOAL D
    #input T
    inputtahun4 = input('Masukkan tahun: ')
    inputtahun4 = int(inputtahun4)

    #-----------------------------------tabel 1-----------------------------------
    #~~~~~kumulatif~~~~~
    kumpulandatad1 = df.groupby("kode_negara")["produksi"].sum().to_frame(name='produksi_kumulatif').reset_index()
    imax1 = kumpulandatad1["produksi_kumulatif"].idxmax()
    imax1 = int(imax1)

    print("Kode negara dengan produksi minyak kumulatif terbesar : ", kumpulandatad1.loc[imax1,"kode_negara"])
    print("Jumlah produksi : ", kumpulandatad1.loc[imax1, "produksi_kumulatif"])

    dictionarynegarad1 = (next(x for x in datauas if x["alpha-3"] == kumpulandatad1.loc[imax1,"kode_negara"]))
    namanegarad1 = dictionarynegarad1['name']
    namaregiond1 = dictionarynegarad1['region']
    namasubregiond1 = dictionarynegarad1['sub-region']

    print("Nama negara : ", namanegarad1)
    print("Region : ", namaregiond1)
    print("Sub-Region : ", namasubregiond1)
    print("   ")

    #~~~~~tahun T~~~~~
    kumpulandatad1t = df.loc[df["tahun"] == inputtahun4]
    imax2 = kumpulandatad1t["produksi"].idxmax()
    imax2 = int(imax2)

    print("Kode negara dengan produksi minyak pada tahun ", inputtahun4 ," terbesar : ", kumpulandatad1t.loc[imax2, "kode_negara"])
    print("Jumlah produksi : ", kumpulandatad1t.loc[imax2, "produksi"])

    dictionarynegarad1t = (next(x for x in datauas if x["alpha-3"] == kumpulandatad1t.loc[imax2, "kode_negara"]))
    namanegarad1t = dictionarynegarad1t['name']
    namaregiond1t = dictionarynegarad1t['region']
    namasubregiond1t = dictionarynegarad1t['sub-region']

    print("Nama negara : ", namanegarad1t)
    print("Region : ", namaregiond1t)
    print("Sub-Region : ", namasubregiond1t)
    print("   ")

    #-----------------------------------tabel 2-----------------------------------
    #~~~~~kumulatif~~~~~
    #menghilangkan yang value-nya 0 terlebih dahulu
    kumpulandatad2 = kumpulandatad1[kumpulandatad1.produksi_kumulatif != 0]

    imin1 = kumpulandatad2["produksi_kumulatif"].idxmin()
    imin1 = int(imin1)

    print("Kode negara dengan produksi minyak kumulatif terkecil : ", kumpulandatad2.loc[imin1, "kode_negara"])
    print("Jumlah produksi : ", kumpulandatad2.loc[imin1, "produksi_kumulatif"])

    dictionarynegarad2 = (next(x for x in datauas if x["alpha-3"] == kumpulandatad2.loc[imin1, "kode_negara"]))
    namanegarad2 = dictionarynegarad2['name']
    namaregiond2 = dictionarynegarad2['region']
    namasubregiond2 = dictionarynegarad2['sub-region']

    print("Nama negara : ", namanegarad2)
    print("Region : ", namaregiond2)
    print("Sub-Region : ", namasubregiond2)
    print("   ")

    #~~~~~tahun T~~~~~
    #menghilangkan yang value-nya 0 terlebih dahulu
    kumpulandatad2t = kumpulandatad1t[kumpulandatad1t.produksi != 0]
    imin2 = kumpulandatad2t["produksi"].idxmin()
    imin2 = int(imin2)

    print("Kode negara dengan produksi minyak pada tahun ", inputtahun4, " terkecil : ",
          kumpulandatad2t.loc[imin2, "kode_negara"])
    print("Jumlah produksi : ", kumpulandatad2t.loc[imin2, "produksi"])

    dictionarynegarad2t = (next(x for x in datauas if x["alpha-3"] == kumpulandatad2t.loc[imin2, "kode_negara"]))
    namanegarad2t = dictionarynegarad2t['name']
    namaregiond2t = dictionarynegarad2t['region']
    namasubregiond2t = dictionarynegarad2t['sub-region']

    print("Nama negara : ", namanegarad2t)
    print("Region : ", namaregiond2t)
    print("Sub-Region : ", namasubregiond2t)
    print("   ")

    #-----------------------------------tabel 3-----------------------------------
    #~~~~~kumulatif~~~~~
    #membuat data frame berisi data yang hanya berisikan produksi kumulatif 0
    print("Data produksi minyak kumulatif berjumlah 0:")
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
    print(kumpulandatad3)

    #~~~~~tahun T~~~~~
    #membuat data frame berisi data yang hanya berisikan produksi 0 di tahun T
    print("Data produksi minyak pada tahun ", inputtahun4 , " berjumlah 0:")
    kumpulandatad3t = kumpulandatad1t[kumpulandatad1t.produksi == 0]

    #membuat list untuk kolom nama asli negara, region, dan sub-region
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
    print(kumpulandatad3t)