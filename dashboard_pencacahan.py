import pandas as pd
import numpy as np
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

code = '''Persentase diperoleh dari perhitungan Total Ruta Tercacah dibagi dengan Jumlah Prelist KK Tani Wilkerstat'''

sheet_id = "14W9C-A3m-wfwd2ZwSo9manpB6S-2n0cbSVW8TRqOLUA"
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1460697118")
df['ID SLS'] = df['ID SLS'].astype(str)

@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')
    
def highlight_survived(s):
    if ((s['Jumlah Dokumen L2 PPL ke PML'] > s['Jumlah Dokumen L2 Terpakai']) or (s['Jumlah Dokumen L2 PML ke Koseka'] > s['Jumlah Dokumen L2 Terpakai']) or (s['Jumlah Dokumen L2 PML ke Koseka'] > s['Jumlah Dokumen L2 PPL ke PML']) or (s['Jumlah RTUP Tercacah'] > s['Jumlah Dokumen L2 Terpakai'])):
        return ['background-color: orange']*len(s) 

st.set_page_config(layout = "wide")

def main_page():
    with st.sidebar:
        lstKecamatan = list(df["Nama Kecamatan"].unique())
        lstKecamatan.insert(0, "PILIH KECAMATAN")
                
        FirstFilter = st.selectbox("Nama Kecamatan", lstKecamatan, 0)

        if FirstFilter == "PILIH KECAMATAN":
            print(0)

        if FirstFilter != "PILIH KECAMATAN":
            df2 = df[df["Nama Kecamatan"] == FirstFilter]  

            lstDesa = list(df2["Nama Desa"].unique())
            lstDesa.insert(0, "PILIH DESA")

            SecondFilter = st.selectbox("Nama Desa", lstDesa, 0)

    if FirstFilter == "PILIH KECAMATAN":

        ## Widget 
        col1, col2, col3 = st.columns(3)
        n = len(df)
        p1 = df["Sudah Selesai"].isna().sum()
        p2 = sum(df["Sudah Selesai"] == True)
        p3 = sum(df["Sudah Isi Repo"] == True)
        col1.metric(label = "Persentase SLS/Sub SLS Tercacah", value = f"{round((n - p1)/n * 100, 2)} %")
        col2.metric(label = "Persentase SLS/Sub SLS Selesai", value = f"{round((p2)/n * 100, 2)} %")
        col3.metric(label = "Persentase SLS/Sub SLS Input Repo", value = f"{round((p3)/n * 100, 2)} %")
        style_metric_cards(border_left_color = '#1E1E1E')

        ## Bar Chart
        df_tabel = df.groupby(["Kode Kecamatan", "Nama Kecamatan"])[['Jumlah RTUP Tercacah', 'Jumlah Prelist KK Tani']].agg('sum').reset_index()
        df_tabel["Persentase"] = round(df_tabel["Jumlah RTUP Tercacah"]/df_tabel["Jumlah Prelist KK Tani"] * 100, 2)
        df_tabel2 = pd.DataFrame()
        df_tabel2["Kecamatan"] = df_tabel["Kode Kecamatan"].astype(str) + " - " + df_tabel["Nama Kecamatan"]
        df_tabel2["Persentase"] = df_tabel["Persentase"]
        st.bar_chart(df_tabel2, x = "Kecamatan", y = "Persentase")

        st.code(code, language='python')

        df_show = df[["ID SLS", 'Nama Kecamatan', 'Nama Desa', 'Nama SLS', 'Jumlah RTUP Tercacah', 'Jumlah Prelist KK Tani', 'Jumlah Dokumen L2 Terpakai', 'Jumlah Dokumen L2 PPL ke PML', 'Jumlah Dokumen L2 dari PML ke Koseka', 'Sudah Selesai', 'Sudah Isi Repo']]
        df_show.reset_index(drop=True, inplace=True)
        st.dataframe(df_show.style.apply(highlight_survived, axis=1))

        csv = convert_df(df_show)

        st.download_button(
        "Press to Download",
        csv,
        f"Progres Kabupaten Tabanan.csv",
        "text/csv",
        key='download-csv'
        )
        #df2 = df.groupby(["Kode Kecamatan", "Nama Kecamatan"])['Kondisi Terkini'].apply(lambda x: x.astype(int).sum())
    elif FirstFilter != "PILIH KECAMATAN" and SecondFilter == "PILIH DESA":
        ## Widget 

        df11 = df[df["Nama Kecamatan"] == FirstFilter]
        col1, col2, col3 = st.columns(3)
        n = len(df11)
        p1 = df11["Sudah Selesai"].isna().sum()
        p2 = sum(df11["Sudah Selesai"] == True)
        p3 = sum(df11["Sudah Isi Repo"] == True)
        col1.metric(label = "Persentase SLS/Sub SLS Tercacah", value = f"{round((n - p1)/n * 100, 2)} %")
        col2.metric(label = "Persentase SLS/Sub SLS Selesai", value = f"{round((p2)/n * 100, 2)} %")
        col3.metric(label = "Persentase SLS/Sub SLS Input Repo", value = f"{round((p3)/n * 100, 2)} %")
        style_metric_cards(border_left_color = '#1E1E1E')

        ## Bar Chart
        df_tabel = df11.groupby(["Kode Desa", "Nama Desa"])[['Jumlah RTUP Tercacah', 'Jumlah Prelist KK Tani']].agg('sum').reset_index()
        df_tabel["Persentase"] = round(df_tabel["Jumlah RTUP Tercacah"]/df_tabel["Jumlah Prelist KK Tani"] * 100, 2)
        df_tabel2 = pd.DataFrame()
        df_tabel2["Desa"] = df_tabel["Kode Desa"].astype(str) + " - " + df_tabel["Nama Desa"]
        df_tabel2["Persentase"] = df_tabel["Persentase"]
        st.bar_chart(df_tabel2, x = "Desa", y = "Persentase")

        st.code(code, language='python')
        ## Arus Dokumen
        col1, col2, col3 = st.columns(3)
        col1.metric(label = "Jumlah Dokumen L2", value = sum(df11["Jumlah Dokumen L2 Terpakai"]))
        col2.metric(label = "Jumlah Dokumen L2 dari PPL ke PML", value = sum(df11['Jumlah Dokumen L2 PPL ke PML']))
        col3.metric(label = "Jumlah Dokumen L2 dari PML ke Koseka", value = sum(df11['Jumlah Dokumen L2 dari PML ke Koseka']))
        style_metric_cards(border_left_color = '#1E1E1E')

        df_show = df11[["ID SLS", 'Nama Kecamatan', 'Nama Desa', 'Nama SLS', 'Jumlah RTUP Tercacah', 'Jumlah Prelist KK Tani', 'Jumlah Dokumen L2 Terpakai', 'Jumlah Dokumen L2 PPL ke PML', 'Jumlah Dokumen L2 dari PML ke Koseka', 'Sudah Selesai', 'Sudah Isi Repo']]
        df_show.reset_index(drop=True, inplace=True)
        st.dataframe(df_show.style.apply(highlight_survived, axis=1))
        
        csv = convert_df(df_show)

        st.download_button(
        "Press to Download",
        csv,
        f"{FirstFilter}.csv",
        "text/csv",
        key='download-csv'
        )
        #df2 = df.groupby(["Kode Kecamatan", "Nama Kecamatan"])['Kondisi Terkini'].apply(lambda x: x.astype(int).sum())

    elif FirstFilter != "PILIH KECAMATAN" and SecondFilter != "PILIH DESA":
        ## Widget 

        df21 = df[(df["Nama Kecamatan"] == FirstFilter) & (df["Nama Desa"] == SecondFilter)]
        col1, col2, col3 = st.columns(3)
        n = len(df21)
        p1 = df21["Sudah Selesai"].isna().sum()
        p2 = sum(df21["Sudah Selesai"] == True)
        p3 = sum(df21["Sudah Isi Repo"] == True)
        col1.metric(label = "Persentase SLS/Sub SLS Tercacah", value = f"{round((n - p1)/n * 100, 2)} %")
        col2.metric(label = "Persentase SLS/Sub SLS Selesai", value = f"{round((p2)/n * 100, 2)} %")
        col3.metric(label = "Persentase SLS/Sub SLS Input Repo", value = f"{round((p3)/n * 100, 2)} %")
        style_metric_cards(border_left_color = '#1E1E1E')

        ## Bar Chart
        df_tabel = df21.groupby(["Kode SLS", "Nama SLS"])[['Jumlah RTUP Tercacah', 'Jumlah Prelist KK Tani']].agg('sum').reset_index()
        df_tabel["Persentase"] = round(df_tabel["Jumlah RTUP Tercacah"]/df_tabel["Jumlah Prelist KK Tani"] * 100, 2)
        df_tabel2 = pd.DataFrame()
        df_tabel2["SLS"] = df_tabel["Kode SLS"].astype(str) + " - " + df_tabel["Nama SLS"]
        df_tabel2["Persentase"] = df_tabel["Persentase"]
        st.bar_chart(df_tabel2, x = "SLS", y = "Persentase")
        st.code(code, language='python')
        ## Arus Dokumen
        col1, col2, col3 = st.columns(3)
        col1.metric(label = "Jumlah Dokumen L2", value = sum(df21["Jumlah Dokumen L2 Terpakai"]))
        col2.metric(label = "Jumlah Dokumen L2 dari PPL ke PML", value = sum(df21['Jumlah Dokumen L2 PPL ke PML']))
        col3.metric(label = "Jumlah Dokumen L2 dari PML ke Koseka", value = sum(df21['Jumlah Dokumen L2 dari PML ke Koseka']))
        style_metric_cards(border_left_color = '#1E1E1E')

        df_show = df21[["ID SLS", 'Nama Kecamatan', 'Nama Desa', 'Nama SLS', 'Jumlah RTUP Tercacah', 'Jumlah Prelist KK Tani', 'Jumlah Dokumen L2 Terpakai', 'Jumlah Dokumen L2 PPL ke PML', 'Jumlah Dokumen L2 dari PML ke Koseka', 'Sudah Selesai', 'Sudah Isi Repo']]
        df_show.reset_index(drop=True, inplace=True)
        st.dataframe(df_show.style.apply(highlight_survived, axis=1))

        csv = convert_df(df_show)

        st.download_button(
        "Press to Download",
        csv,
        f"{FirstFilter} - {SecondFilter}.csv",
        "text/csv",
        key='download-csv'
        )

