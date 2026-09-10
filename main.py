import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)


# --------------------------------------------------
# 화면 스타일
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFF9DB;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #4A3B00;
    }

    .graph-section {
        background-color: #FFFDF0;
        border: 1px solid #F0E3A1;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }

    .graph-explanation {
        background-color: #FFF4B8;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: #5A4A00;
        margin-top: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜: YYYYMMDD 형태의 숫자/문자열 → 실제 날짜
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce",
    )

    # 숫자형 데이터 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


df = load_data()


# --------------------------------------------------
# 제목
# --------------------------------------------------
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write(
    "1년치 일별 박스오피스 데이터를 이용해 영화의 시간에 따른 관객 변화를 살펴봅니다."
)


# --------------------------------------------------
# 그래프 1
# --------------------------------------------------
st.markdown('<div class="graph-section">', unsafe_allow_html=True)

st.subheader("그래프 1. 영화별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
)

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
    .copy()
)

fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
    },
    title=f"{selected_movie} - 날짜별 일관객 변화",
)

fig.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    plot_bgcolor="#FFFDF0",
    paper_bgcolor="#FFFDF0",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.markdown(
    """
    <div class="graph-explanation">
    <b>이 그래프로 알 수 있는 것</b>:
    영화의 일별 관객수가 시간의 흐름에 따라 어떻게 증가하고 감소했는지 알 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# 앞으로 추가할 그래프 영역
# --------------------------------------------------
st.markdown("---")

st.subheader("📊 다음 그래프")

st.info(
    "앞으로 이곳에 누적관객, 순위, 스크린 수, 상영횟수 등 시간에 따른 다양한 그래프를 추가할 수 있습니다."
)
