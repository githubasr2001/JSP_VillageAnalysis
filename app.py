import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64

# Set page config
st.set_page_config(
    page_title="Janasena Party Election Analysis",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 1rem;
    }
    .stTitle {
        font-size: 2.5rem !important;
        color: #FF4B4B;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for data
if 'data_initialized' not in st.session_state:
    # Previous constituency data (unchanged)
    # Gudem Constituency Data
    gudem_round_data = {
        "Round": list(range(1, 16)),
        "JSP": [5921, 7784, 7388, 7336, 7387, 6744, 10085, 8148, 9098, 8883, 8538, 8174, 6067, 6860, 6542],
        "YCP": [4357, 4430, 3982, 3192, 4415, 3047, 2507, 2870, 2036, 2950, 3911, 4024, 3793, 3937, 3994],
        "Majority": [1564, 3354, 3406, 4144, 2972, 3697, 7578, 5278, 7062, 5933, 4627, 4150, 2274, 2923, 2548]
    }
    
    # Bhimavaram Constituency Data
    bvrm_round_data = {
        "Round": list(range(1, 18)),
        "JSP": [7481, 7001, 8084, 7891, 7877, 8516, 8200, 9102, 7903, 7773, 7392, 7838, 7983, 5937, 7011, 6802, 5910],
        "YCP": [3348, 4122, 3754, 3266, 2333, 3285, 3237, 2732, 4462, 3358, 4094, 3691, 4240, 3996, 3986, 4845, 3908],
        "Majority": [4133, 2879, 4330, 4625, 5544, 5231, 4963, 6365, 3441, 4415, 3298, 4147, 3743, 1941, 3025, 1957, 2002]
    }

    # Pithapuram Constituency Data
    ptp_round_data = {
        "Round": list(range(1, 19)),
        "JSP": [7940, 7932, 8062, 9065, 7694, 6004, 7746, 8932, 7570, 9216, 8359, 7862, 7625, 7063, 7336, 5407, 6446, 2466],
        "YCP": [3754, 4121, 2565, 3420, 4015, 4032, 3344, 3546, 4094, 2480, 2478, 3434, 4178, 4457, 3996, 4531, 3971, 1140],
        "Majority": [4186, 3811, 5497, 5645, 3679, 1972, 4402, 5386, 3476, 6736, 5881, 4428, 3447, 2606, 3340, 876, 2475, 1326]
    }

    # Nidadavole Round Data
    ndv_round_data = {
        "Round": list(range(1, 17)),
        "JSP": [7091, 8088, 6862, 6478, 4709, 7145, 6754, 5225, 7280, 7908, 7702, 7904, 6856, 7695, 3424, 1578],
        "YCP": [5363, 4659, 5043, 4551, 3998, 4164, 5104, 4533, 5348, 4844, 4550, 4260, 4716, 5554, 1935, 773],
        "Majority": [1728, 3429, 1819, 1927, 711, 2981, 1650, 692, 1932, 3064, 3152, 3644, 2140, 2141, 1489, 805]
    }

    # Unguturu Round Data
    unguturu_round_data = {
        "Round": list(range(1, 18)) + ['Postal'],
        "JSP": [6269, 7027, 6140, 7154, 7217, 6746, 7781, 6549, 6906, 7224, 6833, 6117, 8612, 8070, 6352, 2284, 634, 979],
        "YCP": [4925, 4412, 4039, 4772, 4475, 4339, 4315, 3986, 4051, 3541, 3775, 3630, 3904, 4144, 3680, 1186, 298, 477],
        "Majority": [1344, 2615, 2101, 2382, 2742, 2407, 3466, 2563, 2855, 3683, 3058, 2487, 4708, 3926, 2672, 1098, 336, 502]
    }
    
    # Create DataFrames for round-wise data
    st.session_state.gudem_df = pd.DataFrame(gudem_round_data)
    st.session_state.gudem_df.set_index('Round', inplace=True)
    
    st.session_state.bvrm_df = pd.DataFrame(bvrm_round_data)
    st.session_state.bvrm_df.set_index('Round', inplace=True)

    st.session_state.ptp_df = pd.DataFrame(ptp_round_data)
    st.session_state.ptp_df.set_index('Round', inplace=True)

    st.session_state.ndv_df = pd.DataFrame(ndv_round_data)
    st.session_state.ndv_df.set_index('Round', inplace=True)

    st.session_state.unguturu_df = pd.DataFrame(unguturu_round_data)
    st.session_state.unguturu_df.set_index('Round', inplace=True)
    
    # Area data for each constituency (keeping previous data)
    # Village/Area data for each constituency
    st.session_state.gudem_village_data = pd.DataFrame({
        'Village': [
            'Prattipadu', 'Darshipuru', 'Vallurupalli', 'Racharla', 'Allampuram',
            'Ravipadu', 'Bodapadu', 'Pentapadu', 'Jattipalem', 'Manjipadu',
            'Umamaheshwaram', 'Yanalapalli', 'Padamara Vippuru', 'Parimella',
            'Kashpamentapadu', 'Akutigepadu', 'Mudunuru', 'Chintapalli',
            'Korumilli', 'B.Kondepudu', 'Minavalluru'
        ],
        'JSP': [
            2311, 2272, 1149, 1069, 2299, 1800, 544, 4589, 1082, 745,
            407, 525, 2466, 1156, 1557, 907, 1200, 446, 592, 1026, 1308
        ],
        'YCP': [
            1383, 892, 631, 563, 1465, 671, 292, 2939, 716, 367,
            404, 377, 1303, 614, 927, 538, 521, 431, 388, 770, 456
        ]
    })
    
    st.session_state.bvrm_area_data = pd.DataFrame({
        'Area': [
            'Shivaraopeta (44, 46)', 'Nehrupeta (45)', 'Balusumudi (57)',
            'Nachuvaari Kudali (73)', 'Nachuvaari Kudali (110)', 'Kotta Bustand (78)',
            'Rest House Road (85, 88)', 'Veeramma park (94)', 'Bank Colony (104)',
            'SP Street (105)', 'Jethanpet (106112)', 'Narsayya Lakshmanarao (127)',
            'Housing Board Colony (128)'
        ],
        'JSP': [1670, 520, 847, 790, 802, 790, 1286, 494, 544, 629, 1592, 349, 376],
        'YCP': [320, 83, 232, 246, 165, 246, 272, 61, 93, 108, 336, 97, 102]
    })

    # Pithapuram village data
    villages_1 = pd.DataFrame({
        "Village": [
            "KODAVALI", "CHENDURTHI", "DURGADA", "JAGGAMPETA", "VANNIPUDI", "TADIPATRI", 
            "CHEBROLU", "MALLAVARAM", "GOLLAPROLU", "MADHAPURAM", "NAVAKANDRAVADA", 
            "KOLANKA", "MANIGITURTHI", "VIRVA", "VIRVADA", "MALLAM", "JALLOR", 
            "PK PALEM", "KANDARADA", "N KANDARADA", "DONTHAMURU", "VELDHUTRI", 
            "JAGAPATI RAJAPURAM", "KORIVADA", "JAMULAPALLI", "AV NAGARAM", "KOTHURU"
        ],
        "JSP": [1198, 1528, 5533, 1042, 1098, 4065, 7526, 1873, 12149, 1147, 601, 
                2401, 1231, 2048, 3187, 2327, 1404, 912, 1370, 410, 1322, 925, 48, 
                1081, 475, 393, 740],
        "YCP": [1263, 1130, 1271, 874, 1109, 1749, 2405, 1253, 4821, 466, 627, 951, 
                564, 742, 1422, 691, 731, 432, 395, 639, 646, 569, 258, 300, 619, 
                275, 441]
    })

    villages_2 = pd.DataFrame({
        "Village": [
            "NARINGIPURAM", "RAPARTHI", "P.RAYAVARAM", "P.THIMMAPURAM", "BHOGAPURAM",
            "B.PRATHIPADU", "KUMARAPURAM", "PITAPURAM", "CHITRADA", "RAMANAKKAPETA",
            "MOOLAPETA", "PONNADA", "SEZ MOOLAPETA", "AMARAVALLI", "MOOLAPETA",
            "AMINABAD", "UPPADA", "KOTHAPALLI", "KUTUKUDUMILLI", "SUBBAMIPETA",
            "VAKATIPPA", "YENDAPALLI", "NAGULAPALLI", "PATTHA ISUKAPALLI",
            "KOTHA ISUKAPALLI", "KONDI VARAM", "GORSA", "KOMARLAJUI"
        ],
        "JSP": [1029, 1431, 1119, 811, 1659, 2023, 1500, 25582, 3892, 2143, 437,
                3515, 465, 289, 2173, 2141, 5287, 1695, 990, 527, 1437, 2490, 1301,
                1337, 445, 351, 1286, 1274],
        "YCP": [823, 990, 454, 706, 774, 568, 425, 8917, 1324, 1563, 484, 1845, 482,
                422, 1193, 1557, 3410, 666, 331, 363, 869, 1132, 3133, 924, 365, 103,
                466, 996]
    })

    st.session_state.ptp_village_data = pd.concat([villages_1, villages_2])

    # Nidadavole Area Data
    st.session_state.ndv_area_data = pd.DataFrame({
        'Area': [
            'Korumamidi', 'Tadimalla', 'Unasaramilli', 'Katukoteshwaram', 'Suravaram', 
            'Thimmrajupeta', 'Ravimetta', 'Kanasalapeta', 'Singavaram', 'Thallpeta', 
            'Settipeta', 'Attapadu', 'Namasaguddem', 'Gopavaram', 'Vijayashwaram',
            'Purushottamapalli', 'D. Muthavaram', 'Pandalapuru', 'Jedigunta', 
            'Kalavacharla', 'Munipalli', 'Korupalli'
        ],
        'JSP': [
            2012, 2679, 632, 1214, 554, 1018, 1288, 1144, 771, 964, 829, 764, 
            3069, 1124, 1361, 1450, 1402, 1731, 642, 559, 953, 652
        ],
        'YCP': [
            2166, 1515, 336, 974, 372, 868, 797, 557, 644, 713, 537, 598, 
            2486, 772, 469, 1197, 685, 754, 511, 548, 787, 686
        ]
    })
    
    # Calculate additional metrics for all area data
    for df in [st.session_state.gudem_village_data, st.session_state.bvrm_area_data, 
               st.session_state.ptp_village_data, st.session_state.ndv_area_data]:
        df['Lead'] = df['JSP'] - df['YCP']
        df['Total_Votes'] = df['JSP'] + df['YCP']
        df['Lead_Percentage'] = (df['Lead'] / df['Total_Votes'] * 100).round(2)
    
    st.session_state.data_initialized = True



# Function to create download link
def get_download_link(df, filename):
    csv = df.to_csv().encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} Data</a>'
    return href

