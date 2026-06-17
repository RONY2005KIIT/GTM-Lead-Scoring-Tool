import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

# Read the API key
api_key = os.getenv("GEMINI_API_KEY")

class CompanyAnalysis(BaseModel):
    industry: str = Field(description="Primary industry classification of the company")
    company_size: str = Field(description="Estimated company size/employee count range")
    buyer_persona: str = Field(description="Recommended key buyer persona / target titles at this company")
    growth_signals: str = Field(description="Signals of growth (e.g. recent funding, hiring, expansions, partnerships)")
    reason_to_prioritize: str = Field(description="Strategic justification of why outbound sales should prioritize this account")

def analyze_company(company_name: str, api_key_override: str = None) -> Dict[str, Any]:
    """
    Enriches company information by querying Gemini API and returning structured JSON results.
    
    Args:
        company_name (str): Name of the target company.
        api_key_override (str, optional): Custom Gemini API key override.
        
    Returns:
        Dict[str, Any]: Structured JSON analysis containing industry, company_size, 
                        buyer_persona, growth_signals, and reason_to_prioritize.
    """
    fallback_response = {
        "industry": "Error / Unknown",
        "company_size": "Error / Unknown",
        "buyer_persona": "Error / Unknown",
        "growth_signals": "Error / Unknown",
        "reason_to_prioritize": "Error / Unknown"
    }

    active_key = api_key_override or api_key

    if not active_key:
        print("Error: No Gemini API Key provided (env or override).")
        return {**fallback_response, "reason_to_prioritize": "API Key is missing or not configured."}

    try:
        # Initialize Google GenAI client using the active key
        client = genai.Client(api_key=active_key)
        
        prompt = (
            f"Analyze the company: '{company_name}'. "
            f"Research and provide professional corporate intelligence for our outbound sales team."
        )
        
        # Call the Gemini model (gemini-2.5-flash is standard, stable, and fast in the new SDK)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': CompanyAnalysis,
                'temperature': 0.2
            }
        )
        
        # Access the parsed Pydantic object and convert to dict
        if response and response.parsed:
            parsed_obj = response.parsed
            if hasattr(parsed_obj, "model_dump"):
                return parsed_obj.model_dump()
            else:
                return parsed_obj.dict()
        else:
            return {**fallback_response, "reason_to_prioritize": "Empty or invalid response from Gemini API."}
            
    except Exception as e:
        print(f"Error occurred during company analysis for {company_name}: {e}")
        return {**fallback_response, "reason_to_prioritize": f"Failed during analysis: {str(e)}"}
