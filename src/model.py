from enum import Enum
from typing import List, Optional

import numpy as np
from pydantic import BaseModel

from .model import DistanceMetric


class AddVectorsPayload(BaseModel):
    vectors: np.ndarray
    ids: List[int]

class QueryVectorsPayload(BaseModel):
    vectors: np.ndarray
    ids: List[int]

class QueryVectorsResponse(BaseModel):
    id: int

class BuildIndexPayload(BaseModel):
    distance_metric: DistanceMetric

class RetrieveVectorsResponse(BaseModel):
    ids: List[int]
    vectors: np.ndarray
    next_cursor: Optional[str]

class RecallResponse(BaseModel):
    at_10: float

class DistanceMetric(str, Enum):
    euclidean_squared = "euclidean_squared"

    