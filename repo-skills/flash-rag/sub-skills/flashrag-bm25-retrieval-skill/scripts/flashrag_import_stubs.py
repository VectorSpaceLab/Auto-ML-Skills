from __future__ import annotations

import sys
from importlib.machinery import ModuleSpec
from types import ModuleType
import types


def _module(name: str) -> ModuleType:
    module = ModuleType(name)
    module.__spec__ = ModuleSpec(name, loader=None)
    return module


def install_optional_import_stubs() -> None:
    """Install minimal stubs for optional imports unused by BM25 smoke tests."""
    if "faiss" not in sys.modules:
        faiss = _module("faiss")
        faiss.omp_set_num_threads = lambda *_args, **_kwargs: None
        sys.modules["faiss"] = faiss

    if "langid" not in sys.modules:
        langid = _module("langid")
        langid.classify = lambda _text: ("en", 1.0)
        sys.modules["langid"] = langid

    if "Stemmer" not in sys.modules:
        class _IdentityStemmer:
            def stemWord(self, word):
                return word

        stemmer = _module("Stemmer")
        stemmer.Stemmer = lambda _language: _IdentityStemmer()
        sys.modules["Stemmer"] = stemmer
