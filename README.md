# 🖼 AI Rasm Tahlilchisi (100-Analiz-images)

**OpenRouter** API orqali rasm yuklab, uni sun'iy intellekt yordamida tahlil qiluvchi Streamlit ilovasi.

---

## ✨ Imkoniyatlar

- 📤 **Rasm yuklash** (drag & drop)
- 🤖 **AI tahlili:** rasmda nima borligini tavsiflash
- 🔗 **OpenRouter** ko'p modelli kirish nuqtasi
- ⚡ **Tez javob** (bulut orqali)

---

## 🛠 Texnologiyalar

| Texnologiya | Maqsad |
|---|---|
| **Python 3.10+** | Asosiy til |
| **Streamlit** | Veb-interfeys |
| **requests** | OpenRouter API |
| **Pillow** | Rasm bilan ishlash |
| **python-dotenv** | Muhit o'zgaruvchilari |

---

## ⚙️ O'rnatish

```bash
git clone https://github.com/dastonbek8747/100-Analiz-images.git
cd 100-Analiz-images
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Kalitni sozlang:

```bash
cp .env.example .env
```

```env
API_KEY_REF=sk-or-v1-...
```

> 🔒 `.env` git'ga qo'shilmaydi. **Kalitni hech qachon kodga yozmang.**

---

## ▶️ Ishga tushirish

```bash
streamlit run main.py
```

---

## 📁 Loyiha tuzilishi

```
100-Analiz-images/
├── main.py            # Streamlit ilova
├── test.py            # OpenRouter API namunasi
├── requirements.txt
├── tests/
└── .env.example
```

---

## 📄 Litsenziya

Litsenziya ko'rsatilmagan.
