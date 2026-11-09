# 更新日志

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 与
[Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 规范。

## [Unreleased]

### 计划中
- 难度自适应：根据最近 N 个区块的出块时间动态调整 `difficulty`
- 交易签名：用 `hmac` 实现简化版 UTXO 与签名校验

## [1.0.0] - 2026-11-09

### 新增
- `Block`：SHA-256 哈希计算、工作量证明、JSON 序列化
- `Blockchain`：创世区块、出块、整链校验、篡改模拟、最长链替换
- CLI：`demo` / `mine` / `validate` / `show` / `export` 五个子命令
- 10 个单元测试，覆盖哈希确定性、难度、断链、篡改与 JSON 往返
- 文档：README、设计说明、协作规范、五看三定分析
- 社区规范：CONTRIBUTING、CODE_OF_CONDUCT、Issue/PR 模板