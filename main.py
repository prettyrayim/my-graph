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
# 화면 스타일 + 구름 애니메이션
# ==================================================
st.markdown(
    """
    <style>

    /* 전체 배경 */
    .stApp {
        background: linear-gradient(
            180deg,
            #BFE7FF 0%,
            #DDF3FF 45%,
            #EEF9FF 100%
        );

        overflow-x: hidden;
    }

    /* 내용 영역 */
    .main .block-container {
        position: relative;
        z-index: 5;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ==========================================
       구름 배경
       ========================================== */

    .cloud-background {
        position: fixed;
        inset: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        pointer-events: none;
        z-index: 0;
    }

    .cloud {
        position: absolute;
        background: rgba(255, 255, 255, 0.78);
        border-radius: 100px;
        filter: blur(1px);

        box-shadow:
            0 10px 30px rgba(120, 180, 210, 0.08);
    }

    .cloud::before,
    .cloud::after {
        content: "";
        position: absolute;
        background: inherit;
        border-radius: 50%;
    }

    .cloud::before {
        width: 45%;
        height: 150%;
        left: 15%;
        bottom: 0;
    }

    .cloud::after {
        width: 55%;
        height: 180%;
        right: 12%;
        bottom: 0;
    }


    /* 구름 1 */
    .cloud1 {
        width: 220px;
        height: 65px;
        top: 12%;
        left: -250px;
        animation: moveCloud1 55s linear infinite;
        opacity: 0.65;
    }

    /* 구름 2 */
    .cloud2 {
        width: 320px;
        height: 85px;
        top: 32%;
        left: -350px;
        animation: moveCloud2 75s linear infinite;
        opacity: 0.48;
    }

    /* 구름 3 */
    .cloud3 {
        width: 180px;
        height: 55px;
        top: 57%;
        left: -220px;
        animation: moveCloud3 62s linear infinite;
        opacity: 0.55;
    }

    /* 구름 4 */
    .cloud4 {
        width: 280px;
        height: 75px;
        top: 78%;
        left: -320px;
        animation: moveCloud4 85s linear infinite;
        opacity: 0.42;
    }


    @keyframes moveCloud1 {
        from {
            transform: translateX(0);
        }

        to {
            transform: translateX(calc(100vw + 500px));
        }
    }

    @keyframes moveCloud2 {
        from {
            transform: translateX(0);
        }

        to {
            transform: translateX(calc(100vw + 600px));
        }
    }

    @keyframes moveCloud3 {
        from {
            transform: translateX(0);
        }

        to {
            transform: translateX(calc(100vw + 450px));
        }
    }

    @keyframes moveCloud4 {
        from {
            transform: translateX(0);
        }

        to {
            transform: translateX(calc(100vw + 550px));
        }
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
        background: rgba(255, 255, 255, 0.78);

        border: 1px solid rgba(255, 255, 255, 0.9);

        border-radius: 18px;

        padding: 1.5rem;

        margin: 1.5rem 0;

        box-shadow:
            0 8px 30px rgba(80, 150, 190, 0.10);

        backdrop-filter: blur(6px);
    }


    /* ==========================================
       설명 박스
       ========================================== */

    .graph-explanation {
        background: rgba(255, 249, 190, 0.90);

        border-left: 5px solid #F3CE55;

        border-radius: 10px;

        padding: 0.9rem 1rem;

        color: #5A4A00;

        margin-top: 0.8rem;
    }


    /* 선택 박스 */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.90);

        border-radius: 10px;
    }

    </style>


    <!-- 움직이는 구름 -->
    <div class="cloud-background">

        <div class="cloud cloud1"></div>

        <div class="cloud cloud2"></div>

        <div class="cloud cloud3"></div>

        <div class="cloud cloud4"></div>

    </div>
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

    # 날짜를 진짜 날짜 형식으로 변환
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

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    return df


df = load_data()


# ==================================================
# 제목
# ==================================================

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

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

st.subheader("그래프 1. 영화별 일관객 변화")


# --------------------------------------------------
# 영화 선택
# --------------------------------------------------

movie_list = sorted(
    df["영화명"]
    .dropna()
    .unique()
)

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
)


# --------------------------------------------------
# 선택한 영화 데이터
# --------------------------------------------------

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
    .copy()
)


# ==================================================
# ⭐ 가장 많은 관객이 몰린 날 찾기
# ==================================================

max_row = movie_df.loc[
    movie_df["일관객"].idxmax()
]

max_date = max_row["날짜"]

max_audience = int(
    max_row["일관객"]
)


# ==================================================
# 선 그래프
# ==================================================

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


# ==================================================
# 마우스 오버
# ==================================================

fig.update_traces(
    hovertemplate=
        "날짜: %{x|%Y-%m-%d}"
        "<br>관객수: %{y:,}명"
        "<extra></extra>"
)


# ==================================================
# ⭐ 그래프 안에 설명 넣기
# ==================================================

# ① 흥행 추이 설명
fig.add_annotation(

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

    bgcolor="rgba(255,255,255,0.82)",

    bordercolor="#A8D8F0",

    borderwidth=1,

    borderpad=6,

    xanchor="left",
    yanchor="top",
)


# --------------------------------------------------
# ② 가장 많은 관객이 몰린 날 표시
# --------------------------------------------------

fig.add_annotation(

    x=max_date,

    y=max_audience,

    text=(
        f"<b>② 가장 많은 관객이 몰린 날</b><br>"
        f"{max_date.strftime('%Y-%m-%d')}<br>"
        f"<b>{max_audience:,}명</b>"
    ),

    showarrow=True,

    arrowhead=2,

    arrowsize=1,

    arrowwidth=2,

    arrowcolor="#E07A5F",

    ax=0,

    ay=-80,

    bgcolor="rgba(255,250,220,0.95)",

    bordercolor="#E8B44D",

    borderwidth=2,

    borderpad=8,

    font=dict(
        size=13,
        color="#5A4200",
    ),

)


# ==================================================
# 최대 관객 점 강조
# ==================================================

fig.add_trace(

    px.scatter(
        movie_df[
            movie_df["날짜"] == max_date
        ],

        x="날짜",

        y="일관객",
    ).data[0]

)


# 강조점 스타일
fig.data[-1].update(

    marker=dict(
        size=13,
        color="#E85D4A",
        line=dict(
            color="white",
            width=2,
        ),
    ),

    hovertemplate=
        "⭐ 최다 관객<br>"
        "날짜: %{x|%Y-%m-%d}"
        "<br>관객수: %{y:,}명"
        "<extra></extra>",
)


# ==================================================
# 그래프 디자인
# ==================================================

fig.update_layout(

    hovermode="x unified",

    xaxis_title="날짜",

    yaxis_title="일관객 수(명)",

    plot_bgcolor="rgba(255,255,255,0.55)",

    paper_bgcolor="rgba(255,255,255,0)",

    margin=dict(
        l=20,
        r=20,
        t=80,
        b=20,
    ),

)


# ==================================================
# 그래프 출력
# ==================================================

st.plotly_chart(
    fig,
    use_container_width=True,
)


# ==================================================
# 그래프로 알 수 있는 것
# ==================================================

st.markdown(
    """
    <div class="graph-explanation">

        <b>이 그래프로 알 수 있는 것</b><br>

        영화의 날짜별 관객 변화를 통해
        <b>시간에 따른 흥행 추이</b>와
        <b>관객이 가장 많이 몰린 시점</b>을
        찾아볼 수 있습니다.

    </div>
    """,

    unsafe_allow_html=True,
)


st.markdown(
    "</div>",
    unsafe_allow_html=True,
)
