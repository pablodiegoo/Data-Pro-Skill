"""
DataPro - Data Analysis Intelligence

An AI-powered toolkit for data analysis recommendations.
"""

__version__ = "0.1.3"
__author__ = "Pablo Diego"

from datapro.search import search_knowledge_base
from datapro.reasoning import (
    profile_data, 
    generate_analysis_plan, 
    format_plan,
    DataProfile,
    AnalysisPlan,
    Recommendation
)
from datapro.styles import StylePresets, get_styles
from datapro.dictionary_mapper import DictionaryMapper

__all__ = [
    "search_knowledge_base",
    "profile_data",
    "generate_analysis_plan",
    "format_plan",
    "DataProfile",
    "AnalysisPlan",
    "Recommendation",
    "StylePresets",
    "get_styles",
    "DictionaryMapper",
    "__version__",
]
