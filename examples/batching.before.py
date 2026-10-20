def pack(items, limit):
    result = []
    current = []
    used = 0
    for item in items:
        if current and used + len(item) > limit:
            result.append(current.copy())
            current.clear()
            used = 0
        current.append(item)
        used += len(item)
    if current:
        result.append(current.copy())
    return result
