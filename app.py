import streamlit as st
import requests
import os

# ==================== 從檔案讀取 API Key ====================
def load_api_key(filepath="api_key.txt"):
    """從指定檔案讀取 API Key"""
    try:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                key = f.read().strip()
                if key:
                    return key
        # 如果檔案不存在，嘗試從環境變數或 secrets 讀取（方便部署）
        return os.getenv("WEATHER_API_KEY") or st.secrets.get("WEATHER_API_KEY", "")
    except Exception as e:
        st.error(f"讀取 API Key 失敗：{e}")
        return ""

API_KEY = load_api_key()

st.set_page_config(page_title="即時天氣卡片", page_icon="🌤️", layout="centered")

st.title("🌤️ 即時天氣卡片")
st.caption("Python + Streamlit 版本")

city = st.text_input("輸入城市英文名稱", value="Macau")

if st.button("查詢", type="primary") or city:
    if not API_KEY:
        st.error("⚠️ 找不到 API Key，請確認 api_key.txt 是否存在")
        st.info("申請免費 Key：https://www.weatherapi.com/signup")
    elif not city.strip():
        st.warning("請輸入城市名稱")
    else:
        try:
            with st.spinner("正在查詢..."):
                url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city.strip()}"
                resp = requests.get(url, timeout=10)
                data = resp.json()

            if "error" in data:
                st.error(data["error"]["message"])
            else:
                current = data["current"]
                location = data["location"]
                temp = current["temp_c"]

                # 動態背景
                if temp >= 30:
                    bg = "linear-gradient(135deg, #ff512f, #dd2476)"
                elif temp >= 20:
                    bg = "linear-gradient(135deg, #fbc2eb, #a6c1ee)"
                elif temp >= 10:
                    bg = "linear-gradient(135deg, #89f7fe, #66a6ff)"
                else:
                    bg = "linear-gradient(135deg, #00c6ff, #0072ff)"

                st.markdown(
                    f"<style>.stApp {{background: {bg}; background-attachment: fixed;}}</style>",
                    unsafe_allow_html=True,
                )

                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image("https:" + current["condition"]["icon"], width=110)
                with col2:
                    st.subheader(f"{location['name']}, {location['country']}")
                    st.metric("溫度", f"{temp}°C")
                    st.write(current["condition"]["text"])

                st.divider()
                c1, c2, c3 = st.columns(3)
                c1.metric("濕度", f"{current['humidity']}%")
                c2.metric("體感", f"{current['feelslike_c']}°C")
                c3.metric("風速", f"{current['wind_kph']} km/h")

        except Exception as e:
            st.error(f"查詢失敗：{e}")
