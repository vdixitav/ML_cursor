from typing import Dict,Any
from dataclasses import dataclass, field

@dataclass

class GraphState:
    data: Any=None
    target: str |None=None
    artifacts: Dict[str,Any]=field(default_factory=dict)
    metrics:Dict[str,Any]=field(default_factory=dict)
    errors:list[str]=field(default_factory=list)
    