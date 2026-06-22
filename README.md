# ⚡ Liquidity Engine
**AI-Powered Collateral Valuation & Risk Assessment Dashboard**

Liquidity Engine is a modern, full-stack real estate valuation platform designed for banks and NBFCs. It uses a **Hybrid AI Architecture** combining deterministic Python mathematical modeling with the reasoning capabilities of Large Language Models (LLMs) to predict Market Value, Distress Value, and Liquidity Scores (RPI).

---

## ✨ Key Features
* **🧠 Hybrid AI Architecture:** Uses Python for strict mathematical grounding (base price calculation & age depreciation) and Groq (Llama-3) for nuanced risk and location intelligence.
* **🕵️ Chain of Thought (CoT) Reasoning:** Provides full transparency. The dashboard displays the AI's step-by-step mathematical reasoning before showing the final valuation, completely eliminating "AI hallucinations."
* **📊 Data Grounding:** Implements a localized mock database for real-time area rates (e.g., Lucknow's Circle/Market Rates) to anchor the AI's predictions in reality.
* **📉 Distress Value Calculation:** Accurately calculates "forced sale" values, separating land appreciation from building depreciation.
* **🎛️ Granular Inputs:** Supports specific data points like Property Sub-type (Flat/Plot/Villa), Legal Status (Freehold/Leasehold), and Road Width to generate highly accurate bank-level valuations.
* **🎨 Modern UI/UX:** Built with a sleek, dark-themed Glassmorphism interface using Tailwind CSS.

---

## 🛠️ Tech Stack
* **Backend:** FastAPI (Python)
* **Frontend:** HTML5, Tailwind CSS, JavaScript (Vanilla)
* **AI Integration:** Groq API (Meta Llama-3 Model)
* **Environment Management:** `python-dotenv` for secure API key storage.

---

## 🚀 Setup & Installation (Linux/Ubuntu)

**1. Clone the repository**
```bash
git clone <your-repository-url>
cd Liquidity_Engine
2. Create a fresh Virtual Environment
(Note: Do not move the .venv folder across directories. Always create a fresh one if the project path changes).

Bash
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies

Bash
pip install fastapi uvicorn httpx python-dotenv
4. Setup Environment Variables
Create a .env file in the root directory and add your Groq API key:

Code snippet
GROQ_API_KEY=your_actual_api_key_here
5. Run the Server

Bash
uvicorn main:app --reload
The dashboard will be live at http://127.0.0.1:8000.

💡 How It Works
Data Collection: The user inputs property details via the frontend.

Deterministic Math (Backend): FastAPI calculates a base_price using grounded area rates and strict age-based building depreciation.

AI Reasoning (LLM): The base price and granular details are passed to Llama-3. The AI is prompted to strictly use the base price and assess liquidity risks (Chain of Thought).

Final Output: The API returns the calculated values, risk flags, and reasoning steps to the user dashboard.
