---
name: trace-notes
description: "Add or improve learning-oriented code comments using one concrete input, intermediate state changes, and an expected output. Use when someone asks for educational inline annotations, an example-based walkthrough written into code, or clearer explanations of complex methods. Adapt to the programming language and the reader's natural language. Preserve behavior; do not use for routine API documentation, PR review comments, or general refactoring."
---

# TraceNotes

Make the implementation readable by following a small, concrete example through its actual control flow. Show how data changes, why order matters, and how the final result is produced.

Start with one sentence stating the code's purpose. In a source-editing task, place it near the relevant function or block using an ordinary comment unless a documentation change is requested. In an explanation-only task, put it before the annotated excerpt.

## Scope and defaults

- When asked to add comments to a file, edit that file within the authorized scope. When asked only to explain code, return an annotated excerpt without silently editing files.
- Infer the target from the request and available context. Ask only if multiple plausible targets would lead to materially different work.
- Default to a focused learning walkthrough: enough detail to reconstruct the important operations without narrating every statement. Honor requests for dense line-level teaching or concise production comments.
- Adapt to any programming language you can accurately read; inspect its actual dialect, runtime, and comment rules. Do not promise tested support for every language.
- Do not require a particular IDE, MCP server, model vendor, framework, operating system, or external service. Use symbol navigation when available and ordinary search/read tools otherwise.

## 1. Read before explaining

1. Read applicable repository instructions, the target implementation, its caller, and any helpers that materially determine the behavior. Inspect relevant tests and configuration.
2. Record the actual contract: inputs, output, mutation, errors, units, bounds, and configuration defaults. Distinguish an example parameter from a production default.
3. Locate the difficult transitions: branching, accumulation, stack updates, flushing, copying, recursion, async boundaries, transaction boundaries, retries, or cleanup.
4. Treat existing comments and external documentation as claims to verify. Report a discovered bug separately; do not silently repair it in an annotation-only task.
5. For a fragment, explain the visible behavior and explicitly mark missing contracts or helper behavior. A useful partial explanation is better than inventing a complete execution trace.

## 2. Choose language and depth

Treat the programming language and the explanation language as independent choices.

- Follow applicable instruction priority. Within that hierarchy, use the explicitly requested comment language; otherwise follow repository comment-language rules, then the reader's conversation language.
- Preserve identifiers, API names, literal inputs, and exact outputs. Translate explanatory prose, not the implementation. Explain unfamiliar terms briefly in the chosen natural language.
- Infer knowledge from the reader's question and stated experience. An experienced engineer may still need a detailed walkthrough of an unfamiliar domain.
- Distinguish general technical experience from familiarity with this language, framework, or subsystem. Define concepts the reader lacks and skip concepts they already know.
- Use neutral fictional data. Avoid nationality-based assumptions, culture-dependent metaphors, secrets, real customer data, and personal paths in portable examples.
- Support Unicode where the file encoding and toolchain support it. Preserve encoding, newline style, and indentation; do not impose ASCII-only prose or a comment-line quota.

Use these optional preferences when stated; infer reasonable defaults rather than asking a setup questionnaire. They are natural-language instructions, not implemented CLI flags.

| Preference | Default and adaptation |
| --- | --- |
| Target | The file, symbol, or snippet identified by context |
| Comment language | Explicit request, then repository policy, then conversation language, subject to instruction priority |
| Depth | Focused walkthrough; concise for maintenance, detailed for unfamiliar transitions |
| Reader background | Infer general experience and local familiarity separately |
| Focus / known concepts | Emphasize the stated confusion; avoid reteaching known material |
| Cross-references | Use stable labels such as `Example A` or `Step 2` only when they connect distant blocks; avoid embedded physical line numbers |

## 3. Build one coherent example

Choose the smallest input that reveals the difficult behavior, usually 3-5 items or 2-3 meaningful transitions. Do not reduce an essential domain rule to an inaccurate toy model.

At the method's start, or immediately before the relevant block, introduce:

```text
Example input: <exact values>
Assumptions: <only those needed; units and configuration>
Expected output: <exact result or explicitly illustrative shape>
Key question: <the behavior this example makes visible>
```

Use the target language's native comment syntax, not the plain-text wrapper above. A short example needs only a few lines. For a long method, put the initial fixture once and refer to it by a stable example label.

