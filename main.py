import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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
# ==================================================

GRAPH_COLORS = [
    "#FFD966",
    "#9DD9F3",
    "#B7E4C7",
    "#F7B6C8",
]


# ==================================================
# 화면 디자인
# ==================================================

st.markdown(
    """
    <style>

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

    .main .block-container {
        position: relative;
        z-index: 5;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1,
    h2,
    h3 {
        color: #24445C;
    }

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

    # 날짜 변환
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


fig1.update_traces(
    hovertemplate=
        "날짜: %{x|%Y-%m-%d}"
        "<br>"
        "관객수: %{y:,}명"
        "<extra></extra>"
)


# ==================================================
# 흥행 추이
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
# 최다 관객 표시
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
# 최다 관객 점
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


fig2.update_traces(
    hovertemplate=
        "<b>%{fullData.name}</b>"
        "<br>"
        "날짜: %{x|%Y-%m-%d}"
        "<br>"
        "관객수: %{y:,}명"
        "<extra></extra>"
)


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


st.plotly_chart(
    fig2,
    use_container_width=True,
)


st.markdown(
    """
    <div class="graph-explanation">
        <b>이 그래프로 알 수 있는 것:</b><br>
        기간 전체에서 관객수가 많았던 영화 5편이
        날짜에 따라 어떻게 흥행했는지 비교할 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ==================================================
# 공통 분석 기간
# ==================================================

st.markdown("---")

st.subheader("📅 그래프 3~5 분석 기간")

latest_date = df["날짜"].max()

selected_end_date = st.date_input(
    "기준 날짜를 선택하세요.",
    value=latest_date.date(),
    min_value=df["날짜"].min().date(),
    max_value=latest_date.date(),
)

selected_end_date = pd.Timestamp(
    selected_end_date
)

selected_start_date = (
    selected_end_date
    - pd.Timedelta(days=29)
)


st.write(
    f"📌 분석 기간: "
    f"**{selected_start_date.strftime('%Y-%m-%d')} ~ "
    f"{selected_end_date.strftime('%Y-%m-%d')}**"
)


period_df = df[
    (df["날짜"] >= selected_start_date)
    & (df["날짜"] <= selected_end_date)
].copy()


# ==================================================
# 그래프 3
# 날짜별 TOP 10 일관객 합계
# ==================================================

st.markdown(
    '<div class="graph-section">',
    unsafe_allow_html=True,
)

st.subheader(
    "그래프 3. 날짜별 TOP 10 일관객 합계"
)

st.caption(
    "각 날짜의 TOP 10 영화 일관객을 모두 더한 값입니다."
)


# TOP 10만 사용
top10_df = period_df[
    period_df["순위"] <= 10
].copy()


# 날짜별 합계
daily_top10 = (
    top10_df
    .groupby(
        "날짜",
        as_index=False
    )["일관객"]
    .sum()
)


# 30일 전체 날짜 생성
all_dates = pd.DataFrame(
    {
        "날짜": pd.date_range(
            selected_start_date,
            selected_end_date,
        )
    }
)


daily_top10 = all_dates.merge(
    daily_top10,
    on="날짜",
    how="left",
)


# 데이터 없는 날은 0
daily_top10["일관객"] = (
    daily_top10["일관객"]
    .fillna(0)
)


# 가장 큰 3일
top3_days = (
    daily_top10
    .sort_values(
        "일관객",
        ascending=False
    )
    .head(3)
)


# 영역 그래프
fig3 = px.area(
    daily_top10,
    x="날짜",
    y="일관객",
    title=(
        "최근 30일 날짜별 TOP 10 일관객 합계"
    ),
)


# 연보라색
fig3.update_traces(
    line=dict(
        color="#A77BCA",
        width=3,
    ),
    fillcolor=(
        "rgba(216,196,232,0.65)"
    ),
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>"
        "10위권 일관객 합계: %{y:,}명"
        "<extra></extra>"
    ),
)


# TOP 3 표시
for _, row in top3_days.iterrows():

    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=(
            f"<b>"
            f"{row['날짜'].strftime('%m/%d')}"
            f"</b>"
            f"<br>"
            f"{int(row['일관객']):,}명"
        ),
        showarrow=True,
        arrowhead=2,
        ay=-55,
        bgcolor=(
            "rgba(255,255,255,0.95)"
        ),
        bordercolor="#A77BCA",
        borderwidth=2,
        borderpad=5,
        font=dict(
            size=12,
            color="#5A3D6B",
        ),
    )


fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)",
    plot_bgcolor=(
        "rgba(255,255,255,0.55)"
    ),
    paper_bgcolor=(
        "rgba(255,255,255,0)"
    ),
    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20,
    ),
)


st.plotly_chart(
    fig3,
    use_container_width=True,
)


