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

def align_delete(key_func, xs1, xs2):
    current = 0
    while current < len(xs1) and current < len(xs2):
        key1 = key_func(xs1[current])
        key2 = key_func(xs2[current])
        if key1 < key2:
            xs1.pop(current)
        elif key1 > key2:
            xs2.pop(current)
        else:
            current += 1
    if current < len(xs1):
        for i in xrange(len(xs1) - current):
            xs1.pop()
    elif current < len(xs2):
        for i in xrange(len(xs2) - current):
            xs2.pop()
