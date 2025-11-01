# src/pdf_processing/extract.py
"""
Testlerin beklediği extract_text API'si için köprü.
Önce mevcut pdf_parser içindeki fonksiyonları dener; yoksa PyPDF2 ile okur.
"""
from __future__ import annotations

from pathlib import Path
from typing import Union

PathLike = Union[str, Path]

# 1) Mevcut pdf_parser içindeki muhtemel fonksiyon isimlerini dene
try:
    from .pdf_parser import extract_text as _extract_text_impl  # type: ignore
except Exception:
    _extract_text_impl = None

if _extract_text_impl is None:
    try:
        from .pdf_parser import parse_pdf as _extract_text_impl  # type: ignore
    except Exception:
        _extract_text_impl = None

def _fallback_extract_text(path: PathLike) -> str:
    """PyPDF2 ile basit metin çıkarma (yedek)."""
    from PyPDF2 import PdfReader  # PyPDF2 yoksa `pip install PyPDF2`
    p = Path(path)
    reader = PdfReader(str(p))
    parts = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        parts.append(txt)
    return "\n".join(parts).strip()

def extract_text(path: PathLike) -> str:
    if _extract_text_impl is not None:
        return _extract_text_impl(path)
    return _fallback_extract_text(path)
