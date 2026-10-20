# Contributing to TraceNotes

Thank you for helping make difficult code easier to understand. Contributions may be in English or Chinese; include enough context for another maintainer to reproduce the issue. Keep code identifiers and implementation comments in English unless a worked example intentionally demonstrates Simplified Chinese comments. Programming languages have no whitelist; either maintained comment language can be used with any implementation language.

## Useful contributions

- A small implementation whose existing explanation is misleading or incomplete.
- A correction to a worked example's state, units, ordering, or assumptions.
- Language-specific annotation hazards supported by a reproducible example or primary documentation.
- Clearer wording, translations, or a focused improvement based on observed agent output.

## Before opening a pull request

1. Explain the reader's concrete confusion and the proposed improvement.
2. Keep the skill focused on educational annotations. Avoid unrelated refactoring or universal rules inferred from a single example.
3. Preserve the same fixture throughout a walkthrough and separate edge cases.
4. Update both `README.md` and `README.zh-CN.md` when user-facing behavior changes.
5. Run the checks below and report exactly what ran. If a runtime is unavailable, state which check was skipped.

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python scripts/verify_examples.py
```

The fixture suite requires Python 3.10+, Node.js, and JDK 17+. Use `--java-home` to select a JDK when needed. The scripts operate on the repository and temporary fixtures, not production services.

For skill-behavior changes, also try an appropriate scenario from [practice cases](references/practice-cases.md). Include the actual prompt, relevant input, output excerpt, and observed result. Passing a fixture suite does not demonstrate that a model follows a new instruction.

## Reporting problems

Use a minimal, fictional reproduction. Include the programming language/runtime, requested comment language, relevant repository rules, expected explanation, actual output, and checks performed. Never include secrets, customer data, or private source code without authorization. Follow [SECURITY.md](SECURITY.md) for sensitive issues.

## Review and conduct

Discuss evidence and code behavior, not the contributor's identity or background. Be respectful across experience levels and languages. Maintainers may request a smaller example, revise wording, or decline scope expansion.

Contributions are licensed under the repository's [MIT License](LICENSE).