def main2():
    sheet_id = "14W9C-A3m-wfwd2ZwSo9manpB6S-2n0cbSVW8TRqOLUA"
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=769831016")
    df['SOBAT ID'] = df['SOBAT ID'].astype(str)

    lstKoseka = list(df["Nama Koseka"].unique())
    lstKoseka.insert(0, "PILIH KOSEKA")

    PilihKoseka = st.selectbox("Nama Koseka", lstKoseka, 0)

    if (PilihKoseka != "PILIH KOSEKA"):
        df = df[df["Nama Koseka"] == PilihKoseka]
        df.reset_index(drop=True, inplace=True)
        df_show = df[["Nama Koseka", "Nama PPL", "SOBAT ID", "Progres RTUP Juni", "Progres RTUP Juli", "Progres RTUP Kumulatif"]]
        st.dataframe(df_show)

        csv = convert_df(df_show)

        st.download_button(
        "Press to Download",
        csv,
        f"{PilihKoseka} Progres PPL.csv",
        "text/csv",
        key='download-csv'
        )
       
    else:
        df_show = df[["Nama Koseka", "Nama PPL", "SOBAT ID", "Progres RTUP Juni", "Progres RTUP Juli", "Progres RTUP Kumulatif"]]
        st.dataframe(df_show)

        csv = convert_df(df_show)

        st.download_button(
        "Press to Download",
        csv,
        f"Progres PPL.csv",
        "text/csv",
        key='download-csv'
        )

page_names_to_funcs = {
    "Progress Wilayah": main_page,
    "Progress PPL": main2,
}

selected_page = st.sidebar.selectbox("Pilih Dashboard", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
