"""Execute the published examples using local runtimes without external services."""

import argparse
import ast
import os
import json
import re
import shutil
import sqlite3
import subprocess
import tempfile
from pathlib import Path


def run_checked(command):
    completed = subprocess.run(
        command, check=True, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=60,
    )
    return completed.stdout.strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--java-home", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    if args.java_home is None:
        if os.environ.get("JAVA_HOME"):
            args.java_home = Path(os.environ["JAVA_HOME"])
        elif shutil.which("javac"):
            args.java_home = Path(shutil.which("javac")).resolve().parent.parent
        else:
            parser.error("JDK 17+ is required; provide --java-home or configure JAVA_HOME")
    document = (args.skill / "references/worked-examples.md").read_text(encoding="utf-8")
    blocks = dict(re.findall(r"^```(java|python|javascript|sql|json)\n(.*?)^```", document, re.M | re.S))
    results = []
    before = (args.skill / "examples/batching.before.py").read_text(encoding="utf-8")
    after = (args.skill / "examples/batching.after.py").read_text(encoding="utf-8")
    assert ast.dump(ast.parse(before), include_attributes=False) == ast.dump(ast.parse(after), include_attributes=False)
    for source_code in (before, after):
        scope = {}
        exec(compile(source_code, "<batching-demonstration>", "exec"), scope)
        pack = scope["pack"]
        assert pack(["AA", "BBB", "C", "DDDD"], 5) == [["AA", "BBB"], ["C", "DDDD"]]
        assert pack([], 5) == []
        assert pack(["AAAAA", "B"], 5) == [["AAAAA"], ["B"]]
        assert pack(["AAAAAA"], 5) == [["AAAAAA"]]
    results.append({"language": "Python before/after", "checks": 9, "result": "same AST; 4 behavior cases per version"})

    namespace = {}
    exec(compile(blocks["python"], "<published-python-example>", "exec"), namespace)
    averages = namespace["moving_averages"]
    assert averages([2, 4, 6, 8], 2) == [3.0, 5.0, 7.0]
    assert averages([2], 2) == []
    assert averages([], 2) == []
    assert averages([2, 4], 1) == [2.0, 4.0]
    results.append({"language": "Python", "comment_language": "English", "checks": 4, "result": [3.0, 5.0, 7.0]})

    with sqlite3.connect(":memory:") as connection:
        rows = connection.execute(blocks["sql"]).fetchall()
    assert rows == [("A", "p1", 8), ("B", "p3", 6)]
    results.append({"language": "SQL/SQLite", "comment_language": "Simplified Chinese", "checks": 1, "result": rows})

    json_value = json.loads(blocks["json"])
    assert json_value == {"retries": 2, "timeoutMs": 500}
    results.append({"language": "strict JSON", "checks": 1, "result": "valid; no comments inserted"})

    with tempfile.TemporaryDirectory(prefix="example-comments-check-") as directory:
        working = Path(directory)
        java_source = working / "BatchExample.java"
        java_source.write_text(blocks["java"], encoding="utf-8")
        probe = working / "BatchProbe.java"
        probe.write_text('''import java.util.List;
class BatchProbe {
    static void equal(Object actual, Object expected) {
        if (!actual.equals(expected)) throw new AssertionError(actual + " != " + expected);
    }
    public static void main(String[] args) {
        equal(BatchExample.pack(List.of("AA", "BBB", "C", "DDDD"), 5),
              List.of(List.of("AA", "BBB"), List.of("C", "DDDD")));
        equal(BatchExample.pack(List.of(), 5), List.of());
        equal(BatchExample.pack(List.of("AAAAA", "B"), 5),
              List.of(List.of("AAAAA"), List.of("B")));
        equal(BatchExample.pack(List.of("AAAAAA"), 5), List.of(List.of("AAAAAA")));
        System.out.println("4 Java checks passed");
    }
}
''', encoding="utf-8")
        suffix = ".exe" if (args.java_home / "bin/javac.exe").exists() else ""
        javac = args.java_home / f"bin/javac{suffix}"
        java = args.java_home / f"bin/java{suffix}"
        run_checked([str(javac), "-encoding", "UTF-8", str(java_source), str(probe)])
        output = run_checked([str(java), "-cp", str(working), "BatchProbe"])
        results.append({"language": "Java", "comment_language": "Simplified Chinese", "checks": 4, "result": output})

        node = shutil.which("node")
        if node is None:
            raise RuntimeError("Node.js is required for the JavaScript example check")
        js_probe = working / "probe.mjs"
        js_probe.write_text(blocks["javascript"] + '''
import assert from 'node:assert/strict';
const deferred = new Map();
const completed = [];
const result = loadLabels(['a', 'b'], id => new Promise(resolve => {
    deferred.set(id, label => { completed.push(id); resolve(label); });
}));
deferred.get('b')('B');
await Promise.resolve();
deferred.get('a')('A');
assert.deepEqual(await result, [{id:'a', label:'A'}, {id:'b', label:'B'}]);
assert.deepEqual(completed, ['b', 'a']);
assert.deepEqual(await loadLabels([], async id => id), []);
const failure = new Error('fixture failure');
let finishSecond;
let secondCompleted = false;
const rejected = loadLabels(['a', 'b'], id => {
    if (id === 'a') return Promise.reject(failure);
    return new Promise(resolve => {
        finishSecond = () => { secondCompleted = true; resolve('B'); };
    });
});
await assert.rejects(rejected, error => error === failure);
finishSecond();
assert.equal(secondCompleted, true);
console.log('5 JavaScript checks passed');
''', encoding="utf-8")
        output = run_checked([node, str(js_probe)])
        results.append({"language": "JavaScript", "comment_language": "English", "checks": 5, "result": output})

    report = {
        "status": "passed",
        "checks": sum(item["checks"] for item in results),
        "results": results,
        "limits": "Checks validate these published fixtures and selected boundaries, not every programming language or automatic skill-trigger quality.",
    }
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
