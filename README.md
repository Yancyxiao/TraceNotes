# TraceNotes

**Follow one example. See the state change. Understand the code.**

[English](README.md) | [简体中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Agent Skill](https://img.shields.io/badge/Agent-Skill-4B5563)
![Language-adaptive](https://img.shields.io/badge/Comments-Language%20adaptive-2563EB)

TraceNotes is an Agent Skill for educational code comments. It follows a concrete input through the real implementation, explains important intermediate states, and connects them to the final output. It adapts to the reader's background, selects the comment language from user instructions, local comments, or the user's question, and keeps executable behavior unchanged. There is no programming-language whitelist: use the method with the language of the actual code.

For developers, data engineers, database specialists, infrastructure engineers, and anyone reading an unfamiliar implementation. An experienced engineer may still need a detailed walkthrough of a new subsystem.

## Contents

- [See the difference](#see-the-difference)
- [Install](#install)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Preferences](#preferences)
- [Compatibility and limits](#compatibility-and-limits)
- [Repository layout](#repository-layout)
- [Validation](#validation)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## See the difference

`# Save the batch` names an operation. TraceNotes explains the moment when that operation matters:

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

This is an excerpt, not a standalone program. Compare the runnable [before](examples/batching.before.py) and [after](examples/batching.after.py) files. Validation compares their Python ASTs and checks their outputs.

The method also applies to stacks, recursion, sliding windows, async operations, and queries. Comments focus on difficult transitions rather than every statement.

## Install

### With the skills CLI

The CLI currently requires Node.js 22.20 or later. Choose your agent:

```bash
# Codex, available across projects
npx skills add Yancyxiao/TraceNotes --skill trace-notes -a codex -g

# Claude Code, available across projects
npx skills add Yancyxiao/TraceNotes --skill trace-notes -a claude-code -g
```

Omit `-g` for project-scoped installation. Inspect the skill first with `npx skills add Yancyxiao/TraceNotes --list`.

For an SSH-authenticated local checkout:

```bash
git clone git@github.com:Yancyxiao/TraceNotes.git
cd TraceNotes
npx skills add . --skill trace-notes -a codex -g
```

See the [skills CLI documentation](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) for agents, options, updates, and uninstalling. TraceNotes itself has no Node.js runtime dependency.

### Manual installation

Copy `SKILL.md`, `references/`, `agents/`, and `LICENSE` into a folder named `trace-notes` in your agent's skill directory:

| Agent | Typical user-level folder |
| --- | --- |
| Codex | `${CODEX_HOME:-$HOME/.codex}/skills/trace-notes/` |
| Claude Code | `~/.claude/skills/trace-notes/` |
| Other Agent Skills hosts | Follow the host's documented discovery rules |

Keep `SKILL.md` directly inside `trace-notes/`. Follow the host's reload/restart instructions if the skill is not visible.

## Usage

In Codex:

```text
$trace-notes
Add learning-oriented comments to src/batching.py::pack in English.
I know Python, but do not understand why copying happens before clearing.
Follow one complete example and preserve the implementation.
```

In Claude Code, use `/trace-notes` with the target and learning goal, or request the skill by name. Invocation syntax and automatic selection depend on the host.

```text
Use TraceNotes to explain this Java method with Chinese comments.
Show the stack before and after each important pop.
```

```text
Use TraceNotes to annotate this JavaScript function in English.
Explain Promise.all ordering with one concrete example.
```

```text
Use TraceNotes to explain this function with an annotated excerpt.
Do not edit files. Skip syntax basics and focus on error propagation.
```

A request to add comments authorizes edits within that scope; a request only to explain returns an annotated excerpt. Repository instructions and higher-priority constraints still apply.

## How it works

1. **Ground the explanation:** read the implementation, relevant helpers, caller, configuration, and tests.
2. **State the purpose:** explain what the code accomplishes in one sentence.
3. **Choose one example:** define inputs, necessary assumptions, units, and expected output.
4. **Follow the transitions:** place before/after states beside the operations that cause them; explain why order matters.
5. **Expose non-obvious behavior:** explain relevant side effects, boundaries, failure paths, snapshots, or aliases.
6. **Close the loop:** connect the result to the fixture, verify the explanation, and check the patch for unintended changes.

Concrete problems discovered during the walkthrough are reported separately with evidence and a suggested correction. An annotation request does not automatically authorize a fix or refactor.

## Preferences

These are natural-language preferences, not CLI flags or a required configuration file.

| Preference | Example |
| --- | --- |
| Target | A file, function, method, query, or supplied snippet |
| Comment language | Detect automatically, or specify a language explicitly; independent of the programming language |
| Depth | Concise maintenance notes, focused walkthrough, detailed teaching |
| Background | Familiar with Java; new to reactive streams |
| Focus | Save/reset order, recursion, cancellation, table rows, range boundaries |
| Known concepts | Skip loops; explain ownership and lifetime |
| Cross-references | Stable example/step labels for a long method |

Programming language and comment language are independent. Within binding instructions, choose the comment language in this order:

1. The user's explicit language request for the current task.
2. The predominant language of meaningful comments in the target function, then nearby code in the same file.
3. The language of the user's current question, using the main request or established conversation preference when mixed.

Absent or mixed local comments fall back to the user's question, not automatically to English. Ignore code identifiers, sample strings, license boilerplate, and copied external text when detecting language. Reply in the user's conversation language; keep identifiers, APIs, literals, and exact output values intact. English and Chinese README files do not limit generated comments to those languages.

## Compatibility and limits

| Area | Scope |
| --- | --- |
| Agent integration | Plain `SKILL.md`, optional Codex UI metadata; no required MCP server, IDE, or model vendor |
| Programming languages | No language whitelist; adapt to the target language, dialect, and comment syntax |
| Sample coverage | Runnable examples illustrate state changes and verification; they are not a supported-language list |
| Comment languages | No language whitelist; infer from the request and local context, or follow an explicit choice |
| Reader level | General experience and local familiarity are considered separately |
| Formats without comments | Keep valid syntax; use an excerpt or authorized companion explanation |
| Behavior preservation | A constrained workflow and verification practice, not a mathematical guarantee |

TraceNotes sets no comment-line quota or ASCII-only restriction. It preserves file conventions and semantically active directives, avoids unrequested refactoring, and identifies unknown helper behavior or concurrency ordering instead of inventing results. See [language safety](references/language-safety.md).

There is no telemetry or background service in this repository. The host agent retains its own execution, privacy, and permission settings. The included examples do not imply that every programming language or host agent has been tested end to end.

## Repository layout

```text
TraceNotes/
  SKILL.md                     Agent instructions
  README.md                    English guide
  README.zh-CN.md               Chinese guide
  agents/openai.yaml           Optional Codex UI metadata
  references/                  Examples, safety notes, practice cases
  examples/                    Runnable before/after demonstration
  scripts/                     Validation and fixture checks
  docs/design.md               Design decisions and attribution
  .github/                     CI and contribution templates
  CONTRIBUTING.md
  SECURITY.md
  CHANGELOG.md
  LICENSE
```

## Validation

Using the skill requires no Python or Java installation. Repository maintenance requires Python 3.10+, Node.js, and JDK 17+:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python scripts/verify_examples.py
```

If necessary, select a JDK with `python scripts/verify_examples.py --java-home /path/to/jdk-21`.

Checks cover metadata, local documentation links, YAML configuration, Python before/after AST equivalence, fixture outputs, selected boundary cases, and controlled async ordering. GitHub Actions is configured to run on Linux and Windows.

These checks validate artifacts and concrete examples, not automatic skill selection or every model-generated annotation. [Practice cases](references/practice-cases.md) provide a qualitative rubric for evaluating real outputs.

## Contributing

Reproducible examples, language-specific corrections, and documentation improvements are welcome. Keep both READMEs aligned. Read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and the [changelog](CHANGELOG.md).

## Acknowledgments

- [github/awesome-copilot: add-educational-comments](https://github.com/github/awesome-copilot/blob/main/skills/add-educational-comments/SKILL.md): reader-aware teaching, configurable depth, and file preservation.
- [mohitagw15856/pm-claude-skills: code-explainer](https://github.com/mohitagw15856/pm-claude-skills/blob/main/skills/code-explainer/SKILL.md): purpose-first explanation, stepwise walkthrough, and non-obvious behavior.
- [anthropics/skills](https://github.com/anthropics/skills), [obra/superpowers](https://github.com/obra/superpowers), and [vercel-labs/skills](https://github.com/vercel-labs/skills): references for skill packaging, installation, and repository documentation.

The workflow and examples here are independently written. [Design notes](docs/design.md) document adopted ideas and deliberate differences. No affiliation or endorsement is implied.

## License

[MIT](LICENSE). Contributions use the same license.
