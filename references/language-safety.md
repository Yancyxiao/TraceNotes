# Language and file safety

Read the relevant rows before inserting comments into an unfamiliar language or format. This is a starting checklist, not an exhaustive language specification. Check the actual dialect when uncertain.

| Context | Annotation hazards and safe approach |
| --- | --- |
| Java, C, C++, C#, JavaScript, TypeScript | Use valid native comments outside literals. Do not nest block comments where unsupported. In Java, Unicode escape processing happens before ordinary comment parsing; do not put raw Unicode escape examples into comments carelessly. In JS/TS, preserve automatic-semicolon-insertion-sensitive line breaks and comment directives such as type-check suppressions. |
| Python | Prefer `#` comments for behavior-preserving educational additions. Triple-quoted strings can become runtime docstrings or expression statements. Preserve encoding declarations, type comments, indentation, and line continuations; do not insert a comment after an explicit continuation backslash. |
| Go, Rust | Preserve Go build constraints, generator directives, compiler-related comments, Rust doc comments/doctests, and attributes. Do not turn ordinary notes into documentation tests accidentally. Explain ownership or borrowing only according to the actual code. |
| Shell, PowerShell, Make | Preserve shebangs, here-document/here-string boundaries, quoting, escape/continuation rules, and significant recipe tabs. A `#` inside a quoted value or embedded script is not necessarily a source comment. |
| SQL | Check the database dialect. Preserve optimizer hints and executable comments. Explain logical data transformations, not a guaranteed physical query plan. Row order is unspecified without a sufficient `ORDER BY`; ties need an explicit tie-breaker if exact output order matters. |
| HTML, XML, templates, JSX, CSS | Respect nested-language boundaries and the applicable comment grammar. JSX expression comments differ from JavaScript statements. XML comments cannot contain a double hyphen. Preserve template/compiler directives. |
| Haskell, Lisp, R, Julia, Lua, Swift, Kotlin, other languages | Determine the actual line/block comment syntax and nesting rules first. Account for layout, macro expansion, multiline delimiters, and documentation forms. Do not guess comment syntax by analogy. |
| Strict JSON, notebook cell data, binary or generated artifacts | Strict JSON has no comments. Prefer an annotated excerpt/companion document or the editable generator source. Do not hand-edit generated files unless the task calls for it. Keep notebook JSON valid and use appropriate source/Markdown cells when authorized. |

## Units and indices

Always name the units used by the implementation when lengths affect the example:

- Java `String.length()` and JavaScript string `.length` count UTF-16 code units.
- Python `len(str)` counts Unicode code points; combining sequences can span several code points.
- Byte lengths, grapheme clusters, characters, and model tokens are not interchangeable.
- Use simple ASCII fixture strings when Unicode details would distract from an unrelated algorithm. Use a deliberate Unicode fixture when Unicode behavior is the learning goal.
- State whether a range is half-open, inclusive, local to a slice, or relative to the full input.

## Time and evaluation order

- Distinguish output order from completion order in async code. Label a hypothetical interleaving as one possible schedule.
- For lazy iterators, streams, reactive pipelines, or deferred queries, distinguish pipeline construction from consumption and side effects.
- For recursive or functional code, trace values and call/return dependencies without inventing mutable variables.
- For transactions, distinguish in-memory mutation, pending writes, committed state, rollback, and external side effects when the implementation makes those distinctions.

## Preservation checks

1. Save or otherwise establish the pre-edit version without resetting the user's work.
2. Inspect the diff for changes to executable tokens, strings, declarations, or directives.
3. Use the language's parser, tokenizer, formatter check mode, compiler, or focused existing tests as appropriate. Abstract syntax equality alone does not cover every tool directive, source-location dependency, or documentation effect.
4. Never use a regex-based universal comment stripper as evidence that arbitrary languages retain their behavior.
5. If tools are unavailable, perform a manual diff and trace review and state that limitation plainly. Do not imply successful compilation.
