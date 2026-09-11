import streamlit as st
import requests
import pandas as pd
import altair as alt

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# ==================================================
# 1. 화면 설정
# ==================================================

st.set_page_config(
    page_title="영화 박스오피스",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 박스오피스")
st.caption("영화관입장권통합전산망(KOBIS) 일일 박스오피스")


# ==================================================
# 2. 한국 시간 설정
# ==================================================

KST = ZoneInfo("Asia/Seoul")

today = datetime.now(KST).date()

# 오늘은 아직 집계 전이므로 어제까지만 선택 가능
yesterday = today - timedelta(days=1)


# ==================================================
# 3. 날짜 선택
# ==================================================

st.subheader("📅 조회할 날짜")

selected_date = st.date_input(
    "박스오피스를 보고 싶은 날짜를 선택하세요.",
    value=yesterday,
    min_value=datetime(2000, 1, 1).date(),
    max_value=yesterday
)

target_date = selected_date.strftime("%Y%m%d")

display_date = selected_date.strftime("%Y년 %m월 %d일")


# ==================================================
# 4. KOBIS API 데이터 가져오기
# ==================================================

@st.cache_data(ttl=3600)
def get_boxoffice(target_dt):

    # Streamlit Secrets에서 API 키 가져오기
    api_key = st.secrets["KOBIS_KEY"]

    url = (
        "https://www.kobis.or.kr/"
        "kobisopenapi/webservice/rest/boxoffice/"
        "searchDailyBoxOfficeList.json"
    )

    params = {
        "key": api_key,
        "targetDt": target_dt
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "empty": False,
            "error": f"API 요청에 실패했습니다.\n{e}"
        }

    except ValueError:

        return {
            "success": False,
            "empty": False,
            "error": "API가 올바른 데이터를 보내지 않았습니다."
        }


    # KOBIS API 오류 확인
    if "faultInfo" in data:

        fault = data["faultInfo"]

        return {
            "success": False,
            "empty": False,
            "error": (
                f"KOBIS API 오류\n"
                f"오류 코드: {fault.get('faultCode', '알 수 없음')}\n"
                f"오류 내용: {fault.get('message', '알 수 없음')}"
            )
        }


    # 박스오피스 결과 확인
    if "boxOfficeResult" not in data:

        return {
            "success": False,
            "empty": False,
            "error": "박스오피스 결과가 없습니다."
        }


    movie_list = data["boxOfficeResult"].get(
        "dailyBoxOfficeList",
        []
    )


    # 영화 목록이 없는 경우
    if not movie_list:

        return {
            "success": False,
            "empty": True,
            "error": ""
        }


    return {
        "success": True,
        "empty": False,
        "movies": movie_list
    }


# ==================================================
# 5. 선택한 날짜의 데이터 가져오기
# ==================================================

result = get_boxoffice(target_date)


# ==================================================
# 6. 데이터가 없는 경우
# ==================================================

if result["empty"]:

    st.warning("📭 그날은 아직 집계 전입니다.")
    st.info("다른 날짜를 선택해 주세요.")

    st.stop()


# ==================================================
# 7. API 오류
# ==================================================

if not result["success"]:

    st.error(
        "😥 박스오피스 데이터를 가져오지 못했습니다."
    )

    st.warning(
        """
다음 내용을 확인해 주세요.

• Streamlit Secrets에 KOBIS_KEY가 등록되어 있는지 확인
• KOBIS API 인증키가 올바른지 확인
• 인터넷 연결 확인
• KOBIS API 서버 상태 확인
"""
    )

    st.code(result["error"])

    st.stop()


# ==================================================
# 8. DataFrame 만들기
# ==================================================

df = pd.DataFrame(
    result["movies"]
)


# ==================================================
# 9. 숫자 데이터 변환
# ==================================================

number_columns = [
    "rank",
    "rankInten",
    "audiCnt",
    "audiAcc",
    "scrnCnt",
    "showCnt"
]

for column in number_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0)


# 순위순 정렬
df = df.sort_values(
    "rank",
    ascending=True
).reset_index(drop=True)


