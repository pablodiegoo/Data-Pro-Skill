import pandas as pd

def categorize_text(text: str, category_dict: dict, default_category: str = "Outros", missing_category: str = "NS/NR") -> str:
    """
    Categorizes a spontaneous text string based on a dictionary of keywords.
    
    Args:
        text (str): The raw text to categorize.
        category_dict (dict): Dictionary where keys are category names and values are lists of keywords (lowercase).
                              Example: {"Show": ["music", "band", "stage"], "Food": ["food", "drink", "beer"]}
        default_category (str): Category assigned if no keywords match.
        missing_category (str): Category assigned if text is null or empty.
        
    Returns:
        str: The assigned category name.
    """
    if not text or pd.isna(text):
        return missing_category
        
    # Standardize string for comparison
    text_lower = str(text).lower()
    
    for cat_name, keywords in category_dict.items():
        if any(kw in text_lower for kw in keywords):
            return cat_name
            
    return default_category

def apply_qualitative_categorization(df: pd.DataFrame, source_col: str, target_col: str, category_dict: dict):
    """
    Applies qualitative categorization to an entire DataFrame column.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        source_col (str): The column containing raw spontaneous text.
        target_col (str): The new column to store the categorical result.
        category_dict (dict): Dictionary of categories and keywords.
        
    Returns:
        pd.DataFrame: The updated DataFrame.
    """
    df_copy = df.copy()
    df_copy[target_col] = df_copy[source_col].apply(lambda x: categorize_text(x, category_dict))
    
    # Print summary
    counts = df_copy[target_col].value_counts(normalize=True) * 100
    print(f"Categorization Summary for '{source_col}':")
    print(counts.round(2).astype(str) + "%")
    
    return df_copy

# Example Usage:
# if __name__ == "__main__":
#     df = pd.DataFrame({"feedback": ["The band was great", "Too expensive", "I loved the music", None]})
#     cats = {"Entertainment": ["band", "music", "show"], "Cost": ["expensive", "price", "money"]}
#     df_clean = apply_qualitative_categorization(df, "feedback", "feedback_category", cats)
#     print(df_clean)
