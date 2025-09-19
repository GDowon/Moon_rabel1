import streamlit as st
import pandas as pd
import altair as alt

# ----------------------------------------------------
# 깃허브에서 CSV 파일을 불러오는 함수
# ----------------------------------------------------
@st.cache_data
def load_data():
    """
    GitHub raw URL에서 CSV 파일을 불러옵니다.
    """
    GITHUB_RAW_URL = "https://raw.githubusercontent.com/GDowon/Moon_rabel1/main/%EB%B6%84%EB%A5%98%EB%B2%88%ED%98%B8.csv"
    
    try:
        df = pd.read_csv(GITHUB_RAW_URL, encoding='cp949')
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

# Streamlit 앱의 제목 설정
st.title("분류번호.csv 데이터 시각화")

# CSV 파일 불러오기
df = load_data()

if not df.empty:
    # '문' 문자를 제거하고 숫자 타입으로 변환
    df['90_value'] = pd.to_numeric(df['90'].astype(str).str.replace('문', ''), errors='coerce')
    
    # 데이터 타입을 구분하는 새로운 컬럼 생성
    df['type'] = df['90'].apply(lambda x: '문' if '문' in str(x) else '일반')
    
    # '문'이 붙은 데이터와 일반 데이터로 분리하고, 라벨 위치를 계산
    df_moon = df[df['90'].astype(str).str.startswith('문')].copy()
    df_moon['label_position'] = (df_moon.reset_index().index % 2)
    df_moon['y_label_pos'] = df_moon['label_position'].map({0: 35, 1: 65})
    
    df_general = df[~df['90'].astype(str).str.startswith('문')].copy()
    df_general['label_position'] = (df_general.reset_index().index % 2)
    df_general['y_label_pos'] = df_general['label_position'].map({0: 35, 1: 65})
    
    df_clean = df.dropna(subset=['90_value']).copy()
    df_clean['label_position'] = (df_clean.reset_index().index % 2)
    df_clean['y_label_pos'] = df_clean['label_position'].map({0: 35, 1: 65})

    # ----------------------------------------------------
    # 1. '문'이 붙은 값만 시각화
    # ----------------------------------------------------
    st.write("---")
    st.subheader("1. '문' 데이터 시각화")
    
    points_moon = alt.Chart(df_moon).mark_point(
        opacity=0.5,
        filled=True,
        size=100
    ).encode(
        x=alt.X('90_value', axis=alt.Axis(title='값 (90 컬럼)', grid=True), scale=alt.Scale(domain=(0, 1000))),
        y=alt.value(50),
        tooltip=['245', alt.Tooltip('90_value', title='90 컬럼 값')]
    )

    text_labels_moon = alt.Chart(df_moon).mark_text(
        align='center'
    ).encode(
        x=alt.X('90_value', scale=alt.Scale(domain=(0, 1000))),
        y=alt.Y('y_label_pos', axis=None),
        text=alt.Text('90_value', format='.1f'),
    )
    
    chart_moon = (points_moon + text_labels_moon).properties(
        title="수평선 상의 '문' 데이터",
        width=700,
        height=200
    ).interactive()

    st.altair_chart(chart_moon, use_container_width=True)

    # ----------------------------------------------------
    # 2. 숫자만 있는 값 시각화
    # ----------------------------------------------------
    st.write("---")
    st.subheader("2. 일반 데이터 시각화")

    points_general = alt.Chart(df_general).mark_point(
        opacity=0.5,
        filled=True,
        size=100
    ).encode(
        x=alt.X('90_value', axis=alt.Axis(title='값 (90 컬럼)', grid=True), scale=alt.Scale(domain=(0, 1000))),
        y=alt.value(50),
        tooltip=['245', alt.Tooltip('90_value', title='90 컬럼 값')]
    )
    
    text_labels_general = alt.Chart(df_general).mark_text(
        align='center'
    ).encode(
        x=alt.X('90_value', scale=alt.Scale(domain=(0, 1000))),
        y=alt.Y('y_label_pos', axis=None),
        text=alt.Text('90_value', format='.1f'),
    )
    
    chart_general = (points_general + text_labels_general).properties(
        title="수평선 상의 일반 데이터",
        width=700,
        height=200
    ).interactive()

    st.altair_chart(chart_general, use_container_width=True)

    # ----------------------------------------------------
    # 3. 모든 데이터 시각화 (색상 구분)
    # ----------------------------------------------------
    st.write("---")
    st.subheader("3. 전체 데이터 시각화")

    points_combined = alt.Chart(df_clean).mark_point(
        opacity=0.5,
        filled=True,
        size=100
    ).encode(
        x=alt.X('90_value', axis=alt.Axis(title='값 (90 컬럼)', grid=True), scale=alt.Scale(domain=(0, 1000))),
        y=alt.value(50),
        color=alt.Color('type', scale=alt.Scale(domain=['문', '일반'], range=['blue', 'yellow'])),
        tooltip=['245', alt.Tooltip('90_value', title='90 컬럼 값')]
    )

    text_labels_combined = alt.Chart(df_clean).mark_text(
        align='center'
    ).encode(
        x=alt.X('90_value', scale=alt.Scale(domain=(0, 1000))),
        y=alt.Y('y_label_pos', axis=None),
        text=alt.Text('90_value', format='.1f'),
        color=alt.Color('type', scale=alt.Scale(domain=['문', '일반'], range=['blue', 'yellow'])),
    )

    chart_combined = (points_combined + text_labels_combined).properties(
        title="수평선 상의 전체 데이터 (색상 구분)",
        width=700,
        height=200
    ).interactive()

    st.altair_chart(chart_combined, use_container_width=True)
    
else:
    st.write("데이터를 불러오지 못해 차트를 생성할 수 없습니다. GitHub URL을 확인해주세요.")
