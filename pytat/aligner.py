def align_add(key_func, placeholder_func, *lists):
    current = 0
    while current < max(len(xs) for xs in lists):
        repeat = False
        key = min(key_func(xs[current]) for xs in lists if len(xs) > current)
        for xs in lists:
            if current >= len(xs) or key_func(xs[current]) > key:
                repeat = True
                xs.insert(current, placeholder_func(key))
        if not repeat:
            current += 1

def align_delete(key_func, *lists):
    current = 0
    while current < min(len(xs) for xs in lists):
        repeat = False
        key = max(key_func(xs[current]) for xs in lists)
        for xs in lists:
            while current < len(xs) and key_func(xs[current]) < key:
                repeat = True
                xs.pop(current)
        if not repeat:
            current += 1
    for xs in lists:
        while len(xs) > current:
            xs.pop()