# Sidebar
st.sidebar.header("📋 Navigation")
constituency = st.sidebar.selectbox(
    "Select Constituency",
    ["Gudem", "Bhimavaram", "Pithapuram", "Nidadavole", "Unguturu"]
)

analysis_type = st.sidebar.radio(
    "Select Analysis Type",
    ["Round-wise Analysis", "Area-wise Analysis"]
)

# Function to get active constituency data
def get_active_data():
    if constituency == "Gudem":
        return st.session_state.gudem_df, st.session_state.gudem_village_data
    elif constituency == "Bhimavaram":
        return st.session_state.bvrm_df, st.session_state.bvrm_area_data
    elif constituency == "Pithapuram":
        return st.session_state.ptp_df, st.session_state.ptp_village_data
    elif constituency == "Nidadavole":
        return st.session_state.ndv_df, st.session_state.ndv_area_data
    else:  # Unguturu
        return st.session_state.unguturu_df, None

df_rounds, df_areas = get_active_data()

# Main content
st.title(f"📊 Janasena Party Election Analysis - {constituency} Constituency")

if analysis_type == "Round-wise Analysis":
    # Round-wise Analysis
    st.header("🔄 Round-wise Analysis")
    
    # Download link for round-wise data
    st.markdown(get_download_link(df_rounds, f"{constituency}_round_wise_data"), unsafe_allow_html=True)
    
    # Key metrics
    total_jsp = df_rounds['JSP'].sum()
    total_ycp = df_rounds['YCP'].sum()
    final_margin = total_jsp - total_ycp
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total JSP Votes", f"{total_jsp:,}")
    with col2:
        st.metric("Total YCP Votes", f"{total_ycp:,}")
    with col3:
        st.metric("Final Victory Margin", f"{final_margin:,}")
    
    # Round-wise visualization
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Round-wise Vote Comparison', 'Round-wise Lead Margin'),
        vertical_spacing=0.12
    )
    
    # Vote comparison
    fig.add_trace(
        go.Bar(name='JSP', x=df_rounds.index, y=df_rounds['JSP'], marker_color='red'),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(name='YCP', x=df_rounds.index, y=df_rounds['YCP'], marker_color='blue'),
        row=1, col=1
    )
    
    # Lead margin
    fig.add_trace(
        go.Bar(name='Lead Margin', x=df_rounds.index, y=df_rounds['Majority'], marker_color='green'),
        row=2, col=1
    )
    
    fig.update_layout(
        height=800,
        showlegend=True,
        title_text=f"{constituency} Constituency - Round-wise Analysis"
    )
    
    st.plotly_chart(fig, use_container_width=True)

