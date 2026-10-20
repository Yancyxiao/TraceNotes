# TraceNotes · 循例注释

**沿一个例子，看到状态变化，读懂真实代码。**

[English](README.md) | [简体中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Agent Skill](https://img.shields.io/badge/Agent-Skill-4B5563)
![Language-adaptive](https://img.shields.io/badge/Comments-Language%20adaptive-2563EB)

TraceNotes 是为代码添加学习型注释的 Agent Skill。它让具体输入贯穿真实实现，在关键代码旁展示中间状态、解释操作顺序，再对应回最终输出。它根据读者背景调整讲解，自动识别合适的注释语言，并保持原有可执行逻辑。**编程语言不设白名单，直接针对项目实际使用的语言进行适配。**

适合开发、数据、数据库、基础设施等技术人员阅读陌生实现。经验丰富的工程师，也可能需要仔细理解一个不熟悉的子系统。

## 目录

- [效果示例](#效果示例)
- [安装](#安装)
- [使用](#使用)
- [工作方式](#工作方式)
- [调整讲解方式](#调整讲解方式)
- [兼容性与边界](#兼容性与边界)
- [仓库结构](#仓库结构)
- [验证](#验证)
- [参与贡献](#参与贡献)
- [致谢](#致谢)
- [许可证](#许可证)

## 效果示例

“保存当前批次”只说出了操作名称。TraceNotes 会解释：在哪一轮保存、此时变量是什么、保存后清空为什么不会丢失结果。

下面示例使用英文注释；实际任务会根据用户明确要求、目标代码已有注释或用户提问的语言选择，不固定使用英文。

```python
# Example: items=["AA", "BBB", "C", "DDDD"], limit=5.
# Expected: [["AA", "BBB"], ["C", "DDDD"]].
# Assume positive limit and each item's length<=limit.

# After "AA" and "BBB": current=["AA", "BBB"], used=5.
# On "C", 5+1>5: save the previous batch before starting another.
if current and used + len(item) > limit:
    # Save a snapshot; clearing current next will not erase this batch.
    result.append(current.copy())
    current.clear()
    used = 0
```

这样可以明确：`AA` 和 `BBB` 已占满长度 5；遇到 `C` 时先保存前一批的副本，再清空容器，开始下一批。

这里只是片段，不能独立运行。完整的[注释前](examples/batching.before.py)与[注释后](examples/batching.after.py)示例可以直接对照；验证脚本会比较二者的 Python AST，并检查结果。

同样的方法可以解释栈、递归、滑动窗口、异步操作和 SQL 等过程。重点在难懂的状态转换，不要求逐句翻译源码。

## 安装

### 使用 skills CLI

CLI 当前要求 Node.js 22.20 或更高版本。按使用的 Agent 选择：

```bash
# Codex，全局可用
npx skills add Yancyxiao/TraceNotes --skill trace-notes -a codex -g

# Claude Code，全局可用
npx skills add Yancyxiao/TraceNotes --skill trace-notes -a claude-code -g
```

去掉 `-g` 即为项目级安装。可以先执行 `npx skills add Yancyxiao/TraceNotes --list` 查看 skill。

通过 SSH 克隆后，从本地目录安装：

```bash
git clone git@github.com:Yancyxiao/TraceNotes.git
cd TraceNotes
npx skills add . --skill trace-notes -a codex -g
```

其他 Agent、参数、更新和卸载方式见 [skills CLI 官方说明](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)。TraceNotes 本身不依赖 Node.js 运行时。

### 手动安装

把 `SKILL.md`、`references/`、`agents/` 和 `LICENSE` 放入 Agent 的 `trace-notes` 技能文件夹：

| Agent | 常见用户级位置 |
| --- | --- |
| Codex | `${CODEX_HOME:-$HOME/.codex}/skills/trace-notes/` |
| Claude Code | `~/.claude/skills/trace-notes/` |
| 其他 Agent Skills 工具 | 遵循工具自身的技能发现规则 |

`SKILL.md` 应直接位于 `trace-notes/` 下。如果未发现技能，按宿主说明重新加载或重启会话。

## 使用

在 Codex 中：

```text
$trace-notes
给 src/batching.py 的 pack 方法添加学习型注释，使用英文。
我知道 Python 语法，但不理解为什么要先复制再清空。
用一个完整例子贯穿，保持实现不变。
```

在 Claude Code 中，可以使用 `/trace-notes` 并说明目标与疑惑，也可以在请求中点名 TraceNotes。调用语法及自动选择行为取决于宿主。

```text
用 TraceNotes 给这个 Java 方法添加中文注释。
重点展示每次关键出栈前后，栈中有哪些元素。
```

```text
用 TraceNotes 给这个 JavaScript 函数添加英文注释。
用一个具体例子说明 Promise.all 的结果顺序。
```

```text
用 TraceNotes 讲解这个方法，只返回带注释的片段，不修改文件。
跳过基础语法，重点讲异常如何向上传播。
```

要求给文件加注释时，在授权范围内编辑；只要求解释代码时，返回带注释的片段。仓库规则和更高优先级指令仍然适用。

## 工作方式

1. **核对实现：** 阅读真实代码、关键辅助方法、调用方、配置和相关测试。
2. **一句话说明用途：** 先明确这段代码完成什么任务。
3. **选择一个例子：** 明确输入、必要假设、单位和预期输出。
4. **追踪关键变化：** 在关键语句旁说明前后状态，解释顺序为什么重要。
5. **讲清容易误解的地方：** 包括副作用、边界、失败路径、副本与引用等相关内容。
6. **对应回最终结果：** 核对例子、注释和改动是否影响原有逻辑。

发现具体问题时，单独给出证据与修正建议。添加注释不自动包含修复或重构授权。

## 调整讲解方式

下面都是自然语言偏好，不是 CLI 参数，也不需要配置文件。

| 偏好 | 示例 |
| --- | --- |
| 目标 | 文件、函数、方法、查询或提供的片段 |
| 注释语言 | 自动识别，也可以明确指定；与代码使用的编程语言独立选择 |
| 详细程度 | 简洁维护注释、重点过程讲解、详细教学 |
| 读者背景 | 熟悉 Java，但刚接触响应式流 |
| 关注问题 | 保存与重置、递归、取消、表格行、范围边界 |
| 已知概念 | 跳过循环基础，重点解释所有权和生命周期 |
| 交叉引用 | 长方法中使用稳定的例子或步骤标签 |

编程语言与注释语言分开选择。在遵守适用的强制指令及其优先级的前提下，按以下顺序确定注释语言：

1. 用户本次明确指定的注释语言。
2. 目标方法已有实质性注释的主要语言；方法内没有时，再看同文件附近代码。
3. 用户当前提问的语言；中外文混合时，参考主要请求或已经明确的会话偏好。

已有注释为空或混杂、无法判断主要语言时，回退到用户提问的语言，不自动强制英文。识别时不把变量名、示例字符串、许可证声明或复制的外部文本当作语言依据。回复仍使用用户的会话语言；代码中的变量名、API、字面量和实际输出值保持不变。README 只有中英文版本，不代表生成的注释只能使用中英文。

## 兼容性与边界

| 方面 | 范围 |
| --- | --- |
| Agent 接入 | 普通 `SKILL.md`，附可选 Codex UI 配置；不要求特定 MCP、IDE 或模型厂商 |
| 编程语言 | 不设语言白名单，按目标语言、方言及注释语法适配 |
| 示例用途 | 演示状态追踪与验证方法，不是支持语言清单 |
| 注释自然语言 | 不设白名单；根据用户要求与现有上下文识别，也可明确指定 |
| 读者水平 | 分别判断通用经验和当前领域熟悉度 |
| 不支持注释的格式 | 保持格式有效，提供片段或授权的配套说明 |
| 逻辑保持 | 通过约束与验证减少误改，不是数学意义上的保证 |

TraceNotes 不设注释行数配额，不限制只能写 ASCII，不擅自重构。保留文件约定和有实际语义的指令注释，对未知辅助方法和并发顺序明确说明，不编造结果。参见[语言安全说明](references/language-safety.md)。

仓库不包含遥测或后台服务。宿主 Agent 仍遵循自身执行、隐私和权限设置。自带示例不代表所有编程语言或宿主 Agent 都已经完成端到端测试。

## 仓库结构

```text
TraceNotes/
  SKILL.md                     Agent 工作指令
  README.md                    英文说明
  README.zh-CN.md               中文说明
  agents/openai.yaml           可选 Codex UI 配置
  references/                  示例、安全说明、练习场景
  examples/                    可运行的注释前后对照
  scripts/                     验证与示例检查
  docs/design.md               设计取舍与来源说明
  .github/                     CI 与贡献模板
  CONTRIBUTING.md
  SECURITY.md
  CHANGELOG.md
  LICENSE
```

## 验证

使用 skill 不需要安装 Python 或 Java。维护此仓库需要 Python 3.10+、Node.js 和 JDK 17+：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python scripts/verify_examples.py
```

必要时指定 JDK：`python scripts/verify_examples.py --java-home /path/to/jdk-21`。

检查覆盖元数据、本地文档链接、YAML 配置、Python 注释前后 AST 一致性、示例输出、部分边界和可控的异步顺序。GitHub Actions 配置为在 Linux 和 Windows 执行。

这些检查验证文件和具体示例，不衡量自动触发准确率，也不证明模型生成的每条注释都正确。[练习场景](references/practice-cases.md)提供评估真实输出的定性标准。

## 参与贡献

欢迎提交可复现示例、特定语言修正和文档改进。请同步维护两份 README。参见[贡献指南](CONTRIBUTING.md)、[安全说明](SECURITY.md)和[变更记录](CHANGELOG.md)。

## 致谢

- [github/awesome-copilot：add-educational-comments](https://github.com/github/awesome-copilot/blob/main/skills/add-educational-comments/SKILL.md)：按读者背景调整教学、配置深度、保留文件约定。
- [mohitagw15856/pm-claude-skills：code-explainer](https://github.com/mohitagw15856/pm-claude-skills/blob/main/skills/code-explainer/SKILL.md)：先明确用途、按步骤讲解、关注非显然行为。
- [anthropics/skills](https://github.com/anthropics/skills)、[obra/superpowers](https://github.com/obra/superpowers) 和 [vercel-labs/skills](https://github.com/vercel-labs/skills)：参考技能包装、安装说明和仓库文档组织方式。

工作流和示例重新编写。[设计说明](docs/design.md)记录了采纳内容与保留差异，不表示上述项目与本项目存在隶属或背书关系。

## 许可证

[MIT](LICENSE)。贡献使用同一许可证。
