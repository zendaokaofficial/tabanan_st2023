from logging import PlaceHolder
import streamlit as st
import pandas as pd
from datetime import date
import webbrowser

sheet_url = "https://docs.google.com/spreadsheets/d/13BbpP9ox-XCo3xB74eTTG0oFoI_aIt6w_BP-4hU3Sjg/edit#gid=0"
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

df = pd.read_csv(url_1, header=0, )

if __name__ == "__main__":
    st.markdown("<h1 style='text-align: center; color: green;'>Isikan Form Pelaporan</h1>", unsafe_allow_html=True)

    st.markdown(f"<h3 style='text-align: center; color: green;'>Tanggal: {date.today()}</h3>", unsafe_allow_html=True)

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

                #df4 = df3[df3["Nama SLS" == ThirdFilter]]

                #lstPPL = ["PILIH NAMA PPL"]

                #ForthFilter = st.selectbox("Nama PPL", lstPPL)

                JumlahRuta = st.text_input('Jumlah Ruta', )

                JumlahL2 = st.text_input('Jumlah Dokumen L2', )

                JumlahL2kePML = st.text_input('Jumlah Dokumen L2 ke PML', )

                JumlahL2keKoseka = st.text_input('Jumlah Dokumen L2 ke Koseka', )

                SudahSelesai = st.selectbox("Apakah Sudah Selesai", ["PILIH", "Sudah", "Belum"], 0)

                SudahIsiRepo = st.selectbox("Apakah Sudah Isi Repo", ["PILIH", "Sudah", "Belum"], 0)

                if (len(JumlahRuta) != 0 and len(JumlahL2) != 0 and len(JumlahL2kePML) != 0 and len(JumlahL2keKoseka) != 0 and SudahSelesai != "PILIH" and SudahIsiRepo != "PILIH"):
                    if st.button('Submit'):
                        st.success(f'Kecamatan : {FirstFilter}, Desa : {len(JumlahRuta)}', icon="✅")
                        st_javascript(f'window.open("{"https://laporst2023-tabanan.streamlit.app/"}", "_blank");')