# ==================================================
# 10. 선택한 날짜 표시
# ==================================================

st.subheader(
    f"📅 {display_date} 박스오피스"
)


# ==================================================
# 11. 1위 영화 정보
# ==================================================

first_movie = df.iloc[0]

first_movie_name = first_movie["movieNm"]

first_audience = int(
    first_movie["audiCnt"]
)

first_acc_audience = int(
    first_movie["audiAcc"]
)


# ==================================================
# 12. 1위 영화 카드
# ==================================================

st.subheader("🏆 1위 영화")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🎬 영화",
        first_movie_name
    )


with col2:

    st.metric(
        "👥 해당 날짜 관객수",
        f"{first_audience:,}명"
    )


with col3:

    st.metric(
        "📊 누적 관객수",
        f"{first_acc_audience:,}명"
    )


# ==================================================
# 13. 관객수 상위 5편 하트 그래프
# ==================================================

st.subheader("💗 관객수 상위 5편")

st.caption(
    "관객수가 많을수록 하트가 크게 표시됩니다."
)


top5 = (
    df.sort_values(
        "audiCnt",
        ascending=False
    )
    .head(5)
    .copy()
)


max_audience = int(
    top5["audiCnt"].max()
)

min_audience = int(
    top5["audiCnt"].min()
)


# ==================================================
# 14. 하트 표시
# ==================================================

for _, movie in top5.iterrows():

    movie_name = movie["movieNm"]

    audience = int(
        movie["audiCnt"]
    )


    if max_audience == min_audience:

        heart_size = 70

    else:

        ratio = (
            (audience - min_audience)
            / (max_audience - min_audience)
        )

        heart_size = int(
            40 + ratio * 70
        )


    st.write(
        f"🎬 **{movie_name}**"
    )


    st.markdown(
        f"""
<span style="
font-size:{heart_size}px;
color:#FFC0CB;
line-height:1;
">
♥
</span>
""",
        unsafe_allow_html=True
    )


    st.caption(
        f"👥 {audience:,}명"
    )

    st.divider()


# ==================================================
# 15. 최근 30일 데이터 가져오기
# ==================================================

st.subheader("💜 날짜별 10위권 일관객 합계")

st.caption(
    "선택한 날짜를 포함한 최근 30일 동안 "
    "그날 10위까지의 관객수를 합산했습니다."
)


# 최근 30일
graph_start_date = selected_date - timedelta(days=29)

graph_end_date = selected_date


# 날짜별 10위권 관객수 저장
daily_sum_data = []

# 영화별 데이터 저장
movie_period_data = []


current_date = graph_start_date


while current_date <= graph_end_date:

    date_string = current_date.strftime("%Y%m%d")

    daily_result = get_boxoffice(date_string)


    # ==================================================
    # 데이터가 정상적으로 있는 경우
    # ==================================================

    if daily_result["success"]:

        movies = daily_result["movies"]

        # 10위까지
        top10_movies = movies[:10]


        # ----------------------------------------------
        # 날짜별 10위권 관객수 합계
        # ----------------------------------------------

        total_audience = 0

        for movie in top10_movies:

            try:

                audience = int(
                    movie.get("audiCnt", 0)
                )

            except (ValueError, TypeError):

                audience = 0


            total_audience += audience


        daily_sum_data.append(
            {
                "날짜": current_date,
                "10위권 관객수": total_audience
            }
        )


        # ----------------------------------------------
        # 영화별 기간 관객수 기록
        # ----------------------------------------------

        for movie in top10_movies:

            movie_name = movie.get(
                "movieNm",
                "알 수 없는 영화"
            )

            movie_code = movie.get(
                "movieCd",
                movie_name
            )


            try:

                audience = int(
                    movie.get("audiCnt", 0)
                )

            except (ValueError, TypeError):

                audience = 0


            movie_period_data.append(
                {
                    "movieCd": movie_code,
                    "movieNm": movie_name,
                    "audiCnt": audience,
                    "날짜": current_date
                }
            )


    # ==================================================
    # 데이터가 없는 경우
    # ==================================================

    else:

        daily_sum_data.append(
            {
                "날짜": current_date,
                "10위권 관객수": None
            }
        )


    current_date += timedelta(days=1)


