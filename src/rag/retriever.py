# src/rag/retriever.py
"""
TopKRetriever için basit bir köprü sınıfı:
- index(texts, ids, embed_fn)
- search(query, embed_fn=None, top_k=None) -> [{'id','text','score'}, ...]
"""

from __future__ import annotations
from typing import Callable, Iterable, List, Dict, Any, Optional, Tuple

Vector = List[float]
EmbedFn = Callable[[Iterable[str]], List[Vector]]

def _cosine(a: Vector, b: Vector) -> float:
    import math
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

class TopKRetriever:
    def __init__(self, k: int = 3, embed_fn: Optional[EmbedFn] = None) -> None:
        self.k = k
        self._embed_fn: Optional[EmbedFn] = embed_fn
        self._docs: List[Tuple[str, str]] = []  # (id, text)
        self._vecs: List[Vector] = []

    def index(self, *, texts: List[str], ids: List[str], embed_fn: Optional[EmbedFn] = None) -> None:
        assert len(texts) == len(ids), "texts ve ids uzunlukları eşit olmalı"
        ef = embed_fn or self._embed_fn
        if ef is None:
            raise ValueError("embed_fn gerekli (kurucuda veya index çağrısında verilmeli)")
        self._docs = list(zip(ids, texts))
        self._vecs = ef(texts)

    def search(self, query: str, *, embed_fn: Optional[EmbedFn] = None, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        if not self._docs or not self._vecs:
            return []
        ef = embed_fn or self._embed_fn
        if ef is None:
            raise ValueError("embed_fn gerekli (kurucuda veya search çağrısında verilmeli)")
        qv = ef([query])[0]
        scored = []
        for (doc_id, text), vec in zip(self._docs, self._vecs):
            score = _cosine(qv, vec)
            scored.append({"id": doc_id, "text": text, "score": float(score)})
        k = top_k or self.k
        scored.sort(key=lambda r: r["score"], reverse=True)
        return scored[:k]
