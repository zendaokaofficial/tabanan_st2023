import streamlit as st
import pandas as pd
from datetime import date
import time
from streamlit_js_eval import streamlit_js_eval
import gspread
import streamlit as st
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from gsheetsdb import connect
import datetime
import json
import pytz

tzInfo = pytz.timezone('Asia/Bangkok')
# Create a connection object.
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('st2023-tabanan-5595d78f9fe7.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("db ST2023")
worksheet1 = sheet.worksheet('Sheet1')

## Membaca db asal
sheet_url = "https://docs.google.com/spreadsheets/d/13BbpP9ox-XCo3xB74eTTG0oFoI_aIt6w_BP-4hU3Sjg/edit#gid=0"
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

df = pd.read_csv(url_1, header=0, )
hari = date.today()

if __name__ == "__main__":
    st.markdown("<h1 style='text-align: center; color: green;'>Isikan Form Pelaporan</h1>", unsafe_allow_html=True)
    st.subheader(f"Tanggal: {hari}")

    lstKecamatan = list(df["Nama Kecamatan"].unique())
    lstKecamatan.insert(0, "PILIH KECAMATAN")
              
    FirstFilter = st.selectbox("Nama Kecamatan", lstKecamatan, 0)

    if FirstFilter != 'PILIH KECAMATAN':

        df2 = df[df["Nama Kecamatan"] == FirstFilter]  

        lstDesa = list(df2["Nama Desa"].unique())
        lstDesa.insert(0, "PILIH DESA")

        SecondFilter = st.selectbox("Nama Desa", lstDesa, 0)

        if SecondFilter != 'PILIH DESA':

            df3 = df2[df2["Nama Desa"] == SecondFilter]

            lstSLS = list(df3["Nama SLS"].unique())
            lstSLS.insert(0, "PILIH SLS")

            ThirdFilter = st.selectbox("Nama SLS", lstSLS, 0)

            if ThirdFilter != "PILIH SLS":

                df4 = df3[df3["Nama SLS"] == ThirdFilter]

                lstPPL = list(df4["Nama PPL"].unique())
                lstPPL.insert(0, "PILIH PPL")

                ForthFilter = st.selectbox("Nama PPL", lstPPL)

                if ForthFilter != "PILIH PPL":

                    JumlahRuta = st.text_input('Jumlah Ruta', )

                    JumlahL2 = st.text_input('Jumlah Dokumen L2', )

                    JumlahL2kePML = st.text_input('Jumlah Dokumen L2 ke PML', )

                    JumlahL2keKoseka = st.text_input('Jumlah Dokumen L2 ke Koseka', )

                    SudahSelesai = st.selectbox("Apakah Sudah Selesai", ["PILIH", "Sudah", "Belum"], 0)

                    SudahIsiRepo == ""

                    if (SudahSelesai == "Sudah"):
                        SudahIsiRepo = st.selectbox("Apakah Sudah Isi Repo", ["PILIH", "Sudah", "Belum"], 0)
                        if (len(JumlahRuta) != 0 and len(JumlahL2) != 0 and len(JumlahL2kePML) != 0 and len(JumlahL2keKoseka) != 0 and SudahSelesai != "PILIH" and SudahIsiRepo != "PILIH"):
                                 if st.button('Submit', "https://laporst2023-tabanan.streamlit.app/"):
                                     st.success(f'Data berhasil tersubmit', icon="✅")
                                     worksheet1.append_row([datetime.datetime.now(tz=tzInfo).isoformat(), FirstFilter, SecondFilter, ThirdFilter, ForthFilter, JumlahRuta, JumlahL2, JumlahL2kePML, JumlahL2keKoseka, SudahSelesai, SudahIsiRepo])
                                     time.sleep(3)
                                     streamlit_js_eval(js_expressions="parent.window.location.reload()")
                                     #st.markdown(f'window.open("{"https://laporst2023-tabanan.streamlit.app/"}", "_blank");')
                    else:
                         if (len(JumlahRuta) != 0 and len(JumlahL2) != 0 and len(JumlahL2kePML) != 0 and len(JumlahL2keKoseka) != 0 and SudahSelesai != "PILIH"):
                                 if st.button('Submit', "https://laporst2023-tabanan.streamlit.app/"):
                                     st.success(f'Data berhasil tersubmit', icon="✅")
                                     worksheet1.append_row([datetime.datetime.now(tz=tzInfo).isoformat(), FirstFilter, SecondFilter, ThirdFilter, ForthFilter, JumlahRuta, JumlahL2, JumlahL2kePML, JumlahL2keKoseka, SudahSelesai])
                                     time.sleep(3)
                                     streamlit_js_eval(js_expressions="parent.window.location.reload()")
                                     #st.markdown(f'window.open("{"https://laporst2023-tabanan.streamlit.app/"}", "_blank");')
