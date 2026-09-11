import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# 기본 설정
# ==================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)


# ==================================================
# 그래프 색상
# 노란색 / 연하늘색 / 연초록색 / 베이비핑크
# ==================================================

GRAPH_COLORS = [
    "#FFD966",  # 노란색
    "#9DD9F3",  # 연하늘색
    "#B7E4C7",  # 연초록색
    "#F7B6C8",  # 베이비핑크
]


# ==================================================
# 화면 디자인
# ==================================================

st.markdown(
    """
    <style>

    /* ==========================================
       전체 배경
       ========================================== */

    .stApp {
        background:
            linear-gradient(
                180deg,
                #BFE7FF 0%,
                #DDF3FF 48%,
                #EEF9FF 100%
            );

        overflow-x: hidden;
    }


    /* ==========================================
       움직이는 구름
       HTML div를 사용하지 않고
       CSS pseudo-element만 사용
       ========================================== */

    .stApp::before {
        content: "";

        position: fixed;

        width: 420px;
        height: 120px;

        top: 14%;
        left: -500px;

        z-index: 0;

        pointer-events: none;

        opacity: 0.62;

        background:
            radial-gradient(
                ellipse at 25% 70%,
                rgba(255,255,255,0.95) 0 18%,
                transparent 19%
            ),
            radial-gradient(
                ellipse at 45% 50%,
                rgba(255,255,255,0.95) 0 25%,
                transparent 26%
            ),
            radial-gradient(
                ellipse at 68% 65%,
                rgba(255,255,255,0.95) 0 22%,
                transparent 23%
            ),
            radial-gradient(
                ellipse at 82% 72%,
                rgba(255,255,255,0.90) 0 16%,
                transparent 17%
            );

        filter: blur(1px);

        animation:
            cloudMove1 55s linear infinite;
    }


    .stApp::after {
        content: "";

        position: fixed;

        width: 520px;
        height: 150px;

        top: 52%;
        left: -600px;

        z-index: 0;

        pointer-events: none;

        opacity: 0.42;

        background:
            radial-gradient(
                ellipse at 20% 70%,
                rgba(255,255,255,0.95) 0 17%,
                transparent 18%
            ),
            radial-gradient(
                ellipse at 38% 48%,
                rgba(255,255,255,0.95) 0 25%,
                transparent 26%
            ),
            radial-gradient(
                ellipse at 60% 60%,
                rgba(255,255,255,0.95) 0 22%,
                transparent 23%
            ),
            radial-gradient(
                ellipse at 80% 70%,
                rgba(255,255,255,0.90) 0 18%,
                transparent 19%
            );

        filter: blur(1px);

        animation:
            cloudMove2 75s linear infinite;
    }


    /* ==========================================
       구름 애니메이션
       ========================================== */

    @keyframes cloudMove1 {

        0% {
            transform: translateX(0);
        }

        100% {
            transform:
                translateX(
                    calc(100vw + 600px)
                );
        }
    }


    @keyframes cloudMove2 {

        0% {
            transform: translateX(0);
        }

        100% {
            transform:
                translateX(
                    calc(100vw + 700px)
                );
        }
    }


    /* ==========================================
       Streamlit 내용
       ========================================== */

    .main .block-container {

        position: relative;

        z-index: 5;

        padding-top: 2rem;

        padding-bottom: 3rem;
    }


    /* ==========================================
       제목
       ========================================== */

    h1,
    h2,
    h3 {

        color: #24445C;
    }


    /* ==========================================
       그래프 카드
       ========================================== */

    .graph-section {

        background:
            rgba(255, 255, 255, 0.78);

        border:
            1px solid
            rgba(255, 255, 255, 0.9);

        border-radius: 18px;

        padding: 1.5rem;

        margin: 1.5rem 0;

        box-shadow:
            0 8px 30px
            rgba(80, 150, 190, 0.10);

        backdrop-filter:
            blur(6px);
    }


    /* ==========================================
       그래프로 알 수 있는 것
       ========================================== */

    .graph-explanation {

        background:
            rgba(255, 249, 190, 0.90);

        border-left:
            5px solid
            #F3CE55;

        border-radius: 10px;

        padding: 0.9rem 1rem;

        color: #5A4A00;

        margin-top: 0.8rem;

        line-height: 1.7;
    }


    /* ==========================================
       영화 선택 박스
       ========================================== */

    div[data-baseweb="select"] > div {

        background-color:
            rgba(255, 255, 255, 0.90);

        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# 데이터 불러오기
# ==================================================

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():

    df = pd.read_csv(DATA_URL)


    # ----------------------------------------------
    # 날짜 변환
    # YYYYMMDD → 실제 날짜
    # ----------------------------------------------

    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce",
    )


    # ----------------------------------------------
    # 숫자형 데이터 변환
    # ----------------------------------------------

    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수",
    ]


    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )


    return df


df = load_data()


# ==================================================
# 제목
# ==================================================

st.title(
    "🎬 영화 데이터 그래프 도감 1 - 시간"
)


st.write(
    "1년치 일별 박스오피스 데이터를 이용해 "
    "영화의 시간에 따른 관객 변화를 살펴봅니다."
)


# ==================================================
# 그래프 1
# ==================================================

st.markdown(
    '<div class="graph-section">',
    unsafe_allow_html=True,
)


st.subheader(
    "그래프 1. 영화별 일관객 변화"
)


# ==================================================
# 영화 선택
# ==================================================

movie_list = sorted(
    df["영화명"]
    .dropna()
    .unique()
)


selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
)


# ==================================================
# 선택한 영화 데이터
# ==================================================

movie_df = (
    df[
        df["영화명"] == selected_movie
    ]
    .sort_values("날짜")
    .copy()
)


# ==================================================
# 최다 관객 날짜
# ==================================================

max_row = movie_df.loc[
    movie_df["일관객"].idxmax()
]


max_date = max_row["날짜"]


max_audience = int(
    max_row["일관객"]
)


# ==================================================
# 그래프 1
# ==================================================

fig1 = px.line(

    movie_df,

    x="날짜",

    y="일관객",

    markers=True,

    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
    },

    title=(
        f"{selected_movie} - "
        "날짜별 일관객 변화"
    ),

    color_discrete_sequence=[
        GRAPH_COLORS[0]
    ],
)


# ==================================================
# 마우스 오버
# ==================================================

fig1.update_traces(

    hovertemplate=
        "날짜: %{x|%Y-%m-%d}"
        "<br>"
        "관객수: %{y:,}명"
        "<extra></extra>"
)


# ==================================================
# ① 흥행 추이
# ==================================================

fig1.add_annotation(

    xref="paper",

    yref="paper",

    x=0.01,

    y=0.97,

    text="① 시간에 따른 흥행 추이",

    showarrow=False,

    font=dict(
        size=14,
        color="#315B73",
    ),

    bgcolor=(
        "rgba(255,255,255,0.82)"
    ),

    bordercolor="#A8D8F0",

    borderwidth=1,

    borderpad=6,

    xanchor="left",

    yanchor="top",
)


# ==================================================
# ② 가장 많은 관객이 몰린 날
# ==================================================

fig1.add_annotation(

    x=max_date,

    y=max_audience,

    text=(
        "<b>② 가장 많은 관객이 몰린 날</b>"
        "<br>"
        f"{max_date.strftime('%Y-%m-%d')}"
        "<br>"
        f"<b>{max_audience:,}명</b>"
    ),

    showarrow=True,

    arrowhead=2,

    arrowsize=1,

    arrowwidth=2,

    arrowcolor="#E07A5F",

    ax=0,

    ay=-80,

    bgcolor=(
        "rgba(255,250,220,0.95)"
    ),

    bordercolor="#E8B44D",

    borderwidth=2,

    borderpad=8,

    font=dict(
        size=13,
        color="#5A4200",
    ),
)


# ==================================================
# 최다 관객 점 강조
# ==================================================

max_point = movie_df[
    movie_df["날짜"] == max_date
]


fig1.add_trace(

    px.scatter(

        max_point,

        x="날짜",

        y="일관객",

    ).data[0]
)


fig1.data[-1].update(

    marker=dict(

        size=13,

        color=GRAPH_COLORS[3],

        line=dict(

            color="white",

            width=2,
        ),
    ),

    hovertemplate=
        "⭐ 최다 관객"
        "<br>"
        "날짜: %{x|%Y-%m-%d}"
        "<br>"
        "관객수: %{y:,}명"
        "<extra></extra>",
)


# ==================================================
# 그래프 1 디자인
# ==================================================

fig1.update_layout(

    hovermode="x unified",

    xaxis_title="날짜",

    yaxis_title="일관객 수(명)",

    plot_bgcolor=(
        "rgba(255,255,255,0.55)"
    ),

    paper_bgcolor=(
        "rgba(255,255,255,0)"
    ),

    margin=dict(

        l=20,

        r=20,

        t=80,

        b=20,
    ),
)


# ==================================================
# 그래프 1 출력
# ==================================================

st.plotly_chart(

    fig1,

    use_container_width=True,
)


# ==================================================
# 그래프 1 설명
# ==================================================

st.markdown(

    """
    <div class="graph-explanation">

        이 그래프로 알 수 있는 것:
        영화의 일별 관객수가 시간의 흐름에 따라
        어떻게 증가하고 감소했는지 알 수 있습니다.

    </div>
    """,

    unsafe_allow_html=True,
)


st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ==================================================
# 그래프 2
# ==================================================

st.markdown(
    '<div class="graph-section">',
    unsafe_allow_html=True,
)


st.subheader(
    "그래프 2. 일관객 합계가 가장 큰 영화 5편의 변화"
)


# ==================================================
# 영화별 일관객 합계
# ==================================================

movie_totals = (

    df.groupby("영화명")["일관객"]

    .sum()

    .sort_values(
        ascending=False
    )
)


# ==================================================
# 상위 5편
# ==================================================

top5_movies = (

    movie_totals

    .head(5)

    .index

    .tolist()
)


# ==================================================
# 상위 5편 데이터
# ==================================================

top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()


top5_df = top5_df.sort_values(
    [
        "날짜",
        "영화명",
    ]
)


# ==================================================
# 그래프 2
# ==================================================

fig2 = px.line(

    top5_df,

    x="날짜",

    y="일관객",

    color="영화명",

    markers=True,

    labels={

        "날짜": "날짜",

        "일관객": "일관객 수",

        "영화명": "영화",
    },

    title=(
        "기간 내 일관객 합계 상위 5편"
    ),

    color_discrete_sequence=GRAPH_COLORS,
)


# ==================================================
# 마우스 오버
# ==================================================

fig2.update_traces(

    hovertemplate=
        "<b>%{fullData.name}</b>"
        "<br>"
        "날짜: %{x|%Y-%m-%d}"
        "<br>"
        "관객수: %{y:,}명"
        "<extra></extra>"
)


# ==================================================
# ① 그래프 안 설명
# ==================================================

fig2.add_annotation(

    xref="paper",

    yref="paper",

    x=0.01,

    y=0.97,

    text=(
        "① 기간 전체에서 관객이 많이 모인 영화들의 변화"
    ),

    showarrow=False,

    font=dict(

        size=14,

        color="#315B73",
    ),

    bgcolor=(
        "rgba(255,255,255,0.82)"
    ),

    bordercolor="#A8D8F0",

    borderwidth=1,

    borderpad=6,

    xanchor="left",

    yanchor="top",
)


# ==================================================
# 그래프 2 디자인
# ==================================================

fig2.update_layout(

    hovermode="x unified",

    xaxis_title="날짜",

    yaxis_title="일관객 수(명)",

    plot_bgcolor=(
        "rgba(255,255,255,0.55)"
    ),

    paper_bgcolor=(
        "rgba(255,255,255,0)"
    ),

    margin=dict(

        l=20,

        r=20,

        t=80,

        b=20,
    ),

    legend=dict(

        title="영화",

        orientation="h",

        yanchor="bottom",

        y=1.02,

        xanchor="left",

        x=0,
    ),
)


# ==================================================
# 그래프 2 출력
# ==================================================

st.plotly_chart(

    fig2,

    use_container_width=True,
)


# ==================================================
# 그래프 2 설명
# ==================================================

st.markdown(

    """
    <div class="graph-explanation">

        이 그래프로 알 수 있는 것:
        영화의 일별 관객수가 시간의 흐름에 따라
        어떻게 증가하고 감소했는지 알 수 있습니다.

    </div>
    """,

    unsafe_allow_html=True,
)


st.markdown(
    "</div>",
    unsafe_allow_html=True,
)
