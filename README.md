# ⚡ Liquidity Engine - AI-Powered Collateral Valuation Dashboard

## 📌 Overview
The **Liquidity Engine** is a market-aware collateral intelligence dashboard designed for NBFCs, secured lenders, and real estate professionals. Moving beyond traditional, static pricing models, this engine utilizes advanced LLMs to evaluate both the **intrinsic value** (what the asset should sell for) and the **liquidity risk** (how fast and reliably it can be sold) of a property in the Indian Real Estate market.

## 🚀 Key Features
Provide the engine with basic property details (Location, Size, Age, Property Type), and it dynamically generates:
* **Estimated Market Value (₹):** Optimal price range in normal market conditions.
* **Distress Sale Value (₹):** Fire-sale equivalent price incorporating liquidity discounts.
* **Resale Potential Index (RPI):** A 0-100 score indicating how liquid/easy-to-sell the asset is.
* **Time to Liquidate:** Estimated days required to sell the property.
* **Risk Alerts & Key Drivers:** Automated anomaly detection (e.g., leasehold complexities, location mismatches) and positive valuation drivers.

## 🛠️ Tech Stack
* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
* **Backend:** Python, FastAPI
* **AI Engine:** Groq API (using the `llama-3.3-70b-versatile` model)
* **HTTP Client:** `httpx` (for async API calls)

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

**1. Clone the repository (if applicable) or navigate to your project folder:**
```bash
cd Liquidity_Engine
2. Set up a Virtual Environment (Recommended):

Bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
3. Install the required dependencies:

Bash
pip install fastapi uvicorn httpx
4. Add your API Key:

Open main.py in your code editor.

Locate the Groq API Key variable.

Replace the placeholder with your actual Groq API Key (gsk_...).

5. Run the Server:
Start the FastAPI server using Uvicorn:

Bash
uvicorn main:app --reload
6. Access the Dashboard:
Open your web browser and go to:
http://127.0.0.1:8000

🧠 How it Works
The user inputs property attributes via the intuitive UI.

The frontend sends a POST request to the FastAPI backend /analyze endpoint.

The backend constructs a highly specific System Prompt instructing the AI to act as an "Expert Indian Real Estate Valuer" calculating strictly in INR (₹).

The request is securely routed via Groq's lightning-fast inference engine using httpx.

The LLM processes the location intelligence and property characteristics, returning a structured JSON response.

The dashboard updates dynamically in real-time without page reloads.

🚧 Future Scope
Integration with Live Maps API for exact geospatial coordinates.

Connecting to Government Circle Rate APIs for dynamic statutory floor values.

Image upload feature for automated interior/exterior condition scoring.
