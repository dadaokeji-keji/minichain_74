# 参与贡献

感谢你愿意为 MiniChain 做出贡献！无论是提 Issue、改文档，还是提交代码，都非常欢迎。

## 快速上手

1. Fork 本仓库并克隆到本地：

   ```bash
   git clone https://github.com/<你的用户名>/minichain_74.git
   cd minichain_74
   ```

2. 创建分支（命名见 [协作规范](docs/协作规范.md)）：

   ```bash
   git switch -c feature/your-feature
   ```

3. 本地验证（本项目零依赖，只需 Python 3.9+）：

   ```bash
   python -m unittest discover -s tests -v
   python -m minichain demo
   ```

4. 提交并推送：

   ```bash
   git add .
   git commit -m "feat(scope): 一句话说明"
   git push -u origin feature/your-feature
   ```

5. 在 GitHub 上发起 Pull Request，描述里写清楚「改了什么 / 为什么改 / 怎么验证」。

## 提交前检查清单

- [ ] 单元测试全部通过
- [ ] 新增逻辑有对应测试
- [ ] 公开函数有中文 docstring
- [ ] 没有引入第三方运行时依赖
- [ ] 提交信息符合 Conventional Commits

## Issue 规范

- 使用仓库提供的 Issue 模板；
- Bug 请附上 Python 版本、复现步骤、完整报错；
- 功能建议请说明使用场景，而不是只给结论。

## 行为准则

参与本项目即表示你同意遵守 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。