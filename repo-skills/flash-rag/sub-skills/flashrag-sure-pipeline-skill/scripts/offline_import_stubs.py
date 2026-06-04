from __future__ import annotations

import sys
from importlib.machinery import ModuleSpec
from types import ModuleType, SimpleNamespace


def _module(name: str) -> ModuleType:
    module = ModuleType(name)
    module.__spec__ = ModuleSpec(name, loader=None)
    return module


class _FakeEncoding:
    def encode(self, text, *args, **kwargs):
        return list(range(len(str(text).split())))

    def decode(self, tokens):
        return " ".join(str(token) for token in tokens)


def install_offline_import_stubs() -> None:
    """Install minimal optional dependency stubs for offline fake pipeline smoke tests."""
    if "torch" not in sys.modules:
        torch = _module("torch")
        torch.cuda = SimpleNamespace(
            is_available=lambda: False,
            device_count=lambda: 0,
            manual_seed=lambda *_args, **_kwargs: None,
            manual_seed_all=lambda *_args, **_kwargs: None,
        )
        torch.manual_seed = lambda *_args, **_kwargs: None
        torch.backends = SimpleNamespace(cudnn=SimpleNamespace(benchmark=False, deterministic=True))
        torch.inference_mode = lambda *args, **kwargs: SimpleNamespace(__enter__=lambda self: None, __exit__=lambda self, *exc: False)
        sys.modules["torch"] = torch

    if "transformers" not in sys.modules:
        transformers = _module("transformers")

        class _AutoConfig:
            _name_or_path = "offline-stub"
            architectures = ["OfflineStub"]

            @classmethod
            def from_pretrained(cls, *_args, **_kwargs):
                return cls()

        class _AutoTokenizer:
            vocab_size = 0
            added_tokens_decoder = {}

            @classmethod
            def from_pretrained(cls, *_args, **_kwargs):
                return cls()

            def encode(self, text, *args, **kwargs):
                return list(range(len(str(text).split())))

            def decode(self, tokens, *args, **kwargs):
                return " ".join(str(token) for token in tokens)

            def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=True):
                return "\n".join(str(message.get("content", "")) for message in messages)

            def convert_tokens_to_ids(self, token):
                return abs(hash(token)) % 100000

        transformers.AutoConfig = _AutoConfig
        transformers.AutoTokenizer = _AutoTokenizer
        transformers.PreTrainedTokenizer = _AutoTokenizer
        transformers.PreTrainedTokenizerFast = _AutoTokenizer
        transformers.LogitsProcessorList = list
        sys.modules["transformers"] = transformers

    if "datasets" not in sys.modules:
        datasets = _module("datasets")
        datasets.load_dataset = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("datasets stub cannot load remote data"))
        datasets.Image = object
        sys.modules["datasets"] = datasets

    if "tiktoken" not in sys.modules:
        tiktoken = _module("tiktoken")
        tiktoken.encoding_for_model = lambda *_args, **_kwargs: _FakeEncoding()
        sys.modules["tiktoken"] = tiktoken

    if "PIL" not in sys.modules:
        pil = _module("PIL")
        image_mod = _module("PIL.Image")

        class _Image:
            pass

        image_mod.Image = _Image
        pil.Image = image_mod
        sys.modules["PIL"] = pil
        sys.modules["PIL.Image"] = image_mod
