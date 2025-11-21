import streamlit as st
import pandas as pd
import altair as alt

# -------------------------
# 데이터 불러오기
# -------------------------
df = pd.read_csv("countriesMBTI_16types.csv")  # Streamlit Cloud에서는 같은 폴더에 두면 됨

# -------------------------
# 웹앱 제목
# -------------------------
st.title("🌍 MBTI 유형별 국가 비율 Top 10 / Bottom 10 시각화")

st.markdown("학생의 MBTI 유형을 선택하면, 해당 MBTI 비율이 **가장 높은 10개 국가**와 **가장 낮은 10개 국가**를 확인할 수 있어요!")

# -------------------------
# MBTI 선택 위젯
# -------------------------
mbti_list = [col for col in df.columns if col != "Country"]
selected_mbti = st.selectbox("📌 MBTI 유형을 선택하세요", mbti_list)

# -------------------------
# 선택한 MBTI 기준 정렬
# -------------------------
df_sorted = df.sort_values(selected_mbti, ascending=False)

# 가장 높은 10개
top10 = df_sorted.head(10)

# 가장 낮은 10개
bottom10 = df_sorted.tail(10).sort_values(selected_mbti, ascending=True)

# -------------------------
# Altair 그래프 함수
# -------------------------
def make_bar_chart(data, mbti, title):
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(mbti + ":Q", title=f"{mbti} 비율"),
            y=alt.Y("Country:N", sort="-x", title="국가"),
            tooltip=["Country", mbti]
        )
        .properties(
            title=title,
            width=650,
            height=350
        )
        .interactive()
    )
    return chart

# -------------------------
# 그래프 출력
# -------------------------

st.subheader("🔥 MBTI 비율이 가장 높은 10개 국가")
st.altair_chart(make_bar_chart(top10, selected_mbti, f"{selected_mbti} Highest 10 Countries"), use_container_width=True)

st.subheader("❄️ MBTI 비율이 가장 낮은 10개 국가")
st.altair_chart(make_bar_chart(bottom10, selected_mbti, f"{selected_mbti} Lowest 10 Countries"), use_container_width=True)
