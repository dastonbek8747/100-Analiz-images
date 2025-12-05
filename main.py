import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image
import os
from dotenv import load_dotenv
import time

# .env fayldan o'qish
load_dotenv()

# Sahifa konfiguratsiyasi
st.set_page_config(
    page_title="AI Rasm Tahlilchisi",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stillar - Zamonaviy dizayn
st.markdown("""
    <style>
    /* Umumiy fon */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Asosiy kontent */
    .main {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #f1f5f9;
    }

    section[data-testid="stSidebar"] h2 {
        color: #fbbf24 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    section[data-testid="stSidebar"] h3 {
        color: #fcd34d !important;
    }

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stTextInput label,
    section[data-testid="stSidebar"] .stCheckbox label {
        color: #e2e8f0 !important;
        font-weight: 600;
    }

    /* Tugmalar */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    /* Input maydonlari */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e7ff;
        padding: 0.75rem;
        background: white;
    }

    /* File uploader */
    .stFileUploader {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0e7ff 100%);
        border-radius: 15px;
        padding: 2rem;
        border: 2px dashed #818cf8;
    }

    /* Natija kartasi */
    .result-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.5s ease;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Yuz tanish kartasi */
    .person-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #f59e0b;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
        animation: slideIn 0.5s ease 0.2s both;
    }

    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }

    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #3b82f6;
    }

    /* Success box */
    .success-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        border-left: 4px solid #34d399;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        color: white;
        font-weight: 600;
    }

    /* Warning box */
    .warning-box {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        border-left: 4px solid #fbbf24;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        color: white;
        font-weight: 600;
    }

    .warning-box small {
        color: #fef3c7;
        display: block;
        margin-top: 0.5rem;
    }

    /* Sarlavha animatsiya */
    .header-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: fadeIn 1s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Rasm container */
    .image-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        margin: 1rem 0;
    }

    /* Feature card */
    .feature-card {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(245, 158, 11, 0.1) 100%);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border: 2px solid rgba(251, 191, 36, 0.3);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        color: #f1f5f9;
        font-size: 1rem;
        line-height: 1.7;
    }

    .feature-card strong {
        color: #fcd34d;
        font-size: 1.1rem;
    }

    /* Metric style */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #667eea;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)


def search_person_face(description, api_key):
    """Inson yuzini qidirish funksiyasi"""
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        search_prompt = f"""Bu tavsifga mos keladigan mashhur shaxsni aniqlang va qisqa ma'lumot bering:
        {description}

        Agar bu mashhur shaxs bo'lsa:
        - Ismi va familiyasi
        - Kasbi/soha
        - Asosiy yutuqlari

        Agar aniqlay olmasangiz yoki mashhur shaxs bo'lmasa, "Noma'lum shaxs" deb javob bering."""

        payload = {
            "model": "google/gemini-flash-1.5",
            "messages": [{"role": "user", "content": search_prompt}]
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return "Qidiruv amalga oshmadi"

    except Exception as e:
        return f"Xatolik: {str(e)}"


def analyze_image_with_retry(api_key, base64_image, selected_model, max_retries=3):
    """Rasm tahlili - retry mexanizmi bilan"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    models = [
        selected_model,
        "google/gemini-flash-1.5",
        "google/gemini-pro-1.5",
        "anthropic/claude-3-haiku",
        "meta-llama/llama-3.2-11b-vision-instruct:free"
    ]

    for attempt in range(max_retries):
        current_model = models[min(attempt, len(models) - 1)]

        try:
            payload = {
                "model": current_model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Bu rasmni juda batafsil tahlil qiling va o'zbek tilida javob bering:

1. UMUMIY TAVSIF: Rasmda nima tasvirlangan?
2. OB'EKTLAR: Qanday ob'ektlar bor? (ranglar, o'lchamlar, joylashuv)
3. INSON: Agar rasmda odam bo'lsa:
   - Jins (erkak/ayol)
   - Taxminiy yosh
   - Kiyim-kechak (ranglar, stil)
   - Pozitsiya/harakat
   - Yuz ifodasi
   - Soch rangi va uslubi
   - Maxsus belgilar (ko'zoynak, soqol va h.k.)
4. MASHINA: Agar mashina bo'lsa - turi, rangi, modeli, ishlab chiqaruvchi
5. MUHIT: Orqa fon, joy, ob-havo sharoiti

Juda batafsil va aniq javob bering!"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": base64_image}
                            }
                        ]
                    }
                ]
            }

            response = requests.post(url, headers=headers, json=payload, timeout=60)

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "content": data["choices"][0]["message"]["content"],
                    "model": current_model
                }
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    st.warning(f"⏳ {current_model} band. Boshqa model sinab ko'rilmoqda...")
                    time.sleep(2)
                    continue
                else:
                    return {
                        "success": False,
                        "error": "Barcha modellar band. Keyinroq urinib ko'ring."
                    }
            else:
                error_data = response.json()
                return {
                    "success": False,
                    "error": f"Xatolik ({response.status_code}): {error_data}"
                }

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return {"success": False, "error": str(e)}

    return {"success": False, "error": "Barcha urinishlar muvaffaqiyatsiz tugadi"}


# Sarlavha
st.markdown("""
    <div class='header-box'>
        <h1 style='color: white; margin: 0; font-size: 3rem; text-align: center;'>
            🎨 AI Rasm Tahlilchisi
        </h1>
        <p style='color: #e0e7ff; margin-top: 0.5rem; text-align: center; font-size: 1.2rem;'>
            Sun'iy intellekt + Yuz tanish tizimi
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar - Sozlamalar
with st.sidebar:
    st.markdown("<h2 style='color: #fbbf24; text-align: center; font-size: 2rem;'>⚙️ Sozlamalar</h2>",
                unsafe_allow_html=True)
    st.markdown("---")

    # .env dan API kalitni olish
    default_api_key = os.getenv("API_KEY_REF", "")

    # API kalit input
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    api_key = st.text_input(
        "🔑 OpenRouter API Kaliti",
        type="password",
        value=default_api_key,
        placeholder="sk-or-v1-...",
        help="API kalitni https://openrouter.ai/keys dan olishingiz mumkin"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # API kalit holati
    if api_key:
        if api_key == default_api_key and default_api_key:
            st.markdown("""
                <div class='success-box'>
                    <strong>✅ .env fayldan yuklandi!</strong>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class='success-box'>
                    <strong>✅ API kalit kiritildi!</strong>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class='warning-box'>
                <strong>⚠️ API kalit kiritilmagan</strong><br>
                <small>.env faylida API_KEY_REF o'zgaruvchisini sozlang yoki yuqorida kiriting</small>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Model tanlash
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    model_options = {
        "🚀 Google Gemini Flash 2": "google/gemini-2.0-flash-001",
        "💎 Google Gemini Pro 1.5": "google/gemini-1.5-pro",
        "🆓 Llama 3.2 Vision": "meta-llama/llama-3.2-11b-vision-instruct:free",
        "⚡ Claude 3 Haiku": "anthropic/claude-3-haiku"
    }

    selected_model_name = st.selectbox(
        "🤖 Model tanlang",
        options=list(model_options.keys()),
        index=0
    )
    selected_model = model_options[selected_model_name]
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Yuz tanish
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    enable_face_search = st.checkbox(
        "👤 Yuz tanish tizimi",
        value=True,
        help="Rasmda inson bo'lsa, kimligini aniqlashga harakat qiladi"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Qo'llanma
    st.markdown("""
        <div style='color: white;'>
            <h3 style='color: #fbbf24;'>📖 Qo'llanma</h3>
            <div class='feature-card'>
                <strong>1️⃣</strong> API kalitni kiriting<br>
                <strong>2️⃣</strong> Modelni tanlang<br>
                <strong>3️⃣</strong> Rasm yuklang<br>
                <strong>4️⃣</strong> Tahlil qiling<br>
            </div>

            <h3 style='color: #fbbf24; margin-top: 1rem;'>✨ Imkoniyatlar</h3>
            <div class='feature-card'>
                🎯 Batafsil tahlil<br>
                👥 Yuz tanish<br>
                🚗 Ob'ekt aniqlash<br>
                🎨 Rang tahlili<br>
                🔄 Avtomatik retry<br>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Asosiy qism
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📤 Rasm Yuklash")

    uploaded_file = st.file_uploader(
        "Rasmni tanlang",
        type=["png", "jpg", "jpeg", "gif", "webp"],
        help="PNG, JPG, JPEG, GIF, WEBP formatdagi rasmlar"
    )

    if uploaded_file is not None:
        # Rasmni ko'rsatish
        image = Image.open(uploaded_file)
        st.markdown("<div class='image-container'>", unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Rasm ma'lumotlari
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("📐 O'lchami", f"{image.width}×{image.height}")
        with col_b:
            st.metric("🎨 Format", image.format)
        with col_c:
            file_size = len(uploaded_file.getvalue()) / 1024
            st.metric("📦 Hajmi", f"{file_size:.1f} KB")

        st.markdown("<br>", unsafe_allow_html=True)

        # Tahlil qilish tugmasi
        if st.button("🔍 Rasmni Tahlil Qilish", type="primary", use_container_width=True):
            if not api_key:
                st.error("⚠️ Iltimos, API kalitni kiriting!")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    # 1. Rasmni base64 ga o'girish
                    status_text.text("📸 Rasm qayta ishlanmoqda...")
                    progress_bar.progress(20)

                    buffered = BytesIO()
                    image.save(buffered, format=image.format if image.format else "PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    base64_image = f"data:image/{image.format.lower() if image.format else 'png'};base64,{img_str}"

                    # 2. Rasm tahlili
                    status_text.text("🤖 AI tahlil qilmoqda...")
                    progress_bar.progress(40)

                    result = analyze_image_with_retry(api_key, base64_image, selected_model)

                    if result["success"]:
                        analysis_result = result["content"]
                        st.session_state["analysis"] = analysis_result
                        st.session_state["model_used"] = result["model"]

                        progress_bar.progress(70)

                        # 3. Yuz qidirish
                        person_info = None
                        if enable_face_search:
                            if any(word in analysis_result.lower() for word in
                                   ['odam', 'inson', 'erkak', 'ayol', 'shaxs', 'kishi']):
                                status_text.text("👤 Yuz tanilmoqda...")
                                progress_bar.progress(85)

                                person_info = search_person_face(analysis_result, api_key)
                                st.session_state["person_info"] = person_info

                        progress_bar.progress(100)
                        status_text.text("✅ Tahlil yakunlandi!")
                        time.sleep(1)
                        status_text.empty()
                        progress_bar.empty()

                        st.success(f"✅ Muvaffaqiyatli tahlil qilindi!")
                        st.rerun()
                    else:
                        progress_bar.empty()
                        status_text.empty()
                        st.error(f"❌ {result['error']}")

                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Xatolik: {str(e)}")

with col2:
    st.markdown("### 📊 Tahlil Natijalari")

    if "analysis" in st.session_state and st.session_state["analysis"]:
        # AI Tahlili
        st.markdown("""
            <div class='result-card'>
                <h4 style='color: #667eea; margin-top: 0; display: flex; align-items: center;'>
                    🤖 AI Tahlili
                </h4>
        """, unsafe_allow_html=True)

        st.markdown(
            f"<div style='color: #1e293b; line-height: 1.8; font-size: 1.05rem;'>{st.session_state['analysis']}</div>",
            unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Shaxs ma'lumotlari
        if "person_info" in st.session_state and st.session_state["person_info"]:
            st.markdown("""
                <div class='person-card'>
                    <h4 style='color: #92400e; margin-top: 0;'>
                        👤 Shaxs Ma'lumotlari
                    </h4>
            """, unsafe_allow_html=True)

            st.markdown(
                f"<div style='color: #78350f; line-height: 1.8; font-size: 1.05rem;'>{st.session_state['person_info']}</div>",
                unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Model info
        if "model_used" in st.session_state:
            st.markdown(f"""
                <div class='info-box'>
                    <small>🤖 <strong>Ishlatilgan model:</strong> {st.session_state['model_used']}</small>
                </div>
            """, unsafe_allow_html=True)

        # Tozalash tugmasi
        if st.button("🗑️ Natijani Tozalash", use_container_width=True):
            for key in ["analysis", "person_info", "model_used"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    else:
        st.markdown("""
            <div class='info-box' style='text-align: center; padding: 3rem;'>
                <h3 style='color: #3b82f6;'>👈 Boshlash uchun</h3>
                <p style='color: #64748b; margin-top: 1rem;'>
                    Rasm yuklang va tahlil qilish tugmasini bosing
                </p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #64748b;'>
        <p style='font-size: 1.1rem; margin-bottom: 0.5rem;'>
            <strong style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           -webkit-background-clip: text; 
                           -webkit-text-fill-color: transparent;'>
                Powered by AI Vision Models
            </strong> 🚀
        </p>
        <p style='font-size: 0.9rem; color: #94a3b8;'>
            Google Gemini • Claude • Llama Vision
        </p>
    </div>
""", unsafe_allow_html=True)