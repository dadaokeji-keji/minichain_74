"""MiniChain —— 一个零依赖的迷你区块链教学库。

只暴露最常用的三个名字，方便课堂演示：

    >>> from minichain import Blockchain
    >>> chain = Blockchain()
    >>> chain.add_block(["A 转给 B 10 枚"])
"""

from .block import Block
from .chain import Blockchain

__version__ = "1.0.0"
__all__ = ["Block", "Blockchain", "__version__"]