from turbopyffer import TurboPufferClient, AddVectorsPayload, RetrieveVectorsResponse
import numpy as np
import os
import json

index_name="jeadie-1"
c = TurboPufferClient(os.environ["API_KEY"])
c.delete_index(index_name)

c.add_vectors(index_name=index_name, vectors=np.random.random((2, 6)), ids=[2,3])
c.build_index(index_name)
for v in c.query_vectors(index_name, np.random.random(6), 5):
    print(v)

for batch in c.retrieve_all_vectors(index_name):
    for i, b in zip(batch.ids, batch.vectors):
        print(i, b)

result = c.retrieve_vectors(index_name=index_name)
for _id, v in zip(result.ids, result.vectors):
    print(f"retrieve_vectors: {_id} --> {v}")

for batch in c.retrieve_all_vectors(index_name=index_name):
    print(f"retrieve_all_vectors: {batch.next_cursor}")
    for _id, v in zip(batch.ids, batch.vectors):
        print(f"retrieve_all_vectors: {_id} --> {v}")

recall = c.test_recall(index_name=index_name)
print(recall.at_10)

c.delete_index(index_name)

# requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://api.turbopuffer.com/v1/vectors/jeadie/_debug/recall