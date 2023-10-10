from enum import Enum
import json 
from typing import List, Optional

import numpy as np
from pydantic import BaseModel, field_serializer


class DistanceMetric(str, Enum):
    euclidean_squared = "euclidean_squared"
    

class AddVectorsPayload(BaseModel):
    vectors: np.ndarray
    ids: List[int]

    @field_serializer('vectors')
    def serialize_dt(self, vectors: np.ndarray, _info):
        return json.dumps(vectors.tolist())

    class Config:
        arbitrary_types_allowed = True

class QueryVectorsPayload(BaseModel):
    vectors: np.ndarray
    ids: List[int]

    @field_serializer('vectors')
    def serialize_dt(self, vectors: np.ndarray, _info):
        return json.dumps(vectors.tolist())

    class Config:
        arbitrary_types_allowed = True

class QueryVectorsResponse(BaseModel):
    id: int

class BuildIndexPayload(BaseModel):
    distance_metric: DistanceMetric

class RetrieveVectorsResponse(BaseModel):
    ids: List[int]
    vectors: np.ndarray
    next_cursor: Optional[str]

    @field_serializer('vectors')
    def serialize_dt(self, vectors: np.ndarray, _info):
        return json.dumps(vectors.tolist())

    class Config:
        arbitrary_types_allowed = True

class RecallResponse(BaseModel):
    at_10: float
