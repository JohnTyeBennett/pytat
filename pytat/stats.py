from math import sqrt

def ratio(numerator, denominator):
    if denominator == 0:
        return None
    return float(numerator) / denominator

def mean(values):
    return ratio(sum(values), len(values))

def median(values):
    if len(values) == 0:
        return None
    elif len(values) == 1:
        return values[0]
    else:
        n1 = (len(values) - 1) / 2
        n2 = len(values) / 2 + 1
        return mean(sorted(values)[n1:n2])

def stddev(values):
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return sqrt(ratio(sum([(x - m) ** 2 for x in values]), len(values) - 1))

def correlation(x, y):
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum([e[0] * e[1] for e in zip(x, y)])
    sum_x2 = sum([e ** 2 for e in x])
    sum_y2 = sum([e ** 2 for e in y])
    n = len(x)
    correlation = ratio(n * sum_xy - sum_x * sum_y, sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)))
    return correlation

def sma(values, period):
    new_values = []
    for i in xrange(len(values)):
        if i < period - 1:
            new_values.append(None)
        else:
            new_values.append(mean(values[i - period + 1:i + 1]))
    return new_values

def ema(values, period):
    new_values = []
    k = 2.0 / (period + 1)
    new_values = sma(values[0:period], period)
    for value in values[period:]:
        new_values.append(k * value + (1 - k) * new_values[-1])
    return new_values

def best_fit(points):
    sum_xy = float(sum([p[0] * p[1] for p in points]))
    sum_x = float(sum([p[0] for p in points]))
    sum_y = float(sum([p[1] for p in points]))
    sum_x2 = float(sum([p[0] * p[0] for p in points]))
    n = len(points)
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    intercept = (sum_y - slope * sum_x) / n
    return (slope, intercept)