st.markdown(
    """
    <div class="graph-explanation">
        이 그래프로 알 수 있는 것:
        매일 TOP 10 영화가 기록한 관객수를 모두 합쳐
        날짜별 전체 관객 규모를 비교할 수 있습니다.
        그래프 위에는 관객 합계가 가장 컸던 3일이 표시됩니다.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ==================================================
# 그래프 4
# 영화별 30일 일관객 합계 TOP 10
# ==================================================

st.markdown(
    '<div class="graph-section">',
    unsafe_allow_html=True,
)

st.subheader(
    "그래프 4. 최근 30일 영화별 일관객 TOP 10"
)

st.caption(
    "30일 동안 TOP 10에 들어온 날의 일관객을 영화별로 합산합니다."
)


# TOP 10 데이터
movie_top10 = period_df[
    period_df["순위"] <= 10
].copy()


# 영화별 집계
movie_sum = (
    movie_top10
    .groupby(
        ["영화코드", "영화명"],
        as_index=False,
    )
    .agg(
        기간관객합계=(
            "일관객",
            "sum",
        ),
        TOP10진입일수=(
            "날짜",
            "nunique",
        ),
    )
    .sort_values(
        "기간관객합계",
        ascending=False,
    )
    .head(10)
)


# 가로 막대그래프용 역순
movie_plot = movie_sum.sort_values(
    "기간관객합계",
    ascending=True,
)


fig4 = px.bar(
    movie_plot,
    x="기간관객합계",
    y="영화명",
    orientation="h",
    title=(
        "최근 30일 영화별 일관객 합계 TOP 10"
    ),
)


fig4.update_traces(
    marker_color="#F7B6C8",
    customdata=movie_plot[
        ["TOP10진입일수"]
    ].to_numpy(),
    hovertemplate=(
        "<b>%{y}</b>"
        "<br>"
        "30일간 관객 합계: %{x:,}명"
        "<br>"
        "TOP 10 진입 일수: %{customdata[0]}일"
        "<extra></extra>"
    ),
)


fig4.update_layout(
    xaxis_title="30일간 일관객 합계(명)",
    yaxis_title="영화",
    plot_bgcolor=(
        "rgba(255,255,255,0.55)"
    ),
    paper_bgcolor=(
        "rgba(255,255,255,0)"
    ),
    margin=dict(
        l=20,
        r=80,
        t=60,
        b=20,
    ),
)


st.plotly_chart(
    fig4,
    use_container_width=True,
)


st.markdown(
    """
    <div class="graph-explanation">
        이 그래프로 알 수 있는 것
        최근 30일 동안 TOP 10에 들어온 영화들의
        일관객을 모두 합쳐 관객이 가장 많았던 영화 10편을 보여줍니다.
        영화 막대에 마우스를 올리면
        TOP 10 진입 일수도 확인할 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ==================================================
# 그래프 5
# 월 × 요일별 일관객 합계 히트맵
# ==================================================

st.markdown(
    '<div class="graph-section">',
    unsafe_allow_html=True,
)

st.subheader(
    "그래프 5. 월 × 요일별 일관객 합계"
)

st.caption(
    "월과 요일에 따라 TOP 10 영화의 관객수가 "
    "어떻게 달라지는지 보여줍니다."
)


heat_df = period_df[
    period_df["순위"] <= 10
].copy()


# 월
heat_df["월"] = (
    heat_df["날짜"].dt.month
)


# 요일 번호
heat_df["요일번호"] = (
    heat_df["날짜"].dt.weekday
)


# 요일
weekday_names = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일",
]


heat_df["요일"] = (
    heat_df["요일번호"]
    .map(
        dict(
            enumerate(
                weekday_names
            )
        )
    )
)


# 월 × 요일 관객 합계
heat_sum = (
    heat_df
    .groupby(
        [
            "월",
            "요일번호",
            "요일",
        ],
        as_index=False,
    )["일관객"]
    .sum()
)


# 피벗
heat_pivot = heat_sum.pivot(
    index="월",
    columns="요일번호",
    values="일관객",
)


# 월요일 → 일요일
heat_pivot = heat_pivot.reindex(
    columns=range(7)
)


heat_pivot.columns = (
    weekday_names
)


# 히트맵
fig5 = px.imshow(
    heat_pivot,
    x=weekday_names,
    y=[
        f"{x}월"
        for x in heat_pivot.index
    ],
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계",
    },
    color_continuous_scale=[
        "#F5EEFA",
        "#E7D7F0",
        "#D5BCE3",
        "#B991CF",
        "#8F5FB5",
    ],
    aspect="auto",
    title=(
        "월 × 요일별 TOP 10 일관객 합계"
    ),
)


fig5.update_traces(
    hovertemplate=(
        "월: %{y}"
        "<br>"
        "요일: %{x}"
        "<br>"
        "일관객 합계: %{z:,}명"
        "<extra></extra>"
    )
)


fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    plot_bgcolor=(
        "rgba(255,255,255,0.55)"
    ),
    paper_bgcolor=(
        "rgba(255,255,255,0)"
    ),
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20,
    ),
)


st.plotly_chart(
    fig5,
    use_container_width=True,
)


st.markdown(
    """
    <div class="graph-explanation">
        이 그래프로 알 수 있는 것:
        월과 요일에 따라 TOP 10 영화의 관객수가
        어떻게 달라지는지 한눈에 볼 수 있습니다.
        <b>색이 진할수록 관객 합계가 많습니다.
        요일은 월요일 → 일요일 순서입니다.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)
