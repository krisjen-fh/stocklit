import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import csv
import pandas as pd

state = st.session_state

st.set_page_config(
    page_title='Stocklit',
    page_icon='📈'
)

def read_company_data(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=';')
        company_data = {row['Company Name']: row['Stock Code'] for row in reader}

        file.seek(0)
        reader = csv.DictReader(file, delimiter=';')
        company_data2 = {row['Stock Code']: row['Company Name'] for row in reader}

    return company_data, company_data2

def welcome_page():
    st.markdown("""
    <div style="display: flex; justify-content: start; align-items: center; height: 15vh; width: 150vh;">
        <h1 style="font-size: 30px; color: white; ">
            Selamat Datang di
        </h1>
        <h2 style="font-size: 80px; color: red; font-weight: 900">
            STOCKLIT
        </h2>
    </div>
    """, unsafe_allow_html=True)

    st.write("Analisis Saham Terasa Menyenangkan")

    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"]  {
    background-image: url("https://i.pinimg.com/originals/b1/a7/78/b1a778b8e9704e10bdec549ce8494143.jpg");
    background-size: cover;

    }
    [data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    if st.button("Lanjut"):
        state.page = 'input_page'

def input_page(company_data, company_data2):
    st.sidebar.markdown (f"""
        <div style="display: flex; justify-content: left; align-items: center; height: 0vh;">
            <h1 style="font-size: 17px;font-family: 'Sans Serif';font-weight: 300;line-height:1.9; color: white;">
                Cari Nama Perusahaan
            </h1>
        </div>
        """, unsafe_allow_html=True)
    selected_company1 = st.sidebar.selectbox(
    'Pilih Perusahaan',
    options=list(company_data.keys()),
    index=None,
    placeholder="Pilih Perusahaan"
    )
    st.sidebar.markdown(f"""
        <div style="display: flex; justify-content: start; align-items: center; height: 5vh; width: 60vh">
            <h1 style="font-size: 17px;font-family: 'Sans Serif';font-weight: 300;line-height:1; color: white;margin-right:10px">
                Kode Saham: 
            </h1>
            <h2 style="font-size: 25px;font-family: 'Sans Serif';font-weight: 800;line-height:1.9; color: white; width: 10vh">
                {company_data[selected_company1]} 
            </h2>
        </div>
        """, unsafe_allow_html=True)
    st.sidebar.markdown (f"""
        <div style="display: flex; justify-content: left; align-items: center; height: 5vh;">
            <h1 style="font-size: 17px;font-family: 'Sans Serif';font-weight: 300;line-height:1.9; color: white;">
                Bandingkan dengan Perusahaan
            </h1>
        </div>
        """, unsafe_allow_html=True)
    selected_company2 = st.sidebar.selectbox('  ', ['Pilih Perusahaan'] + list(company_data.keys()))
    st.sidebar.markdown(f"""
        <div style="display: flex; justify-content: start; align-items: center; height: 5vh; width: 60vh">
            <h1 style="font-size: 17px;font-family: 'Sans Serif';font-weight: 300;line-height:1; color: white;margin-right:10px">
                Kode Saham: 
            </h1>
            <h2 style="font-size: 25px;font-family: 'Sans Serif';font-weight: 800;line-height:1.9; color: white; width: 10vh">
                {company_data[selected_company2]}
            </h2>
        </div>
        """, unsafe_allow_html=True)
    if selected_company1 =='Pilih Perusahaan' and selected_company2 =='Pilih Perusahaan':
        st.warning('Pilih Saham Perusahaan Yang Ingin Anda Analisis')
    elif selected_company1 != 'Pilih Perusahaan' and selected_company2=='Pilih Perusahaan':
        st.markdown (f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 15vh;">
            <h1 style="font-size: 27px;font-family: 'Sans Serif';font-weight: 700;line-height:1.9; color: white; margin: 0;">
                Informasi Saham {company_data[selected_company1]} 
            </h1>
        </div>
        """, unsafe_allow_html=True)
        ticker_data1 = get_ticker_data(selected_company1)
        tabel1=data_tabel(ticker_data1,selected_company1)
        grafik1=plot_candle_chart(ticker_data1,selected_company1)
        st.plotly_chart(grafik1)
        pie_plot1=pie_plot(ticker_data1,selected_company1)
        st.plotly_chart(pie_plot1,
                    config ={'displayModeBar':False})
        analisis1=analyze_stock(ticker_data1,selected_company1)
        st.plotly_chart(analisis1,
                    config ={'displayModeBar':False}
                    )
    elif selected_company1 != 'Pilih Perusahaan' and selected_company2 != 'Pilih Perusahaan' and selected_company1!= selected_company2:
        st.markdown (f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 15vh;">
            <h1 style="font-size: 27px;font-family: 'Sans Serif';font-weight: 700;line-height:1.9; color: white; margin: 0;">
                Informasi Saham {company_data[selected_company1]} dan {company_data[selected_company2]}
            </h1>
        </div>
        """, unsafe_allow_html=True)
        
        ticker_data1 = get_ticker_data(selected_company1)
        tabel1=data_tabel(ticker_data1,selected_company1)
        grafik1=plot_candle_chart(ticker_data1,selected_company1)
        pie_plot1=pie_plot(ticker_data1,selected_company1)
        analisis1=analyze_stock(ticker_data1,selected_company1)

        ticker_data2 = get_ticker_data(selected_company2)
        tabel2=data_tabel(ticker_data2,selected_company2)
        grafik2=plot_candle_chart(ticker_data2,selected_company2)
        pie_plot2=pie_plot(ticker_data2,selected_company2)
        analisis2=analyze_stock(ticker_data2,selected_company2)
        
    elif selected_company1 == selected_company2:
        st.warning('Pilih Perusahaan yang berbeda')

def get_ticker_data(selected_company):
    ticker_data = {'Date': [], 'Company Name' : [], 'Open Price': [], 'Close Price': [], 'High Price': [], 'Low Price': [],  'Changes':[], 'Buyers':[], 'Sellers':[]}

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        ticker_data_list = [row for row in reader if row['Company Name'] == selected_company]
        if not ticker_data_list:
            st.write(f'Tidak Dapat Menemukan Kode Saham {selected_company}. Pilih Nama Saham Lainnya.')
        else:
            for row in ticker_data_list:
                ticker_data['Date'].append(row['Date'])
                ticker_data['Company Name'].append(str(row['Company Name']))
                ticker_data['Open Price'].append(float(row['Open Price']))
                ticker_data['Close Price'].append(float(row['Close']))
                ticker_data['High Price'].append(float(row['High']))
                ticker_data['Low Price'].append(float(row['Low']))
                ticker_data['Changes'].append(float(row['Change']))
                ticker_data['Buyers'].append(float(row['Offer Volume']))
                ticker_data['Sellers'].append(float(row['Bid Volume']))

    return ticker_data

def data_tabel(ticker_data,selected_company):
    df = pd.DataFrame(ticker_data)
    df.set_index(['Date'], inplace=True)
    df = df.drop(['Company Name'], axis=1)
    st.markdown (f"""
    <div style="display: flex; justify-content: left; align-items: center; height: 7vh;">
        <h1 style="font-size: 20px;font-family: 'Sans Serif';font-weight: 300;line-height:30; color: white;margin-right:40px">
            Tabel Saham {selected_company}
        </h1>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(df)
    return df

def plot_candle_chart(ticker_data,selected_company):
    st.markdown (f"""
    <div style="display: flex; justify-content: left; align-items: center; height: 7vh;">
        <h1 style="font-size: 20px;font-family: 'Sans Serif';font-weight: 300;line-height:30; color: white;margin-right:40px">
            Grafik Penjualan Saham {selected_company}
        </h1>
    </div>
    """, unsafe_allow_html=True)
    candle_fig = go.Figure()
    candle_fig.add_trace(
        go.Candlestick(x=ticker_data['Date'],
                       open=ticker_data['Open Price'],
                       close=ticker_data['Close Price'],
                       low=ticker_data['Low Price'],
                       high=ticker_data['High Price'],
        )
    )

    candle_fig.update_layout( 
        height = 400,
        xaxis_title='Tanggal',
        yaxis_title='Harga Saham',
    )
    st.plotly_chart(candle_fig)
    st.markdown("""
    <div style="text-align: right;">
        <h1 style="font-size:15px;">Keterangan</h1>
    </div>
    <div style="display: flex; align-items: center; flex-direction: row-reverse;">
        <div style="width: 15px; height: 15px; background-color: green; margin-left: 15px;"></div>
        <p style="margin: 0; font-size:10 px;">Nilai Saham Naik</p>
    </div>
        <div style="display: flex; align-items: center; flex-direction: row-reverse;">
        <div style="width: 15px; height: 15px; background-color: red; margin-left: 15px;"></div>
        <p style="margin: 0; font-size:10 px;">Nilai Saham Turun</p>
    </div>
    """, unsafe_allow_html=True)
    return candle_fig

def pie_plot(ticker_data,selected_company):
    colors = ['#fabd02', '#fdee87']
    st.markdown (f"""
    <div style="display: flex; justify-content: left; align-items: center; height: 7vh;">
        <h1 style="font-size: 20px;font-family: 'Sans Serif';font-weight: 300;line-height:30; color: white;margin-right:40px">
            Skala Penjual dan Pembeli Saham {selected_company}
        </h1>
    </div>
    """, unsafe_allow_html=True)
    pie_fig = go.Figure()
    pie_fig.add_trace(
        go.Pie(
            labels=['Pembeli', 'Penjual'],
            values=[sum(ticker_data['Buyers']), sum(ticker_data['Sellers'])],
            marker=dict(colors=colors),
            legendgroup = "group",
            domain=dict(x=[0, 1])
        )
    )

    pie_fig.update_layout(
        showlegend=False,
    )
    st.plotly_chart(pie_fig,  config ={'displayModeBar':False})
    st.markdown("""
    <div style="text-align: right;margin-top: 10px;">
        <h1 style="font-size:15px;">Keterangan</h1>
    </div>
    <div style="display: flex; align-items: left; flex-direction: row-reverse;">
        <div style="width: 15px; height: 15px; background-color: #fabd02; margin-left: 15px;"></div>
        <p style="margin: 0; font-size:10 px;">Pembeli</p>
    </div>
        <div style="display: flex; align-items: left; flex-direction: row-reverse;">
        <div style="width: 15px; height: 15px; background-color: #fdee87; margin-left: 15px;"></div>
        <p style="margin: 0; font-size:10 px;">Penjual</p>
    </div>
    """, unsafe_allow_html=True)
    return pie_fig

def analyze_stock(ticker_data,selected_company):
    st.markdown (f"""
    <div style="display: flex; justify-content: left; align-items: center; height: 7vh;">
        <h1 style="font-size: 20px;font-family: 'Sans Serif';font-weight: 300;line-height:30; color: white;margin-right:40px">
            Analisis Jual Beli Saham {selected_company}
        </h1>
    </div>
    """, unsafe_allow_html=True)
    indications = []
    for change in ticker_data['Changes']:
        if change > 0:
            indications.append('Jual')
        elif change < 0:
            indications.append('Beli')
        else:
            indications.append('Tahan')

    ticker_data['Indications'] = indications

    fig = px.line(x=ticker_data['Date'], y=ticker_data['Close Price'])
    fig.update_layout(xaxis_title='Tanggal', yaxis_title='Harga Closing', template='plotly_dark')

    for i, indication in enumerate(indications):
        fig.add_annotation(
            x=ticker_data['Date'][i],
            y=ticker_data['Close Price'][i],
            text=indication,
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40 if indication == 'Beli' else 40,
        )
    st.plotly_chart(fig,
                    config ={'displayModeBar':False}
                    )
    return fig

if __name__ == "__main__":
    file_path = "C:\\Users\\E L I T E B O O K\\OneDrive\\Documents\\SEM 1\\PROGRAM DASAR\\New folder\\work\\saham1.csv"
    st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
    )
    if 'page' not in state:
        state.page = 'welcome_page'
    if state.page == 'welcome_page':
        welcome_page()
    elif state.page == 'input_page':
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 12vh;">
            <h1 style="font-size: 50px; color: red; margin: auto;">
                STOCKLIT
            </h1>
        </div>
        """, unsafe_allow_html=True)
        st.markdown ("""
        <div style="display: flex; justify-content: center; align-items: center; height: 7vh;">
            <h1 style="font-size: 15px;font-family: 'Sans Serif';font-weight: 545;line-height:1.9; color: white; margin: 0;">
                Periode Data Saham : 2 Oktober - 1 Desember 2023
            </h1>
        </div>
        """, unsafe_allow_html=True)
        result_data, result_data2 = read_company_data(file_path)
        input_page(result_data, result_data2)
