def checkIncremental(a):
    for i in range(2, len(a)):
        if (a[i]-a[i-1]) * (a[i - 1] - a[i - 2]) < 0:
            return False
    return True

