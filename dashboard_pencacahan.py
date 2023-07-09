import pandas as pd
import numpy as np
import streamlit as st
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_extras.metric_cards import style_metric_cards

sheet_id = "14W9C-A3m-wfwd2ZwSo9manpB6S-2n0cbSVW8TRqOLUA"
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1460697118")
df['ID SLS'] = df['ID SLS'].astype(str)

def highlight_survived(s):
    if s["Sudah Selesai"]:
        return ['background-color: green']*len(s) 

st.set_page_config(layout = "wide")

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
    p1 = np.nansum(df["Sudah Selesai"].to_numpy())
    p2 = sum(df["Sudah Selesai"] == True)
    p3 = sum(df["Sudah Isi Repo"] == True)
    col1.metric(label = "Persentase SLS/Sub SLS Tercacah", value = f"{round((n - p1)/n * 100, 2)} %")
    col2.metric(label = "Persentase SLS/Sub SLS Selesai", value = f"{round((p2)/n * 100, 2)} %")
    col3.metric(label = "Persentase SLS/Sub SLS Input Repo", value = f"{round((p3)/n * 100, 2)} %")
    style_metric_cards(border_left_color = '#1E1E1E')

    ## Bar Chart
    df_tabel = df.groupby(["Kode Kecamatan", "Nama Kecamatan"])[['Jumlah Ruta Tercacah', 'Jumlah Prelist KK Tani']].agg('sum').reset_index()
    df_tabel["Persentase"] = round(df_tabel["Jumlah Ruta Tercacah"]/df_tabel["Jumlah Prelist KK Tani"] * 100, 2)
    df_tabel2 = pd.DataFrame()
    df_tabel2["Kecamatan"] = df_tabel["Kode Kecamatan"].astype(str) + " - " + df_tabel["Nama Kecamatan"]
    df_tabel2["Persentase"] = df_tabel["Persentase"]
    st.bar_chart(df_tabel2, x = "Kecamatan", y = "Persentase")

    df_show = df[["ID SLS", 'Nama Kecamatan', 'Nama Desa', 'Nama SLS', 'Jumlah Ruta Tercacah', 'Jumlah Prelist KK Tani', 'Jumlah Dokumen L2 Terpakai', 'Jumlah Dokumen L2 PPL ke PML', 'Jumlah Dokumen L2 dari PML ke Koseka', 'Sudah Selesai', 'Sudah Isi Repo']]
    st.dataframe(df_show)
    #df2 = df.groupby(["Kode Kecamatan", "Nama Kecamatan"])['Kondisi Terkini'].apply(lambda x: x.astype(int).sum())
elif FirstFilter != "PILIH KECAMATAN" and SecondFilter == "PILIH DESA":
    ## Widget 

    df11 = df[df["Nama Kecamatan"] == FirstFilter]
    col1, col2, col3 = st.columns(3)
    n = len(df11)
    p1 = np.nansum(df11["Sudah Selesai"].to_numpy())
    p2 = sum(df11["Sudah Selesai"] == True)
    p3 = sum(df11["Sudah Isi Repo"] == True)
    col1.metric(label = "Persentase SLS/Sub SLS Tercacah", value = f"{round((n - p1)/n * 100, 2)} %")
    col2.metric(label = "Persentase SLS/Sub SLS Selesai", value = f"{round((p2)/n * 100, 2)} %")
    col3.metric(label = "Persentase SLS/Sub SLS Input Repo", value = f"{round((p3)/n * 100, 2)} %")
    style_metric_cards(border_left_color = '#1E1E1E')

    ## Bar Chart
    df_tabel = df11.groupby(["Kode Desa", "Nama Desa"])[['Jumlah Ruta Tercacah', 'Jumlah Prelist KK Tani']].agg('sum').reset_index()
    df_tabel["Persentase"] = round(df_tabel["Jumlah Ruta Tercacah"]/df_tabel["Jumlah Prelist KK Tani"] * 100, 2)
    df_tabel2 = pd.DataFrame()
    df_tabel2["Desa"] = df_tabel["Kode Desa"].astype(str) + " - " + df_tabel["Nama Desa"]
    df_tabel2["Persentase"] = df_tabel["Persentase"]
    st.bar_chart(df_tabel2, x = "Desa", y = "Persentase")

    ## Arus Dokumen
    col1, col2, col3 = st.columns(3)
    col1.metric(label = "Jumlah Dokumen L2", value = sum(df11["Jumlah Dokumen L2 Terpakai"]))
    col2.metric(label = "Jumlah Dokumen L2 dari PPL ke PML", value = sum(df11['Jumlah Dokumen L2 PPL ke PML']))
    col3.metric(label = "Jumlah Dokumen L2 dari PML ke Koseka", value = sum(df11['Jumlah Dokumen L2 dari PML ke Koseka']))
    style_metric_cards(border_left_color = '#1E1E1E')

    df_show = df11[["ID SLS", 'Nama Kecamatan', 'Nama Desa', 'Nama SLS', 'Jumlah Ruta Tercacah', 'Jumlah Prelist KK Tani', 'Jumlah Dokumen L2 Terpakai', 'Jumlah Dokumen L2 PPL ke PML', 'Jumlah Dokumen L2 dari PML ke Koseka', 'Sudah Selesai', 'Sudah Isi Repo']]
    st.dataframe(df_show)
    #df2 = df.groupby(["Kode Kecamatan", "Nama Kecamatan"])['Kondisi Terkini'].apply(lambda x: x.astype(int).sum())

