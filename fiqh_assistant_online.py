import streamlit as st
import json
from difflib import SequenceMatcher
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI

# إعداد الصفحة
st.set_page_config(page_title="المساعد الفقهي الذكي", layout="wide")
st.title("🕌 المساعد الفقهي الذكي - بحث داخلي + عبر الإنترنت")

# تحميل قاعدة البيانات
with open("fiqh_masail_expanded.json", "r", encoding="utf-8") as f:
    masail_data = json.load(f)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def search_in_json(query):
    best_match = None
    highest_score = 0.0
    for item in masail_data:
        score = similar(query.strip(), item["المسألة"])
        if score > highest_score:
            highest_score = score
            best_match = item
    return best_match if highest_score > 0.5 else None

# أدوات الذكاء الاصطناعي
search = DuckDuckGoSearchRun()
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")  # يتطلب مفتاح OpenAI API

tools = [
    Tool(name="Web Search", func=search.run, description="البحث عن معلومات فقهية من مواقع موثوقة")
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=False)

# واجهة الإدخال
query = st.text_input("✍️ اكتب سؤالك الفقهي:")

if query:
    st.markdown("🔍 **جاري البحث...**")

    # 1. البحث في JSON المحلي
    json_result = search_in_json(query)
    if json_result:
        st.success(f"✅ وُجدت مسألة مشابهة في قاعدة البيانات: {json_result['المسألة']}")
        st.markdown(f"**📚 الموضوع: {json_result['الموضوع']}**")
        for madhhab, content in json_result["الأقوال"].items():
            st.markdown(f"### {madhhab}")
            st.write(f"🔹 الحكم: {content['الحكم']}")
            st.write(f"📘 المرجع: {content['المرجع']}")
            st.markdown("---")

    # 2. البحث عبر الإنترنت
    st.markdown("🌐 **جارٍ البحث في الإنترنت...**")
    result = agent.run(f"أجب عن هذا السؤال الفقهي من مصادر موثوقة: {query}")
    st.markdown("### 🌐 نتيجة البحث من الإنترنت:")
    st.info(result)

# توقيع
st.markdown("---")
st.markdown("📝 تم إنشاء هذه الواجهة بالاستعانة بالذكاء الاصطناعي ChatGPT، وهي صدقة جارية من **عبدون أيوب**.")
