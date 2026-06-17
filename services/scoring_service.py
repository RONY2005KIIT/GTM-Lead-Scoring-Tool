from typing import Dict, Any

# Default target parameters for GTM fit matching
DEFAULT_TARGET_INDUSTRIES = ["software", "saas", "technology", "fintech", "finance", "healthcare", "e-commerce", "artificial intelligence", "biotech"]
DEFAULT_TARGET_SIZES = ["51-200", "201-500", "501-1000", "1000+", "10,000+"]
DEFAULT_GROWTH_KEYWORDS = ["funding", "hiring", "expansion", "growth", "launch", "acquire", "raising", "raised", "expand", "recruiting", "valuation"]
DEFAULT_BUYER_PERSONAS = ["cto", "vp of product", "head of engineering", "vp of finance", "chief technology officer", "director of product", "vp of marketing", "vp of sales", "chief operating officer", "coo", "head of partnerships"]

def calculate_lead_score(enriched_data: Dict[str, Any], target_profile: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Calculates the ICP alignment score and outbound sales priority category.
    
    Scoring rules (Total 100 points):
    - Industry fit = 25 points
    - Company size = 25 points
    - Growth signals = 25 points
    - Buyer persona fit = 25 points
    
    Priority categorization:
    - 80+ = High
    - 60-79 = Medium
    - Below 60 = Low
    
    Args:
        enriched_data (Dict[str, Any]): Enriched metrics from Gemini analysis.
        target_profile (Dict[str, Any], optional): Custom overrides for targeting.
        
    Returns:
        Dict[str, Any]: Dictionary containing 'score', 'priority', and 'breakdown' details.
    """
    if not target_profile:
        target_profile = {}

    target_industries = target_profile.get("target_industries", DEFAULT_TARGET_INDUSTRIES)
    target_sizes = target_profile.get("target_sizes", DEFAULT_TARGET_SIZES)
    growth_keywords = target_profile.get("growth_keywords", DEFAULT_GROWTH_KEYWORDS)
    buyer_personas = target_profile.get("buyer_personas", DEFAULT_BUYER_PERSONAS)

    # 1. Industry Fit (25 pts)
    industry_text = str(enriched_data.get("industry", "")).lower()
    industry_score = 0.0
    if any(ind in industry_text for ind in target_industries):
        industry_score = 25.0
    elif industry_text and "error" not in industry_text and "unknown" not in industry_text:
        industry_score = 10.0  # Partial fit fallback

    # 2. Company Size Fit (25 pts)
    size_text = str(enriched_data.get("company_size", "")).lower()
    size_score = 0.0
    if any(sz in size_text for sz in target_sizes):
        size_score = 25.0
    elif size_text and "error" not in size_text and "unknown" not in size_text:
        size_score = 10.0  # Partial fit fallback

    # 3. Growth Signals (25 pts)
    growth_text = str(enriched_data.get("growth_signals", "")).lower()
    growth_score = 0.0
    matches = [kw for kw in growth_keywords if kw in growth_text]
    if len(matches) >= 2:
        growth_score = 25.0
    elif len(matches) == 1:
        growth_score = 15.0
    elif growth_text and "error" not in growth_text and "unknown" not in growth_text:
        growth_score = 5.0

    # 4. Buyer Persona Fit (25 pts)
    persona_text = str(enriched_data.get("buyer_persona", "")).lower()
    persona_score = 0.0
    if any(pers in persona_text for pers in buyer_personas):
        persona_score = 25.0
    elif persona_text and "error" not in persona_text and "unknown" not in persona_text:
        persona_score = 10.0

    # Calculate final summation
    total_score = industry_score + size_score + growth_score + persona_score

    # Assign Priority category
    if total_score >= 80.0:
        priority = "High"
    elif total_score >= 60.0:
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "score": int(total_score),
        "priority": priority,
        "breakdown": {
            "industry_fit": int(industry_score),
            "company_size_fit": int(size_score),
            "growth_signals_fit": int(growth_score),
            "buyer_persona_fit": int(persona_score)
        }
    }
