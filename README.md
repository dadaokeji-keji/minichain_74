# MiniChain · 迷你区块链教学演示

> 用 300 行纯 Python 标准库，把「哈希链 + 工作量证明 + 最长链共识 + 篡改检测」跑给你看。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-10%20passed-brightgreen.svg)](tests/)
[![Version](https://img.shields.io/badge/version-v1.0.0-orange.svg)](CHANGELOG.md)

---

## 为什么做这个项目

区块链课程里，比特币、以太坊、Hyperledger Fabric 都很宏大，但初学者往往在「装环境」这一步就卡住了：
需要 Docker、需要 Node、需要同步区块，还没看到一条链，热情先被消耗掉一半。

MiniChain 的目标很朴素：**`git clone` 之后 10 秒内看到一条真实的链在运行**，
并且每一行代码都能在课堂上讲清楚。它不追求性能与安全，只追求「可解释」。

## 功能特性

- **零第三方依赖**：只用 Python 标准库（`hashlib` / `json` / `argparse` / `unittest`），机房离线也能跑。
- **真实的 SHA-256 工作量证明**：难度可配置，哈希必须以 N 个 `0` 开头。
- **最长链共识**：`replace_with()` 演示分叉后如何选择主链。
- **篡改检测**：改动一笔交易，整条链立刻校验失败。
- **一条命令的完整演示**：`python -m minichain demo`，适合课堂投屏。
- **中文文档 + 10 个单元测试 + 语义化版本**。

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/dadaokeji-keji/minichain_74.git
cd minichain_74

# 2. 运行完整演示（无需安装任何依赖，默认挖矿难度 4）
python -m minichain demo
```

### 运行效果

```text
$ python -m minichain demo
MiniChain v1.0.0 · 迷你区块链演示
==============================================================
① 初始化区块链（难度 = 4）
   创世区块 #0 已生成，耗时 1187 ms
   hash = 00009cf099a994bce5ba1368e9255e15f96e58e4b68c92e89080a4cf77f7dcf0

② 打包交易并挖矿
   #1 耗时 13 ms | nonce=2200    hash=00000fc053827ea104611269…
   #2 耗时 372 ms | nonce=64686   hash=000082193995b579fb8aac78…
   #3 耗时 656 ms | nonce=108568  hash=000006334815f6aa3fc372e0…

③ 校验整条链
   ✅ 校验通过：共 4 个区块，难度 4

④ 模拟攻击：篡改 #2 号区块的交易
   篡改后 #2 的交易：['Carol → Dave 7000 枚']

⑤ 再次校验
   ❌ 第 2 号区块的工作量证明无效
   原理：哈希变了，后面的区块全部断链，篡改无法隐藏。
```

## 命令行用法

| 命令 | 作用 |
| --- | --- |
| `python -m minichain demo` | 完整演示：出块 → 校验 → 篡改 → 再校验 |
| `python -m minichain mine -t "A→B 10"` | 追加一个新区块（`-t` 可重复） |
| `python -m minichain validate` | 校验整条链，非法时返回退出码 1 |
| `python -m minichain show` | 以表格形式打印整条链 |
| `python -m minichain export -o chain.json` | 把链导出为 JSON |
| `python -m minichain benchmark` | 测试难度 1~4 的平均出块耗时 |
| `python -m minichain benchmark` | 测试难度 1~4 的平均出块耗时 |
| `python -m minichain --load chain.json show` | 从 JSON 载入后查看 |

通用参数：`-d/--difficulty` 指定挖矿难度（默认 4），`-v/--version` 查看版本。

## 目录结构

```text
minichain_74/
├── minichain/            # 核心包
│   ├── block.py          # 区块：哈希计算与工作量证明
│   ├── chain.py          # 链：出块、校验、篡改、最长链替换
│   ├── cli.py            # 命令行界面
│   └── __main__.py       # 支持 python -m minichain
├── tests/test_chain.py   # 10 个单元测试
├── docs/                 # 设计说明、协作规范、战略分析
├── .github/              # Issue / PR 模板
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## 核心概念对照

| 概念 | 代码位置 | 说明 |
| --- | --- | --- |
| 哈希链 | `Block.previous_hash` | 每个区块保存前驱哈希，形成链式结构 |
| 工作量证明 | `Block.mine()` | 调整 nonce 直到哈希满足难度 |
| 防篡改 | `Blockchain.is_valid()` | 内容变化 → 哈希变化 → 校验失败 |
| 最长链共识 | `Blockchain.replace_with()` | 只接受更长且合法的链 |
| 交易打包 | `Blockchain.add_block()` | 一组交易 → 一个区块 |

## 运行测试

```bash
python -m unittest discover -s tests -v
# Ran 10 tests ... OK
```

## 路线图

- [x] v1.0.0 核心链、PoW、CLI、单元测试
- [ ] v1.1 难度自适应（按出块时间动态调整）
- [ ] v1.2 交易签名（`hmac` 简化版 UTXO）
- [ ] v2.0 浏览器可视化：一条链的「成长过程」动画

## 参与贡献

欢迎提交 Issue 与 Pull Request，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 与
[协作规范](docs/协作规范.md)。所有参与者需遵守 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

## 许可证

本项目使用 [MIT License](LICENSE) 发布，可自由使用、修改与分发，保留版权声明即可。

## 作者

徐茂林 · 区块链 232 · 学号 2023131074
课程：开源文化运动（指导教师：范佳）