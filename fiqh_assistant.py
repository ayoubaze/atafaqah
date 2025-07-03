
import json
import streamlit as st

# تحميل البيانات
with open("fiqh_masail_expanded.json", "r", encoding="utf-8") as f:
    data = json.load(f)

st.title("المساعد الفقهي الذكي - مجاني")

# إدخال السؤال
user_input = st.text_input("اكتب مسألتك الفقهية:")

if user_input:
    found = False
    for item in data:
        if user_input.strip() in item["المسألة"]:
            found = True
            st.markdown(f"### 🧾 المسألة: {item['المسألة']}")
            for madhhab, content in item["الأقوال"].items():
                st.markdown(f"**{madhhab}**")
                st.write(f"🔹 الحكم: {content['الحكم']}")
                st.write(f"📚 المرجع: {content['المرجع']}")
                st.markdown("---")
            break
    if not found:
        st.warning("❌ لم يتم العثور على هذه المسألة في قاعدة البيانات.")
