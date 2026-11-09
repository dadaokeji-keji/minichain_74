"""MiniChain 命令行入口。

用法示例::

    python -m minichain demo                 # 完整演示：出块 → 校验 → 篡改 → 再校验
    python -m minichain mine -t "A→B 10"     # 追加一个新区块
    python -m minichain validate             # 校验链的完整性
    python -m minichain show                 # 打印当前链
    python -m minichain export -o chain.json # 导出为 JSON
    python -m minichain benchmark            # 测试不同难度下的平均出块耗时
"""

from __future__ import annotations

import argparse
import sys
import time

from . import __version__
from .block import Block
from .chain import Blockchain


def _fmt_seconds(seconds: float) -> str:
    return f"{seconds * 1000:.0f} ms"


def cmd_demo(args: argparse.Namespace) -> int:
    """一条龙演示，适合课堂投屏。"""
    print(f"MiniChain v{__version__} · 迷你区块链演示")
    print("=" * 62)

    print(f"① 初始化区块链（难度 = {args.difficulty}）")
    start = time.perf_counter()
    chain = Blockchain(difficulty=args.difficulty)
    print(f"   创世区块 #0 已生成，耗时 {_fmt_seconds(time.perf_counter() - start)}")
    print(f"   hash = {chain.last_block.hash}")

    print("\n② 打包交易并挖矿")
    batches = [
        ["Alice → Bob 10 枚", "Bob → Carol 3 枚"],
        ["Carol → Dave 7 枚"],
        ["Dave → Alice 2 枚", "Alice → Carol 5 枚"],
    ]
    for batch in batches:
        start = time.perf_counter()
        block = chain.add_block(batch)
        print(
            f"   #{block.index} 耗时 {_fmt_seconds(time.perf_counter() - start)} | "
            f"nonce={block.nonce:<7} hash={block.hash[:24]}…"
        )

    print("\n③ 校验整条链")
    ok, reason = chain.is_valid()
    print(f"   {'✅' if ok else '❌'} {reason}")

    print("\n④ 模拟攻击：篡改 #2 号区块的交易")
    target = chain.tamper(2, ["Carol → Dave 7000 枚"])
    print(f"   篡改后 #2 的交易：{target.transactions}")
    print(f"   内容已变，但区块里保存的 hash 仍是 {target.hash[:24]}…")

    print("\n⑤ 再次校验")
    ok, reason = chain.is_valid()
    print(f"   {'✅' if ok else '❌'} {reason}")
    print("   原理：哈希变了，后面的区块全部断链，篡改无法隐藏。")

    print("\n⑥ 恢复链并查看结构")
    chain = Blockchain(difficulty=args.difficulty)
    for batch in batches:
        chain.add_block(batch)
    print(chain.summary())
    return 0


def cmd_mine(args: argparse.Namespace) -> int:
    chain = _load_or_new(args)
    block = chain.add_block(args.transaction)
    print(f"已出块 #{block.index}  nonce={block.nonce}  hash={block.hash}")
    if args.save:
        chain.save(args.save)
        print(f"链已保存到 {args.save}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    chain = _load_or_new(args)
    ok, reason = chain.is_valid()
    print(f"{'✅' if ok else '❌'} {reason}")
    return 0 if ok else 1


def cmd_show(args: argparse.Namespace) -> int:
    chain = _load_or_new(args)
    print(f"{'高度':<6}{'nonce':>8}  {'哈希':<40}交易")
    for block in chain.chain:
        print(
            f"{block.index:<6}{block.nonce:>8}  {block.hash[:38]:<40}"
            f"{'; '.join(block.transactions)}"
        )
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    chain = _load_or_new(args)
    chain.save(args.output)
    print(f"已导出 {len(chain.chain)} 个区块到 {args.output}")
    return 0


def cmd_benchmark(args: argparse.Namespace) -> int:
    """测量不同难度下的平均出块耗时，帮助学生建立「难度」的直觉。"""
    print(f"{'难度':<6}{'期望尝试次数':>12}{'平均耗时':>12}")
    for difficulty in range(1, args.max_difficulty + 1):
        costs = []
        for _ in range(args.rounds):
            block = Block(
                index=1,
                transactions=["benchmark"],
                previous_hash="0" * 64,
                difficulty=difficulty,
            )
            start = time.perf_counter()
            block.mine()
            costs.append(time.perf_counter() - start)
        avg = sum(costs) / len(costs)
        print(f"{difficulty:<6}{16 ** difficulty:>12}{_fmt_seconds(avg):>12}")
    print("\n提示：难度每 +1，期望尝试次数约为原来的 16 倍。")
    return 0


def _load_or_new(args: argparse.Namespace) -> Blockchain:
    if getattr(args, "load", None):
        return Blockchain.load(args.load)
    return Blockchain(difficulty=args.difficulty)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="minichain",
        description="MiniChain · 零依赖的迷你区块链教学演示",
    )
    parser.add_argument("-v", "--version", action="version", version=f"MiniChain {__version__}")
    parser.add_argument(
        "-d", "--difficulty", type=int, default=4, help="挖矿难度，默认 4（哈希以 4 个 0 开头）"
    )
    parser.add_argument("--load", metavar="FILE", help="从 JSON 文件读取已有链")

    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="完整演示：出块 → 校验 → 篡改 → 再校验")
    demo.set_defaults(func=cmd_demo)

    mine = sub.add_parser("mine", help="追加一个新区块")
    mine.add_argument("-t", "--transaction", action="append", required=True,
                      help="交易内容，可重复传入多笔")
    mine.add_argument("-s", "--save", metavar="FILE", help="出块后把链保存到文件")
    mine.set_defaults(func=cmd_mine)

    validate = sub.add_parser("validate", help="校验链的完整性")
    validate.set_defaults(func=cmd_validate)

    show = sub.add_parser("show", help="以表格形式打印整条链")
    show.set_defaults(func=cmd_show)

    export = sub.add_parser("export", help="把链导出为 JSON")
    export.add_argument("-o", "--output", default="chain.json", help="输出文件，默认 chain.json")
    export.set_defaults(func=cmd_export)

    bench = sub.add_parser("benchmark", help="测试不同难度下的平均出块耗时")
    bench.add_argument("-n", "--rounds", type=int, default=3, help="每个难度的测试次数，默认 3")
    bench.add_argument("--max-difficulty", type=int, default=4, help="最大测试难度，默认 4")
    bench.set_defaults(func=cmd_benchmark)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())