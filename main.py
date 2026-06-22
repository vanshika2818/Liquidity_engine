from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Literal
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Real Estate Liquidity Engine",
    description="API for property valuation and liquidity assessment using Hybrid AI Architecture & Data Grounding",
    version="0.1.0"
)

# Load API Key from .env
GROK_API_KEY = os.getenv("GROK_API_KEY")

# Mock database of area rates in INR per sqft
AREA_RATES_DB = {
    'udaiganj': 8000,
    'gomti nagar': 12000,
    'hazratganj': 15000,
    'indira nagar': 7000,
    'aliganj': 9000,
    'mumbai': 25000,
    'bandra': 40000,
    'andheri': 22000,
    'gurgaon': 14000,
    'bengaluru': 11000
}

class PropertyValuationRequest(BaseModel):
    location: str = Field(..., description="Location of the property")
    size_sqft: float = Field(..., description="Size of the property in square feet")
    building_age_years: int = Field(..., description="Age of the building in years")
    category: Literal["Residential", "Commercial", "Land"] = Field(..., description="Category of the property")
    subtype: Literal["Apartment", "Independent House", "Plot", "Shop"] = Field(..., description="Sub-type of the property")
    legal_status: Literal["Freehold", "Leasehold", "Unregistered"] = Field(..., description="Legal status of the property")
    road_width: Literal["Narrow Alley", "Standard Road", "Main Highway"] = Field(..., description="Road width leading to the property")

@app.post("/analyze", response_model=dict)
async def analyze_collateral(payload: PropertyValuationRequest):
    """
    Evaluate collateral value, liquidity, and risk metrics using a Hybrid AI approach.
    """
    if GROK_API_KEY is None:
        raise HTTPException(status_code=500, detail="API key not configured. Please paste your key in .env.")

    # --- DATA GROUNDING (RAG CONCEPT) ---
    location_lower = payload.location.lower()
    area_rate = 6000  # Default rate
    
    for area, rate in AREA_RATES_DB.items():
        if area in location_lower:
            area_rate = rate
            break
            
    # --- HYBRID AI ARCHITECTURE: PYTHON BASE MATH ---
    # Assume a default rate of ₹6000/sqft
    default_rate = 6000
    base_price_before_depreciation = payload.size_sqft * default_rate
    
    # Strictly deduct 1% of the total value for every year of the property's age (Depreciation)
    depreciation = base_price_before_depreciation * 0.01 * payload.building_age_years
    base_price = max(0.0, base_price_before_depreciation - depreciation)
    # ------------------------------------------------

    system_prompt = (
        "You are an expert Indian Real Estate Valuer. "
        "All price calculations (Market Value, Distress Value) MUST be strictly in Indian Rupees (INR) "
        "and accurately reflect the current Indian real estate market rates. Do not use USD or any other currency. "
        f"The exact current market rate for this specific location is ₹{area_rate} per sqft. You MUST base your entirely valuation strictly on this rate. "
        f"The mathematically calculated base price is exactly ₹{base_price}. Use this absolute number as your starting point. Only adjust it slightly based on the location and property type to determine the final Market Value, Distress Value, RPI, and Time to Sell. "
        "Before outputting the final numeric values, you must first calculate the values step-by-step. Add a new field called \"reasoning_steps\" at the very top of your JSON response explaining your exact math (e.g., Size * Rate - Depreciation = Final). "
        "Given the property details, calculate the following metrics: "
        "1. Estimated Market Value Range (e.g. '₹1.50 Cr - ₹1.65 Cr' or '₹50,00,000 - ₹55,00,000') "
        "2. Distress Sale Value Range (e.g. '₹1.10 Cr - ₹1.25 Cr' or '₹35,00,000 - ₹40,00,000') "
        "3. Resale Potential Index (integer between 0 and 100) "
        "4. Estimated Time to Liquidate (e.g. '30-60 Days') "
        "5. Risk Flags (list of strings, 0-3 flags) "
        "6. Key Drivers (list of strings, 2-4 positive drivers) "
        "Return the output STRICTLY as valid JSON with the exact keys: "
        "'reasoning_steps', 'market_value', 'distress_value', 'resale_potential_index', 'time_to_liquidate', 'risk_flags', 'key_drivers'. "
        "Do not include markdown blocks, just the raw JSON object."
    )
    
    user_prompt = (
        f"Location: {payload.location}\n"
        f"Size (sqft): {payload.size_sqft}\n"
        f"Age (years): {payload.building_age_years}\n"
        f"Category: {payload.category}\n"
        f"Sub-type: {payload.subtype}\n"
        f"Legal Status: {payload.legal_status}\n"
        f"Road Width: {payload.road_width}"
    )

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
            
            if response.status_code != 200:
                print(f"API Error: {response.status_code} - {response.text}")
                raise HTTPException(status_code=500, detail=f"API Error: {response.status_code} - {response.text}")
                
            result = response.json()
            
            # Safely extract content
            choices = result.get("choices", [])
            if not choices:
                raise ValueError("No choices returned in API response")
                
            ai_content = choices[0].get("message", {}).get("content", "")
            
            # Clean up the response if it has markdown formatting
            ai_content = ai_content.strip()
            if ai_content.startswith("```json"):
                ai_content = ai_content[7:]
            if ai_content.startswith("```"):
                ai_content = ai_content[3:]
            if ai_content.endswith("```"):
                ai_content = ai_content[:-3]
            ai_content = ai_content.strip()
            
            try:
                parsed_json = json.loads(ai_content)
                return parsed_json
            except json.JSONDecodeError:
                print(f"Failed to parse JSON. Raw content: {ai_content}")
                raise ValueError("API did not return valid JSON")
            
        except httpx.RequestError as e:
            print(f"HTTP Request failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Network error connecting to API: {str(e)}")
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            print(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing API response: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    with open("index.html", "r") as f:
        return f.read()

@app.get("/health")
async def health_check():
    return {"status": "ok"}
