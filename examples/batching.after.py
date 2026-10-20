def pack(items, limit):
    # Group strings in order, starting a new batch when the next item would exceed limit.
    # Example: items=["AA", "BBB", "C", "DDDD"], limit=5.
    # Assume limit>0 and each item's length<=limit; this method does not validate them.
    # Expected: [["AA", "BBB"], ["C", "DDDD"]]. Python counts Unicode code points.
    result = []
    current = []
    used = 0
    for item in items:
        # After "AA" and "BBB": current=["AA", "BBB"], used=5.
        # On "C", 5+1>5: save the previous batch before starting another.
        if current and used + len(item) > limit:
            # Save a snapshot: result becomes [["AA", "BBB"]].
            # Clearing current next will not erase this saved list.
            result.append(current.copy())
            current.clear()
            used = 0
        # "C" enters the empty batch; after "DDDD", current=["C", "DDDD"], used=5.
        current.append(item)
        used += len(item)
    # The final batch has no later item to trigger a flush; save it here.
    if current:
        result.append(current.copy())
    # Two independent batches; empty input returns [] without saving a batch.
    return result
