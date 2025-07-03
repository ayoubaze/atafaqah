import json
import streamlit as st
from difflib import SequenceMatcher
import requests

# ---------------------------
# تحميل بيانات المسائل الفقهية
# ---------------------------
with open("fiqh_masail_expanded.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ---------------------------
# إعداد مواقيت الصلاة والتاريخ
# ---------------------------
def get_prayer_times(city="Algiers", country="Algeria"):
    url = f"https://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=2"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["data"]
        return data["timings"], data["date"]["hijri"], data["date"]["gregorian"]
    else:
        return None, None, None

# ---------------------------
# واجهة Streamlit
# ---------------------------
st.set_page_config(page_title="المساعد الفقهي الذكي", layout="wide")
st.title("🕌 المساعد الفقهي الذكي + مواقيت الصلاة")

# ---------------------------
# الشريط الجانبي: مواقيت الصلاة
# ---------------------------
st.sidebar.title("🕐 مواقيت الصلاة")

city = st.sidebar.selectbox("اختر المدينة", ["Algiers", "Cairo", "Makkah", "Tunis", "Casablanca"])
country_map = {
    "Algiers": "Algeria",
    "Cairo": "Egypt",
    "Makkah": "Saudi Arabia",
    "Tunis": "Tunisia",
    "Casablanca": "Morocco"
}

timings, hijri, gregorian = get_prayer_times(city, country_map[city])

if timings:
    st.sidebar.markdown(f"📅 التاريخ الهجري: {hijri['date']}")
    st.sidebar.markdown(f"📆 التاريخ الميلادي: {gregorian['date']}")
    st.sidebar.markdown("---")
    for prayer, time in timings.items():
        st.sidebar.markdown(f"**{prayer}**: {time}")
else:
    st.sidebar.warning("❌ تعذر جلب مواقيت الصلاة.")

# ---------------------------
# المساعد الفقهي الذكي
# ---------------------------
st.markdown("## 🔍 اسأل عن مسألة فقهية")

user_input = st.text_input("✍️ اكتب سؤالك:")

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

if user_input:
    best_match = None
    highest_score = 0.0

    for item in data:
        score = similar(user_input.strip(), item["المسألة"])
        if score > highest_score:
            highest_score = score
            best_match = item

    if best_match and highest_score > 0.5:
        st.success(f"✅ أقرب مسألة: {best_match['المسألة']}")
        st.markdown(f"**📚 الموضوع: {best_match['الموضوع']}**")
        for madhhab, content in best_match["الأقوال"].items():
            st.markdown(f"### {madhhab}")
            st.write(f"🔹 الحكم: {content['الحكم']}")
            st.write(f"📘 المرجع: {content['المرجع']}")
            st.markdown("---")
    else:
        st.warning("❌ لم يتم العثور على مسألة مشابهة.")