else:  # Area-wise Analysis
    if df_areas is not None:
        st.header("📍 Area-wise Analysis")
        
        # Download link for area-wise data
        st.markdown(get_download_link(df_areas, f"{constituency}_area_wise_data"), unsafe_allow_html=True)
        
        # Sort areas by lead margin
        df_areas_sorted = df_areas.sort_values('Lead', ascending=False)
        
        # Area-wise visualization
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Area-wise Vote Comparison', 'Area-wise Lead Margin'),
            vertical_spacing=0.12
        )
        
        # Vote comparison
        fig.add_trace(
            go.Bar(name='JSP', x=df_areas_sorted.index, y=df_areas_sorted['JSP'], marker_color='red'),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(name='YCP', x=df_areas_sorted.index, y=df_areas_sorted['YCP'], marker_color='blue'),
            row=1, col=1
        )
        
        # Lead margin
        fig.add_trace(
            go.Bar(name='Lead Margin', x=df_areas_sorted.index, y=df_areas_sorted['Lead'], marker_color='green'),
            row=2, col=1
        )
        
        fig.update_layout(
            height=1000,
            showlegend=True,
            title_text=f"{constituency} Constituency - Area-wise Analysis"
        )
        
        # Update xaxis properties for better readability
        fig.update_xaxes(tickangle=45)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Area-wise data not available for this constituency.")