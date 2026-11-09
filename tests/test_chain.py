"""MiniChain 的单元测试。

运行方式::

    python -m unittest discover -s tests -v
"""

import unittest

from minichain import Block, Blockchain


class TestBlock(unittest.TestCase):
    def test_hash_is_deterministic(self):
        block = Block(index=1, transactions=["a"], previous_hash="0" * 64, timestamp=1700000000)
        self.assertEqual(block.compute_hash(), block.compute_hash())
        self.assertEqual(len(block.compute_hash()), 64)

    def test_mine_meets_difficulty(self):
        block = Block(index=1, transactions=["a"], previous_hash="0" * 64, difficulty=3)
        block.mine()
        self.assertTrue(block.hash.startswith("000"))
        self.assertTrue(block.is_valid_proof())

    def test_content_change_breaks_hash(self):
        block = Block(index=1, transactions=["a"], previous_hash="0" * 64, difficulty=2)
        block.mine()
        original = block.hash
        block.transactions = ["b"]
        self.assertNotEqual(original, block.compute_hash())


class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.chain = Blockchain(difficulty=2)

    def test_genesis_block(self):
        self.assertEqual(self.chain.height, 0)
        self.assertEqual(self.chain.chain[0].previous_hash, "0" * 64)
        self.assertTrue(self.chain.is_valid()[0])

    def test_add_block_links_previous_hash(self):
        block = self.chain.add_block(["Alice → Bob 10"])
        self.assertEqual(block.previous_hash, self.chain.chain[0].hash)
        self.assertEqual(self.chain.height, 1)

    def test_valid_chain_passes(self):
        for i in range(3):
            self.chain.add_block([f"tx-{i}"])
        ok, _ = self.chain.is_valid()
        self.assertTrue(ok)
        self.assertEqual(self.chain.height, 3)

    def test_tampering_is_detected(self):
        self.chain.add_block(["Alice → Bob 10"])
        self.chain.tamper(1, ["Alice → Bob 99999"])
        ok, reason = self.chain.is_valid()
        self.assertFalse(ok)
        self.assertIn("无效", reason)

    def test_replace_prefers_longer_chain(self):
        other = Blockchain(difficulty=2)
        for i in range(2):
            other.add_block([f"other-{i}"])
        self.assertTrue(self.chain.replace_with(other.chain))
        self.assertEqual(self.chain.height, 2)

    def test_replace_rejects_shorter_chain(self):
        self.chain.add_block(["a"])
        other = Blockchain(difficulty=2)
        self.assertFalse(self.chain.replace_with(other.chain))

    def test_json_roundtrip(self):
        self.chain.add_block(["a", "b"])
        restored = Blockchain.from_dict(self.chain.to_dict())
        self.assertEqual(restored.height, self.chain.height)
        self.assertTrue(restored.is_valid()[0])


if __name__ == "__main__":
    unittest.main()