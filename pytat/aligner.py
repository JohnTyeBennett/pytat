def align_add(key_func, xs1, xs2, placeholder_func = lambda key: None):
    current = 0
    while current < len(xs1) and current < len(xs2):
        key1 = key_func(xs1[current])
        key2 = key_func(xs2[current])
        if key1 < key2:
            xs2.insert(current, placeholder_func(key1))
        elif key1 > key2:
            xs1.insert(current, placeholder_func(key2))
        current += 1
    while current < len(xs1):
        xs2.append(placeholder_func(key_func(xs1[current])))
        current += 1
    while current < len(xs2):
        xs1.append(placeholder_func(key_func(xs2[current])))
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
