def aggregate(key_fields, items, accumulator = lambda x: x):
    class Entry(object):

        def __init__(self, key):
            self.key = key
            self.items = []

    class Key(object):

        def __cmp__(self, other):
            if other == None: return 1
            return cmp(self.__dict__.values(), other.__dict__.values())

        def __str__(self):
            return ','.join([str(x) for x in self.__dict__.values()])

    def key_for_item(item):
        key = Key()
        for key_field in key_fields:
            setattr(key, key_field, getattr(item, key_field))
        return key

    entry = None
    key = None
    entries = []
    for item in sorted(items, cmp = lambda a, b: cmp(key_for_item(a), key_for_item(b))):
        item_key = key_for_item(item)
        if item_key != key:
            key = item_key
            entry = Entry(item_key)
            entries.append(entry)
        entry.items.append(item)
    for entry in entries:
        entry.value = accumulator(entry.items)
    return entries
