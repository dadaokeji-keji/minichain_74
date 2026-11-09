"""区块链（Blockchain）的核心逻辑：出块、校验、最长链替换。"""

from __future__ import annotations

import json
import time
from typing import Iterable

from .block import Block


class Blockchain:
    """一条区块链。

    创世区块在实例化时自动生成；每个新区块都保存前一个区块的哈希，
    从而形成一条不可回改的哈希链。校验时同时检查「链接关系」与
    「每个区块的工作量证明」。
    """

    GENESIS_PREV_HASH = "0" * 64

    def __init__(self, difficulty: int = 4) -> None:
        if difficulty < 1:
            raise ValueError("difficulty 至少为 1")
        self.difficulty = difficulty
        self.chain: list[Block] = [self._build_genesis()]

    # ------------------------------------------------------------------ 构建
    def _build_genesis(self) -> Block:
        genesis = Block(
            index=0,
            transactions=["创世区块：MiniChain 诞生"],
            previous_hash=self.GENESIS_PREV_HASH,
            difficulty=self.difficulty,
        )
        return genesis.mine()

    def add_block(self, transactions: Iterable[str]) -> Block:
        """把一组交易打包成新区块并挖矿上链。"""
        block = Block(
            index=len(self.chain),
            transactions=list(transactions),
            previous_hash=self.chain[-1].hash,
            difficulty=self.difficulty,
        )
        block.mine()
        self.chain.append(block)
        return block

    # ------------------------------------------------------------------ 查询
    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    @property
    def height(self) -> int:
        return len(self.chain) - 1

    def is_valid(self, chain: list[Block] | None = None) -> tuple[bool, str]:
        """校验整条链，返回 ``(是否合法, 原因)``。

        检查三件事：
        1. 创世区块的前哈希必须是 64 个 0；
        2. 相邻区块的 previous_hash 必须等于前一个区块的 hash；
        3. 每个区块自身的哈希要能复算出来，且满足难度要求。
        """
        chain = self.chain if chain is None else chain
        if not chain:
            return False, "链为空"

        genesis = chain[0]
        if genesis.previous_hash != self.GENESIS_PREV_HASH:
            return False, "创世区块的前哈希不合法"

        for block in chain:
            if not block.is_valid_proof():
                return False, f"第 {block.index} 号区块的工作量证明无效"

        for prev, curr in zip(chain, chain[1:]):
            if curr.previous_hash != prev.hash:
                return False, f"第 {curr.index} 号区块与前驱断链"
            if curr.index != prev.index + 1:
                return False, f"第 {curr.index} 号区块高度不连续"

        return True, f"校验通过：共 {len(chain)} 个区块，难度 {chain[0].difficulty}"

    # ------------------------------------------------------------------ 篡改
    def tamper(self, index: int, new_transactions: list[str]) -> Block:
        """【教学用】直接改写某个区块的交易，模拟攻击者篡改历史。"""
        block = self.chain[index]
        block.transactions = list(new_transactions)
        return block

    # ------------------------------------------------------------------ 共识
    def replace_with(self, other: list[Block]) -> bool:
        """最长链规则：仅当对方链更长且合法时替换本地链。"""
        if len(other) <= len(self.chain):
            return False
        ok, _ = self.is_valid(other)
        if not ok:
            return False
        self.chain = other
        return True

    # ------------------------------------------------------------------ 存取
    def to_dict(self) -> dict:
        return {
            "difficulty": self.difficulty,
            "height": self.height,
            "chain": [block.to_dict() for block in self.chain],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(self.to_json())

    @classmethod
    def load(cls, path: str) -> "Blockchain":
        with open(path, "r", encoding="utf-8") as fh:
            return cls.from_dict(json.load(fh))

    @classmethod
    def from_dict(cls, data: dict) -> "Blockchain":
        obj = cls(difficulty=data["difficulty"])
        obj.chain = [Block.from_dict(item) for item in data["chain"]]
        return obj

    # ------------------------------------------------------------------ 展示
    def summary(self) -> str:
        """返回一行一句话的链状态，便于 CLI 输出。"""
        ok, reason = self.is_valid()
        status = "✅ 合法" if ok else "❌ 非法"
        return f"高度 {self.height} | 难度 {self.difficulty} | {status} | {reason}"