import json
import streamlit as st
from difflib import SequenceMatcher

# تحميل قاعدة البيانات
with open("fiqh_masail_expanded.json", "r", encoding="utf-8") as f:
    data = json.load(f)

st.title("📚 المساعد الفقهي الذكي")

# إدخال المستخدم
user_input = st.text_input("✍️ اكتب سؤالك الفقهي:")

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
        st.markdown(f"### ✅ المسألة الأقرب: {best_match['المسألة']}")
        st.markdown(f"**🗂️ الموضوع: {best_match['الموضوع']}**")
        for madhhab, content in best_match["الأقوال"].items():
            st.markdown(f"#### 📌 {madhhab}")
            st.write(f"🔹 الحكم: {content['الحكم']}")
            st.write(f"📚 المرجع: {content['المرجع']}")
            st.markdown("---")
    else:
        st.warning("❌ لم يتم العثور على مسألة مشابهة في قاعدة البيانات.")
