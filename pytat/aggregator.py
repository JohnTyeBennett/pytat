def object_key(key_fields):
    return lambda obj: tuple(getattr(obj, field) for field in key_fields)

class Accumulator(object):

    def accumulate(self, item): pass
    def final_value(self): pass

class ListAccumulator(Accumulator):

    def __init__(self):
        super(ListAccumulator, self).__init__()
        self.items = []

    def accumulate(self, item):
        self.items.append(item)

    def final_value(self):
        return self.items

class MaxAccumulator(Accumulator):

    def __init__(self):
        super(MaxAccumulator, self).__init__()
        self.value = None

    def accumulate(self, item):
        if self.value == None or item > self.value:
            self.value = item

    def final_value(self):
        return self.value

class MinAccumulator(Accumulator):

    def __init__(self):
        super(MinAccumulator, self).__init__()
        self.value = None

    def accumulate(self, item):
        if self.value == None or item < self.value:
            self.value = item

    def final_value(self):
        return self.value

class MeanAccumulator(Accumulator):

    def __init__(self):
        super(MeanAccumulator, self).__init__()
        self.sum = 0.0
        self.count = 0
    
    def accumulate(self, item):
        self.sum += item
        self.count += 1

    def final_value(self):
        return self.sum / self.count

class Aggregator(object):

    def __init__(self, key_func, accumulator_class = ListAccumulator, value_func = lambda x: x):
        self.key_func = key_func
        self.accumulator_class = accumulator_class
        self.value_func = value_func

    def aggregate(self, items):
        accumulators = []
        key = None
        for item in sorted(items, cmp = lambda a, b: cmp(self.key_func(a), self.key_func(b))):
            item_key = self.key_func(item)
            if item_key != key:
                key = item_key
                accumulator = self.accumulator_class()
                accumulators.append((key, accumulator))
            accumulator.accumulate(self.value_func(item))
        return [(key, accumulator.final_value()) for key, accumulator in accumulators]
