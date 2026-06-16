"""Builders package — PR4.

Each builder transforms MarketContextInput (raw aggregated data)
into a structured Pydantic section of the MarketThesis.
"""

from .flows_builder import build_flows
from .news_builder import build_news
from .probabilities_builder import build_probabilities
from .risks_builder import build_risks
from .technique_builder import build_technique

__all__ = [
    "build_technique",
    "build_flows",
    "build_news",
    "build_risks",
    "build_probabilities",
]
