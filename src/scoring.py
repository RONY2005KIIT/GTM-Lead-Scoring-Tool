import pandas as pd
from typing import Dict, Any, Tuple

def default_scoring_criteria() -> Dict[str, Any]:
    """
    Returns the default ICP (Ideal Customer Profile) and scoring parameters.
    """
    return {
        "target_industries": ["Technology", "Software", "Finance", "Healthcare"],
        "target_sizes": ["11-50", "51-200", "201-500", "501-1000", "1000+"],
        "tech_stack_keywords": ["cloud", "aws", "salesforce", "react"],
        "growth_signal_weight": 20,
        "industry_weight": 30,
        "size_weight": 20,
        "tech_stack_weight": 30
    }

def calculate_lead_score(company_data: Dict[str, Any], criteria: Dict[str, Any]) -> Tuple[float, str]:
    """
    Evaluates enriched company information against set criteria to generate a score.
    
    Args:
        company_data (Dict[str, Any]): Enriched company details.
        criteria (Dict[str, Any]): Rules and weights for scoring.
        
    Returns:
        Tuple[float, str]: (score from 0-100, summary breakdown / reasoning details)
    """
    # Scoring computation skeleton
    score = 50.0
    breakdown = "Matches default baseline. Awaiting user customization rules."
    return score, breakdown

def assign_priority_tier(score: float) -> str:
    """
    Assigns a priority category based on the numerical lead score.
    
    Args:
        score (float): The final score (0-100).
        
    Returns:
        str: 'Tier 1 (High)', 'Tier 2 (Medium)', or 'Tier 3 (Low)'
    """
    if score >= 80:
        return "Tier 1 (High)"
    elif score >= 50:
        return "Tier 2 (Medium)"
    else:
        return "Tier 3 (Low)"

def score_leads_batch(df: pd.DataFrame, criteria: Dict[str, Any]) -> pd.DataFrame:
    """
    Computes scores and appends scoring and priority columns to a leads DataFrame.
    
    Args:
        df (pd.DataFrame): Enriched leads DataFrame.
        criteria (Dict[str, Any]): Rules and weights for scoring.
        
    Returns:
        pd.DataFrame: DataFrame containing original data plus score, tier, and rationale.
    """
    # Batch scoring loop skeleton
    return df.copy()