# ==================================================
# 16. 세 번째 그래프 DataFrame
# ==================================================

daily_df = pd.DataFrame(
    daily_sum_data
)

daily_df = daily_df.sort_values(
    "날짜"
).reset_index(drop=True)


# ==================================================
# 17. 10위권 관객수가 가장 많았던 날 TOP 3
# ==================================================

ranking_df = daily_df.dropna(
    subset=["10위권 관객수"]
).copy()


ranking_df = ranking_df.sort_values(
    "10위권 관객수",
    ascending=False
).head(3)


# ==================================================
# 18. TOP 3 날짜 표시
# ==================================================

if not ranking_df.empty:

    st.markdown(
        "### 🏆 10위권 관객수가 가장 많았던 날"
    )

    top_columns = st.columns(
        len(ranking_df)
    )


    for i, (_, row) in enumerate(
        ranking_df.iterrows()
    ):

        date_text = row["날짜"].strftime(
            "%Y년 %m월 %d일"
        )

        total = int(
            row["10위권 관객수"]
        )


        with top_columns[i]:

            st.metric(
                f"🏆 {i + 1}위",
                date_text,
                f"{total:,}명"
            )


# ==================================================
# 19. 세 번째 그래프 - 연보라색 영역 그래프
# ==================================================

area_chart = (
    alt.Chart(daily_df)
    .mark_area(
        line=True,
        point=True,
        color="#C8A2C8",
        opacity=0.45
    )
    .encode(

        x=alt.X(
            "날짜:T",
            title="날짜",
            axis=alt.Axis(
                format="%m/%d"
            )
        ),

        y=alt.Y(
            "10위권 관객수:Q",
            title="10위권 관객수 합계",
            axis=alt.Axis(
                format=","
            )
        ),

        tooltip=[
            alt.Tooltip(
                "날짜:T",
                title="날짜",
                format="%Y년 %m월 %d일"
            ),
            alt.Tooltip(
                "10위권 관객수:Q",
                title="10위권 관객수",
                format=","
            )
        ]
    )
)


# ==================================================
# 20. TOP 3 표시
# ==================================================

if not ranking_df.empty:

    top3_points = (
        alt.Chart(ranking_df)
        .mark_point(
            filled=True,
            size=120,
            color="#A77BCA"
        )
        .encode(

            x="날짜:T",

            y="10위권 관객수:Q",

            tooltip=[
                alt.Tooltip(
                    "날짜:T",
                    title="날짜",
                    format="%Y년 %m월 %d일"
                ),
                alt.Tooltip(
                    "10위권 관객수:Q",
                    title="10위권 관객수",
                    format=","
                )
            ]
        )
    )


    top3_text = (
        alt.Chart(ranking_df)
        .mark_text(
            dy=-18,
            fontSize=13,
            fontWeight="bold",
            color="#8E5AAE"
        )
        .encode(

            x="날짜:T",

            y="10위권 관객수:Q",

            text=alt.Text(
                "날짜:T",
                format="%m/%d"
            )
        )
    )


    final_chart = (
        area_chart
        + top3_points
        + top3_text
    )

else:

    final_chart = area_chart


st.altair_chart(
    final_chart,
    use_container_width=True
)


# ==================================================
# 21. 네 번째 그래프
# 기간별 영화 관객수 TOP 10
# ==================================================

st.subheader("🎞️ 기간별 영화 관객수 TOP 10")

st.caption(
    "선택한 날짜를 포함한 최근 30일 동안 "
    "10위권에 있었던 영화들의 일관객수를 모두 합산했습니다."
)


# ==================================================
# 22. 영화별 관객수 합계 계산
# ==================================================

