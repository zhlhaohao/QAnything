"""Wrapper around YouDao embedding models."""
from typing import List

from qanything_kernel.connector.embedding.embedding_client import EmbeddingClient
from qanything_kernel.configs.model_config import LOCAL_EMBED_SERVICE_URL, LOCAL_EMBED_MODEL_NAME, LOCAL_EMBED_MAX_LENGTH, LOCAL_EMBED_BATCH
import concurrent.futures

embedding_client = EmbeddingClient(
    server_url=LOCAL_EMBED_SERVICE_URL,
    model_name=LOCAL_EMBED_MODEL_NAME,
    model_version='1',
    resp_wait_s=120,
    tokenizer_path='qanything_kernel/connector/embedding/embedding_model_0630')

# PPP# 文本嵌入代码,在这里修改代码摆脱triton server
class YouDaoLocalEmbeddings:
    def __init__(self):
        pass

    # 调用推理服务器进行queries条文本的嵌入推理    
    def _get_embedding(self, queries):
        embeddings = embedding_client.get_embedding(queries, max_length=LOCAL_EMBED_MAX_LENGTH)
        # print(f"embeddings...{queries}")
        # print(embeddings)
        return embeddings

    # PPP## 多线程并发进行批量文本嵌入（一个线程处理batch_size条文本,N个线程并发）
    def _get_len_safe_embeddings(self, texts: List[str]) -> List[List[float]]:
        all_embeddings = []
        batch_size = LOCAL_EMBED_BATCH
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                future = executor.submit(self._get_embedding, batch)
                futures.append(future)
            for future in futures:
                embeddings = future.result()
                all_embeddings += embeddings
        return all_embeddings

    @property
    def embed_version(self):
        return embedding_client.getModelVersion()
