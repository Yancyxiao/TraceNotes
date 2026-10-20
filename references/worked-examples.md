# Worked examples

These original examples demonstrate a portable method, not a programming-language whitelist or prescribed language pairing. Comments may be English or Simplified Chinese for any programming language; the sample choices below are interchangeable. In an actual repository, annotate its implementation and follow its contract. Do not replace it with these algorithms.

## Batch accumulation: flush, snapshot, then reset (Java example)

The reader knows Java syntax but wants to understand why saving the batch happens before clearing it. The caller guarantees `limit > 0`, non-null strings, and each item length no greater than `limit`.

```java
import java.util.ArrayList;
import java.util.List;

class BatchExample {
    static List<List<String>> pack(List<String> items, int limit) {
        // 贯穿示例：items=["AA", "BBB", "C", "DDDD"]，limit=5。
        // 长度按 String.length() 的 UTF-16 代码单元计算，本例均为 ASCII。
        // 预期结果：[["AA", "BBB"], ["C", "DDDD"]]，原有顺序不变。
        List<List<String>> result = new ArrayList<>();
        List<String> current = new ArrayList<>();
        int used = 0;

        for (String item : items) {
            // 前两个元素放入后：current=["AA", "BBB"]，used=5。
            // 轮到 "C"：5+1>5，必须先保存上一批，再开始装下一批。
            if (!current.isEmpty() && used + item.length() > limit) {
                // 保存 current 的副本：result 从 [] 变为 [["AA", "BBB"]]。
                // 后面清空 current 时，已保存的这一批仍保留两个元素。
                result.add(new ArrayList<>(current));
                current.clear();
                used = 0;
            }
            // "C" 在重置后进入新批次：current=["C"]，used=1。
            // 下一轮加入 "DDDD" 后：current=["C", "DDDD"]，used=5。
            current.add(item);
            used += item.length();
        }

        // 循环结束并不代表最后一批已经保存；这里补上它。
        if (!current.isEmpty()) {
            result.add(new ArrayList<>(current));
        }
        // 最终得到两批；空输入则不会保存任何批次，返回 []。
        return result;
    }
}
```

The example assumptions do not add validation to the method. For instance, the supplied implementation does not reject an oversized item; do not comment that it does.

## Trace a sliding window (Python example)

Assume `width` is a positive integer and `values` is a list of numbers.

```python
def moving_averages(values, width):
    # Example: values=[2, 4, 6, 8], width=2 -> [3.0, 5.0, 7.0].
    # Keep only the latest width values; emit nothing until the window is full.
    window = []
    total = 0
    result = []
    for value in values:
        window.append(value)
        total += value
        # On value=6: window=[2, 4, 6], total=12; remove the oldest 2.
        if len(window) > width:
            total -= window.pop(0)
        # The same iteration now has window=[4, 6], total=10 -> emit 5.0.
        # Earlier [2, 4] emitted 3.0; the next [6, 8] will emit 7.0.
        if len(window) == width:
            result.append(total / width)
    # A list shorter than width never fills the window and returns [].
    return result
```

Do not silently optimize `pop(0)` into a deque during an annotation-only task. An optimization is a separate change.

## Result order is not completion order (JavaScript example)

The reader understands promises but confuses request completion with array order. Assume `fetchLabel` is an async function.

```javascript
async function loadLabels(ids, fetchLabel) {
    // Example: ids=["a", "b"]. The test double resolves "b" before "a".
    // Expected: [{id:"a", label:"A"}, {id:"b", label:"B"}], in ids order.
    const pending = ids.map(async (id) => {
        // Each callback keeps its own id; others can advance while this one awaits.
        const label = await fetchLabel(id);
        return { id, label };
    });
    // pending contains promises rather than the final objects.
    // Promise.all preserves input order even when "b" completes first.
    // One rejection rejects the result; it does not cancel the other operations.
    return Promise.all(pending);
}
```

The earlier completion of `b` is a controlled fixture, not a universal guarantee. Do not annotate a fixed network schedule as fact.

## Intermediate rows and deterministic ranking (SQL example)

This self-contained query uses SQLite-compatible syntax. The extra tie-breaker is already part of the supplied query, not a refactor introduced while commenting.

```sql
WITH scores(team, person, points) AS (
    -- 贯穿示例：A 组有两个人分数相同，B 组有一个人。
    VALUES ('A', 'p1', 8), ('A', 'p2', 8), ('B', 'p3', 6)
), ranked AS (
    SELECT team, person, points,
           -- 排名后：A 组 p1 的 rn=1、p2 的 rn=2；B 组 p3 的 rn=1。
           -- 分数相同时按 person 排序，使本例中的名次确定。
           ROW_NUMBER() OVER (
               PARTITION BY team ORDER BY points DESC, person ASC
           ) AS rn
    FROM scores
)
-- 只保留 rn=1：得到 (A,p1,8) 和 (B,p3,6)，每组一行。
-- 最后的 ORDER BY 固定返回顺序，不依赖中间计算的行顺序。
SELECT team, person, points FROM ranked WHERE rn = 1 ORDER BY team;
```

In a real query, inspect schema and constraints before claiming uniqueness or deterministic tie-breaking. Do not execute a write query against production merely to check its comments.

## When comments cannot be inserted

For a strict JSON file, keep the file valid and show an explanation outside it:

```json
{"retries": 2, "timeoutMs": 500}
```

Explain the units and values in prose. Whether `retries=2` means two attempts or two retries depends on the consumer; read it before stating a total attempt count. If no consumer is available, identify that uncertainty instead of guessing.
