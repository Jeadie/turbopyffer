from typing import Generator, List, Optional

import numpy as np
from pydantic import BaseModel, HttpUrl

from .model import BuildIndexPayload, AddVectorsPayload, QueryVectorsResponse, QueryVectorsPayload, RetrieveVectorsResponse, RecallResponse, DistanceMetric
from .http import HttpRequests


DEFAULT_BASE_URL = "https://api.turbopuffer.com/v1/vectors"


class TurboPufferClient:
    def __init__(self, token, url=DEFAULT_BASE_URL):
        self.http = HttpRequests(url, {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

    def build_index(self, index_name: str, distance_metric: DistanceMetric = DistanceMetric.euclidean_squared):
        self.http.send_request(
            "POST",
            f"/{index_name}/index",
            body=BuildIndexPayload(distance_metric=distance_metric).json()
        )

    def delete_index(self, index_name: str):
        self.http.send_request(
            "DELETE",
            f"/{index_name}/index",
        )

    def delete_vectors_and_index(self):
        self.http.send_request("DELETE", f"")
    
    def add_vectors(self, index_name: str, vectors: np.ndarray, ids: list[int]):
        self.http.send_request("POST", f"/{index_name}", body=AddVectorsPayload(vectors=vectors, ids=ids).json())

    def query_vectors(self, index_name: str, vector: np.ndarray, top_k: int) -> List[QueryVectorsResponse]:
        result = self.http.send_request("POST", f"/{index_name}/query", body=QueryVectorsPayload(vector=vector, top_k=top_k).json())
        return  [
            QueryVectorsResponse(id=r["id"]) for r in result
        ]

    def retrieve_vectors(self, index_name: str, cursor: Optional[str] = None) -> RetrieveVectorsResponse:
        result = self.http.send_request("GET", f"/{index_name}", param={"cursor": cursor} if cursor else None)
        return RetrieveVectorsResponse.from_json(result)

    def retrieve_all_vectors(self, index_name: str) -> Generator[RetrieveVectorsResponse, None, None]:
        cursor = None
        while True:
            response = self.retrieve_vectors(index_name, cursor)
            cursor = response.next_cursor
            yield response
            if not cursor:
                break

    def test_recall(self, index_name: str) -> RecallResponse:
        result = self.http.send_request("GET", f"/{index_name}/_debug/recall")
        return RecallResponse(at_10=result["recall@10"])