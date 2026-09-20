"""统一的 LLM 接口。

从项目根目录的 config.yaml 读取 AI 配置（api_base / api_key / api_url / model），
走 OpenAI 兼容的 /chat/completions 协议，用 requests 调用，不依赖 openai SDK。

用法::

    from backend.utils.llm import chat

    text = chat([{"role": "user", "content": "你好"}])
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

__all__ = ["load_config", "chat", "chat_raw", "CONFIG_PATH"]

# backend/utils/llm.py -> 上溯三级到项目根目录
CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yaml"


def _parse_flat_yaml(path: Path) -> Dict[str, Any]:
    """PyYAML 缺失时的兜底解析，只支持顶层的 `key: value`。"""
    data: Dict[str, Any] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data


@lru_cache(maxsize=None)
def load_config(path: Optional[str] = None) -> Dict[str, Any]:
    """读取 config.yaml，结果带缓存。"""
    config_path = Path(path) if path else CONFIG_PATH
    if not config_path.exists():
        raise FileNotFoundError(f"找不到配置文件：{config_path}")
    try:
        import yaml
    except ImportError:
        return _parse_flat_yaml(config_path)
    with config_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _resolve(model: Optional[str] = None) -> Dict[str, Any]:
    cfg = load_config()
    missing = [k for k in ("api_key", "api_url") if not cfg.get(k)]
    if missing:
        raise ValueError(f"config.yaml 缺少字段：{', '.join(missing)}")
    return {**cfg, "model": model or cfg.get("model")}


def chat_raw(
    messages: List[Dict[str, str]],
    *,
    model: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: Optional[int] = None,
    timeout: int = 60,
    **kwargs: Any,
) -> Dict[str, Any]:
    """调用 LLM，返回原始响应字典。"""
    cfg = _resolve(model)
    payload: Dict[str, Any] = {
        "model": cfg["model"],
        "messages": messages,
        "temperature": temperature,
        **kwargs,
    }
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens

    resp = requests.post(
        cfg["api_url"],
        headers={
            "Authorization": f"Bearer {cfg['api_key']}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def chat(
    messages: List[Dict[str, str]],
    *,
    model: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: Optional[int] = None,
    timeout: int = 60,
    **kwargs: Any,
) -> str:
    """调用 LLM，返回助手的文本回复。"""
    data = chat_raw(
        messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        **kwargs,
    )
    return data["choices"][0]["message"]["content"]