elif FirstFilter != "PILIH KECAMATAN" and SecondFilter != "PILIH DESA":
    ## Widget 

    df21 = df[(df["Nama Kecamatan"] == FirstFilter) & (df["Nama Desa"] == SecondFilter)]
    col1, col2, col3 = st.columns(3)
    n = len(df21)
    p1 = np.nansum(df21["Sudah Selesai"].to_numpy())
    p2 = sum(df21["Sudah Selesai"] == True)
    p3 = sum(df21["Sudah Isi Repo"] == True)
    col1.metric(label = "Persentase SLS/Sub SLS Tercacah", value = f"{round((n - p1)/n * 100, 2)} %")
    col2.metric(label = "Persentase SLS/Sub SLS Selesai", value = f"{round((p2)/n * 100, 2)} %")
    col3.metric(label = "Persentase SLS/Sub SLS Input Repo", value = f"{round((p3)/n * 100, 2)} %")
    style_metric_cards(border_left_color = '#1E1E1E')

    ## Bar Chart
    df_tabel = df21.groupby(["Kode SLS", "Nama SLS"])[['Jumlah Ruta Tercacah', 'Jumlah Prelist KK Tani']].agg('sum').reset_index()
    df_tabel["Persentase"] = round(df_tabel["Jumlah Ruta Tercacah"]/df_tabel["Jumlah Prelist KK Tani"] * 100, 2)
    df_tabel2 = pd.DataFrame()
    df_tabel2["SLS"] = df_tabel["Kode SLS"].astype(str) + " - " + df_tabel["Nama SLS"]
    df_tabel2["Persentase"] = df_tabel["Persentase"]
    st.bar_chart(df_tabel2, x = "SLS", y = "Persentase")

    ## Arus Dokumen
    col1, col2, col3 = st.columns(3)
    col1.metric(label = "Jumlah Dokumen L2", value = sum(df21["Jumlah Dokumen L2 Terpakai"]))
    col2.metric(label = "Jumlah Dokumen L2 dari PPL ke PML", value = sum(df21['Jumlah Dokumen L2 PPL ke PML']))
    col3.metric(label = "Jumlah Dokumen L2 dari PML ke Koseka", value = sum(df21['Jumlah Dokumen L2 dari PML ke Koseka']))
    style_metric_cards(border_left_color = '#1E1E1E')

    df_show = df21[["ID SLS", 'Nama Kecamatan', 'Nama Desa', 'Nama SLS', 'Jumlah Ruta Tercacah', 'Jumlah Prelist KK Tani', 'Jumlah Dokumen L2 Terpakai', 'Jumlah Dokumen L2 PPL ke PML', 'Jumlah Dokumen L2 dari PML ke Koseka', 'Sudah Selesai', 'Sudah Isi Repo']]
    st.dataframe(df_show)
    #df2 = df.groupby(["Kode Kecamatan", "Nama Kecamatan"])['Kondisi Terkini'].apply(lambda x: x.astype(int).sum())