if movie_period_data:

    movie_df = pd.DataFrame(
        movie_period_data
    )


    # ----------------------------------------------
    # 영화별 관객수 합계
    # ----------------------------------------------

    movie_total_df = (
        movie_df
        .groupby(
            ["movieCd", "movieNm"],
            as_index=False
        )
        .agg(
            기간관객수=("audiCnt", "sum"),
            톱10일수=("날짜", "count")
        )
    )


    # ----------------------------------------------
    # 관객수가 많은 순서로 TOP 10
    # ----------------------------------------------

    movie_total_df = (
        movie_total_df
        .sort_values(
            "기간관객수",
            ascending=False
        )
        .head(10)
        .copy()
    )


    # 차트에 표시할 영화 순서
    movie_order = (
        movie_total_df
        .sort_values(
            "기간관객수",
            ascending=True
        )["movieNm"]
        .tolist()
    )


    # ==================================================
    # 23. 네 번째 그래프 - 가로 막대그래프
    # ==================================================

    movie_chart = (
        alt.Chart(movie_total_df)
        .mark_bar(
            color="#FFC0CB"
        )
        .encode(

            # 영화 이름
            y=alt.Y(
                "movieNm:N",
                title="영화",
                sort=movie_order,
                axis=alt.Axis(
                    labelLimit=250
                )
            ),

            # 기간 관객수
            x=alt.X(
                "기간관객수:Q",
                title="기간 관객수",
                axis=alt.Axis(
                    format=","
                )
            ),

            # 마우스를 올렸을 때 표시
            tooltip=[
                alt.Tooltip(
                    "movieNm:N",
                    title="영화"
                ),
                alt.Tooltip(
                    "기간관객수:Q",
                    title="기간 관객수",
                    format=","
                ),
                alt.Tooltip(
                    "톱10일수:Q",
                    title="10위권에 든 날수",
                    format="d"
                )
            ]
        )
        .properties(
            height=450
        )
    )


    st.altair_chart(
        movie_chart,
        use_container_width=True
    )


else:

    st.info(
        "해당 기간에는 10위권 영화 데이터가 없습니다."
    )


# ==================================================
# 24. 전체 박스오피스 표
# ==================================================

st.subheader("🎞️ 전체 박스오피스")


table_df = df[
    [
        "rank",
        "movieNm",
        "openDt",
        "rankInten",
        "audiCnt",
        "audiAcc",
        "scrnCnt"
    ]
].copy()


# ==================================================
# 25. 누적관객 100만 명 초과 → 트로피
# ==================================================

def add_trophy(row):

    movie_name = str(
        row["movieNm"]
    )

    accumulated = int(
        row["audiAcc"]
    )

    if accumulated > 1_000_000:

        return f"🏆 {movie_name}"

    return movie_name


table_df["movieNm"] = table_df.apply(
    add_trophy,
    axis=1
)


# ==================================================
# 26. 순위 증감 표시
# ==================================================

def make_rank_change(value):

    value = int(value)

    # 양수 = 순위 상승
    if value > 0:

        return f"🔴 ▲ {value}"

    # 음수 = 순위 하락
    elif value < 0:

        return f"🔵 ▼ {abs(value)}"

    # 변화 없음
    else:

        return "━"


table_df["rankInten"] = (
    table_df["rankInten"]
    .apply(make_rank_change)
)


# ==================================================
# 27. 표 컬럼 이름 변경
# ==================================================

table_df.columns = [
    "순위",
    "영화명",
    "개봉일",
    "순위 증감",
    "관객수",
    "누적관객",
    "스크린수"
]


# ==================================================
# 28. 숫자에 쉼표
# ==================================================

table_df["관객수"] = table_df[
    "관객수"
].map(
    lambda x: f"{int(x):,}"
)

table_df["누적관객"] = table_df[
    "누적관객"
].map(
    lambda x: f"{int(x):,}"
)

table_df["스크린수"] = table_df[
    "스크린수"
].map(
    lambda x: f"{int(x):,}"
)


# ==================================================
# 29. 표 출력
# ==================================================

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# 30. 출처
# ==================================================

st.caption(
    "※ 데이터 출처: 영화관입장권통합전산망(KOBIS) "
    "일일 박스오피스 API"
)
