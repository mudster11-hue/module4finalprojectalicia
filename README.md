# 🎨 AI-Powered Image Editing Platform

A lightweight AI image editor built with Streamlit, Python, and OpenRouter (Gemini). Users can upload images, apply natural language edits, and track version history in real-time.

---

## ⚡ Features
* **Natural Language Editing:** Interpret edit instructions using GenAI vision models.
* **Real Image Processing:** Transform images (black & white, blur, brightness, contrast) using natural language or quick presets.
* **Version History Timeline:** Track all edits sequentially with timestamps and thumbnails.

---

## 🚀 How to Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt

```

### 2. Set Up API Key

* Create a `.env` file in the main folder.
* Add your OpenRouter API key:
```text
OPENROUTER_API_KEY=your_openrouter_api_key_here

```



### 3. Start the App

```bash
streamlit run app.py

```

---

## 📂 Project Structure

* `app.py` - Main Streamlit UI and version history logic.
* `services/api_handler.py` - OpenRouter API integration and PIL image transformations.
* `requirements.txt` - Required Python packages.
* `.env` - Environment variables (kept private).

```

```
