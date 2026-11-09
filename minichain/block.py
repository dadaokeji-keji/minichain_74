"""区块（Block）的数据结构与哈希计算。

本模块只依赖 Python 标准库，便于在教室、机房等离线环境中直接运行。
区块的哈希由「高度 + 时间戳 + 交易 + 前哈希 + nonce + 难度」共同决定，
其中任何一项被改动，哈希都会完全不同——这正是区块链防篡改的基础。
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field


@dataclass
class Block:
    """一个区块。

    Attributes:
        index: 区块高度，创世区块为 0。
        transactions: 交易列表，教学演示中用字符串表示。
        previous_hash: 前一个区块的哈希。
        timestamp: 出块时间（Unix 时间戳，秒）。
        nonce: 工作量证明的计数器。
        difficulty: 目标难度，哈希必须以 difficulty 个 "0" 开头。
        hash: 本区块的 SHA-256 哈希，由 :meth:`mine` 计算得出。
    """

    index: int
    transactions: list[str]
    previous_hash: str
    timestamp: float = field(default_factory=time.time)
    nonce: int = 0
    difficulty: int = 4
    hash: str = ""

    def payload(self) -> str:
        """返回参与哈希计算的规范化字符串（不含 hash 自身）。

        使用 sort_keys 与紧凑分隔符，保证同一份数据在任何机器上
        都得到完全相同的字节序列。
        """
        data = {
            "index": self.index,
            "timestamp": round(self.timestamp, 6),
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "difficulty": self.difficulty,
        }
        return json.dumps(
            data, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )

    def compute_hash(self) -> str:
        """计算当前字段（不含 hash）对应的 SHA-256 哈希。"""
        return hashlib.sha256(self.payload().encode("utf-8")).hexdigest()

    def mine(self) -> "Block":
        """执行工作量证明：不断调整 nonce，直到哈希满足难度要求。"""
        target = "0" * self.difficulty
        while True:
            self.hash = self.compute_hash()
            if self.hash.startswith(target):
                return self
            self.nonce += 1

    def is_valid_proof(self) -> bool:
        """校验哈希是否既与内容一致、又满足难度要求。"""
        target = "0" * self.difficulty
        return self.hash == self.compute_hash() and self.hash.startswith(target)

    def to_dict(self) -> dict:
        """导出为可 JSON 序列化的字典。"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "difficulty": self.difficulty,
            "hash": self.hash,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Block":
        """从字典重建区块。"""
        return cls(**data)

    def short_hash(self) -> str:
        """返回便于阅读的短哈希，例如 ``0000a1b2c3d4…``。"""
        return f"{self.hash[:12]}…" if self.hash else "<未计算>"