- Keep the same values, IDs, ordering, and assumptions throughout the main walkthrough.
- If generated IDs or external responses cannot be predicted, use clearly labeled aliases or mock values. Do not invent actual runtime results.
- Separate edge-case examples from the main trace. Do not force one input to cover every branch.
- For unknown helper behavior, inspect it or state the precise uncertainty. Do not fabricate its output to complete the story.

## 4. Attach state changes to decisive code

Write comments next to the operations that cause the change. Prefer:

```text
Before: <relevant state>
This operation: <actual effect and reason>
After: <new state>; <why the next operation is now correct>
```

Use that structure as a thinking aid, not mandatory headings on every comment. Keep comments idiomatic and readable in the chosen language.

Focus on these questions where relevant:

| Mechanism | What the comments should make concrete |
| --- | --- |
| Loop or accumulator | Which iteration matters; current item; collection before/after |
| Flush and reset | What is saved first; what is cleared next; why the order matters |
| Copy or reference | Snapshot versus alias; whether later mutation changes earlier output |
| Stack or hierarchy | Which entries are removed/retained; resulting parent path |
| Split or range | Exact units; inclusive/exclusive ends; local versus global offsets |
| Recursion | Current arguments; smaller subproblem; return value combined by caller |
| Functional/declarative code | Input/output transformations and invariants, without inventing imperative execution order |
| Async or concurrent code | Guaranteed ordering versus one possible schedule; cancellation and ownership |
| Query or transaction | Sample rows; logical stages; filtering/order/commit effects guaranteed by the code |
| Error path | Trigger; returned/thrown result; retries or cleanup only if actually implemented |

At the return or final commit, tie the result back to the fixture: exact records/counts, observable side effects, and the verified downstream consumer when useful. Do not invent a consumer.

Surface non-obvious behavior that helps this reader: mutation, dependencies, resource lifetime, failure propagation, and performance costs when grounded in the implementation. Keep these notes beside the relevant operation; do not turn every annotation task into a broad code review.

Explain reasons that follow from code, tests, or documented contracts. Label an inferred design rationale as an inference rather than the author's proven intent.

## 5. Keep annotation changes safe

Before editing unfamiliar syntax or special files, read [Language and file safety](references/language-safety.md).

- Preserve executable behavior, identifiers, imports, literals, declarations, and existing unrelated changes. Do not refactor, add logging, insert runtime assertions, or change error handling just to fit the example.
- Preserve license notices and semantically active comments/directives. Comments can affect tools and compilation; Python docstrings are not ordinary comments.
- Avoid global reformatting. Prefer separate comment lines near important operations over long trailing prose on every line.
- Improve existing walkthroughs rather than duplicating them or growing them on every invocation.
- If the format does not permit comments, use a nearby annotated excerpt or an authorized companion document. Never make strict JSON invalid by inserting comments.

## 6. Verify both the explanation and the patch

1. Recompute the fixture through the actual implementation. Check arithmetic, counts, ordering, range endpoints, units, aliases, and early returns.
2. Run a relevant existing test or a safe minimal example when practical. Do not execute untrusted code or call production services merely to verify comments.
3. Inspect the diff against the pre-edit version. Use a language-aware parser/token comparison when available to check that executable structure is preserved. Do not use a universal regex to strip comments across languages.
4. Run syntax/build checks appropriate to the touched file if comment placement or encoding could affect parsing. Avoid broad unrelated test runs for ordinary comment-only changes.
5. Clearly distinguish executed results from manually traced examples. Never report validation that was not run, and do not add a runtime-verification claim to source comments unless maintainers requested it.

Completion criteria:

- The reader can follow one input to its result at the relevant source lines.
- Important intermediate states agree with the implementation.
- The chosen natural language and comment syntax fit the reader and repository.
- The patch stays within the requested annotation scope.

Report the changed files/symbols, the behavior the example clarifies, and the checks actually performed. Link the first useful source line when the environment supports file links. If a concrete problem was found, give its trigger, evidence, consequence, and a suggested correction separately; do not apply that correction without scope to change behavior. Do not manufacture findings or imply that an annotation pass is an exhaustive audit.

## Supporting material

- [Worked examples](references/worked-examples.md): Java/Chinese, Python/English, JavaScript/Spanish, and SQL/French; adapt the method instead of copying a language blindly.
- [Language and file safety](references/language-safety.md): syntax hazards, units, ordering, and safe fallbacks.
- [Practice cases](references/practice-cases.md): prompts and review criteria for trying the skill on new tasks; these are not a claim of measured benchmark performance.
