import streamlit as st
import pandas as pd
import altair as alt

# Streamlit 앱의 제목 설정
st.title("분류번호.csv 데이터 시각화")

# CSV 파일 불러오기 및 데이터 전처리
try:
    # 'cp949' 인코딩을 사용하여 파일 읽기
    df = pd.read_csv('분류번호.csv', encoding='cp949')

    # '90' 컬럼의 데이터 전처리 및 숫자형으로 변환
    df['90_value'] = pd.to_numeric(df['90'].astype(str).str.replace('문', ''), errors='coerce')
    
    # '문'이 있는 데이터와 없는 데이터 분리
    df_moon = df[df['90'].astype(str).str.startswith('문')].copy()
    df_general = df[~df['90'].astype(str).str.startswith('문')].copy()

    # 모든 데이터를 위한 'type' 컬럼 추가 및 NaN 값 제거
    df['type'] = df['90'].apply(lambda x: '문' if '문' in str(x) else '일반')
    df_clean = df.dropna(subset=['90_value'])
    
    # ----------------------------------------------------
    # 1. '문'이 붙은 값만 시각화
    # ----------------------------------------------------
    st.write("---")
    st.subheader("1. '문' 데이터 시각화")
    chart_moon = alt.Chart(df_moon).mark_point(
        opacity=0.5,
        filled=True,
        size=100
    ).encode(
        x=alt.X('90_value', axis=alt.Axis(title='값 (90 컬럼)', grid=True), scale=alt.Scale(domain=(0, 1000))),
        y=alt.value(50), # 수평선 위치
        tooltip=['245', alt.Tooltip('90_value', title='90 컬럼 값')]
    ).properties(
        title="수평선 상의 '문' 데이터"
    ).interactive()

    st.altair_chart(chart_moon, use_container_width=True)

    # ----------------------------------------------------
    # 2. 숫자만 있는 값 시각화
    # ----------------------------------------------------
    st.write("---")
    st.subheader("2. 일반 데이터 시각화")
    chart_general = alt.Chart(df_general).mark_point(
        opacity=0.5,
        filled=True,
        size=100
    ).encode(
        x=alt.X('90_value', axis=alt.Axis(title='값 (90 컬럼)', grid=True), scale=alt.Scale(domain=(0, 1000))),
        y=alt.value(50), # 수평선 위치
        tooltip=['245', alt.Tooltip('90_value', title='90 컬럼 값')]
    ).properties(
        title="수평선 상의 일반 데이터"
    ).interactive()

    st.altair_chart(chart_general, use_container_width=True)

    # ----------------------------------------------------
    # 3. 모든 데이터 시각화 (색상 구분)
    # ----------------------------------------------------
    st.write("---")
    st.subheader("3. 전체 데이터 시각화")
    chart_combined = alt.Chart(df_clean).mark_point(
        opacity=0.5,
        filled=True,
        size=100
    ).encode(
        x=alt.X('90_value', axis=alt.Axis(title='값 (90 컬럼)', grid=True), scale=alt.Scale(domain=(0, 1000))),
        y=alt.value(50), # 수평선 위치
        color=alt.Color('type', scale=alt.Scale(domain=['문', '일반'], range=['blue', 'yellow'])),
        tooltip=['245', alt.Tooltip('90_value', title='90 컬럼 값')]
    ).properties(
        title="수평선 상의 전체 데이터 (색상 구분)"
    ).interactive()

    st.altair_chart(chart_combined, use_container_width=True)

except FileNotFoundError:
    st.error("오류: '분류번호.csv' 파일을 찾을 수 없습니다. 파일이 올바른 위치에 있는지 확인해주세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")