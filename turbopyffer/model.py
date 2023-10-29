from enum import Enum
import json 
from typing import Any, Dict, List, Optional

import numpy as np
from pydantic import BaseModel, field_serializer

from .error import TurboPufferError

class DistanceMetric(str, Enum):
    euclidean_squared = "euclidean_squared"
    

class AddVectorsPayload(BaseModel):
    vectors: np.ndarray
    ids: List[int]

    @field_serializer('vectors')
    def serialize_vectors(self, vectors: np.ndarray, _info):
        return vectors.tolist()

    class Config:
        arbitrary_types_allowed = True

class QueryVectorsPayload(BaseModel):
    vector: np.ndarray
    top_k: int

    @field_serializer('vector')
    def serialize_vectors(self, vector: np.ndarray, _info):
        return vector.tolist()

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
    def serialize_vectors(self, vectors: np.ndarray, _info):
        return vectors.tolist()

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_json(cls, _json: Dict[str, Any]) -> "RetrieveVectorsResponse":
        try:
            return RetrieveVectorsResponse(
                ids = _json['ids'],
                next_cursor= _json.get("next_cursor", None),
                vectors=np.asarray(_json['vectors'])
            )
        except KeyError:
            raise TurboPufferError(f"Invalid json object to create RetrieveVectorsResponse: {_json}")

class RecallResponse(BaseModel):
    at_10: float
