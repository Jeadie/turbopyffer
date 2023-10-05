# TurboPyffer

## Install
```shell
pip install turbopuffer-sdk
```

## Usage
```python
from turbopuffer import TurboPufferClient

client = TurboPufferClient(token="YOUR_API_TOKEN")
```

Building an Index
```python
client.build_index(index_name="my_index")
```

Adding Vectors
```python
import numpy as np

vectors = np.array([[1,2,3], [4,5,6]])
ids = [1, 2]
client.add_vectors(index_name="my_index", vectors=vectors, ids=ids)
```

Querying Vectors
```python
vector = np.array([1,2,3])
top_k_results = client.query_vectors(index_name="my_index", vector=vector, top_k=5)
```

Retrieving Vectors
```python
result = client.retrieve_vectors(index_name="my_index")
for _id, v in zip(result.ids, result.vectors):
    print(f"{_id} --> {v}")
```

Or as a pythonic generator
```python
for batch in client.retrieve_all_vectors(index_name="index-name"):
    for _id, v in zip(batch.ids, batch.vectors):
        print(f"{_id} --> {v}")
```

Evaluating Recall
```python
recall = client.test_recall(index_name="my_index")
print(recall.at_10)
```

Error Handling
The SDK provides a custom exception TurboPufferError to handle any issues that arise during API interactions.
```python
from turbopuffer import TurboPufferError

try:
    # Any SDK operation
except TurboPufferError as e:
    print(e)
```
