import streamlit as st
import requests
import os

# ==================== 設定 ====================
# 優先從 Streamlit Secrets 或環境變數讀取 API Key
# 在 Streamlit Cloud 部署時，可在 Settings → Secrets 設定
API_KEY = os.getenv("WEATHER_API_KEY") or st.secrets.get("WEATHER_API_KEY", "")

st.set_page_config(
    page_title="即時天氣卡片",
    page_icon="🌤️",
    layout="centered"
)

# ==================== 標題 ====================
st.title("🌤️ 即時天氣卡片")
st.caption("Python + Streamlit 版本｜前端呼叫第三方 API + 動態樣式")

# ==================== 輸入區 ====================
city = st.text_input(
    "輸入城市英文名稱",
    value="Macau",
    placeholder="例如：Macau、Taipei、Tokyo、London"
)

col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    search = st.button("查詢", type="primary")

# ==================== 查詢邏輯 ====================
if search or (city and city != "Macau"):  # 預設城市也可自動查一次
    if not API_KEY:
        st.error("⚠️ 請先設定 WeatherAPI Key（環境變數或 Streamlit Secrets）")
        st.info("申請免費 Key：https://www.weatherapi.com/signup")
    elif not city.strip():
        st.warning("請輸入城市名稱")
    else:
        try:
            with st.spinner("正在查詢天氣..."):
                url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city.strip()}"
                response = requests.get(url, timeout=10)
                data = response.json()

            if "error" in data:
                st.error(f"查詢失敗：{data['error']['message']}")
            else:
                current = data["current"]
                location = data["location"]
                temp = current["temp_c"]

                # ========== 根據溫度動態改變背景 ==========
                if temp >= 30:
                    bg = "linear-gradient(135deg, #ff512f, #dd2476)"
                    theme_text = "酷熱"
                elif temp >= 20:
                    bg = "linear-gradient(135deg, #fbc2eb, #a6c1ee)"
                    theme_text = "舒適"
                elif temp >= 10:
                    bg = "linear-gradient(135deg, #89f7fe, #66a6ff)"
                    theme_text = "偏涼"
                else:
                    bg = "linear-gradient(135deg, #00c6ff, #0072ff)"
                    theme_text = "寒冷"

                st.markdown(
                    f"""
                    <style>
                    .stApp {{
                        background: {bg};
                        background-attachment: fixed;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                # ========== 天氣卡片 ==========
                st.success(f"目前主題：{theme_text}（{temp}°C）")

                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image("https:" + current["condition"]["icon"], width=120)
                with col2:
                    st.subheader(f"{location['name']}, {location['country']}")
                    st.metric("溫度", f"{temp}°C")
                    st.write(f"**{current['condition']['text']}**")

                st.divider()

                c1, c2, c3 = st.columns(3)
                c1.metric("濕度", f"{current['humidity']}%")
                c2.metric("體感溫度", f"{current['feelslike_c']}°C")
                c3.metric("風速", f"{current['wind_kph']} km/h")

        except Exception as e:
            st.error(f"發生錯誤：{e}")

# ==================== 頁尾說明 ====================
st.divider()
st.caption("教學示範用｜資料來源：WeatherAPI.com")
