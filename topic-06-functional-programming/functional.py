# ( car '(1 2 3) ) -> 1
# ( cdr '(1 2 3) ) -> (2 3)

# ( cons (car x) (cdr x) ) --> x

def length(t):
    return len(t)

def first(t):
    if length(t) > 0:
        return t[0]
    else:
        return None

def tail(t):
    if length(t) > 0:
        return t[1:]
    else:
        return []

def construct(n, t):
    return [ n ] + t

def is_list(t):
    return type(t) is list

# stop defining primitives!

def concat(t, v):
    if length(t) == 0:
        return v
    else:
        return construct(first(t), concat(tail(t), v))

def lower(t, n):
    if length(t) == 0:
        return []
    else:
        if first(t) < n:
            return concat([first(t)], lower(tail(t),n))
        else:
            return lower(tail(t),n)


def upper(t, n):
    if length(t) == 0:
        return []
    else:
        if first(t) > n:
            return concat([first(t)], upper(tail(t), n))
        else:
            return upper(tail(t), n)


def equal(t, n):
    if length(t) == 0:
        return []
    else:
        if first(t) == n:
            return concat([first(t)], equal(tail(t), n))
        else:
            return equal(tail(t), n)


def sort(t):
    if length(t) <= 1:
        return t
    else:
        return concat(concat(sort(lower(t, first(t))), [first(t)]), sort(upper(t, first(t))))


def sort2(t):
    if length(t) <= 1:
        return t
    else:
        return concat(
            concat(sort2(lower(t, first(t))), equal(t,first(t))), sort2(upper(t, first(t)))
        )

def reverse(t):
    if length(t) == 0:
        return t
    else:
        return concat(reverse(tail(t)), [first(t)])

def mirror(t):
    print("t =", t)
    if not is_list(t):
        print("t is not a list")
        return t
    else:
        if length(t) == 0:
            return t
        else:
            return concat(mirror(tail(t)), [mirror(first(t))])


if __name__ == "__main__":
    print(concat([1, 2, 3], [4, 5, 6]))
    print(lower([1, 4, 2, 6, 3, 1, 7], 5))
    print(upper([1, 4, 2, 6, 3, 1, 7], 5))
    print(sort([1,4,6,7,8,9,3,5,2]))
    print(sort2([1, 4, 6, 7, 8, 9, 3, 4, 5, 2, 7]))
    print(sort2(["cat","apple","banana","dog","zebra","moose"]))
    print(reverse([1, 4, 6, 7, 8, 9, 3, 4, 5, 2, 7]))
    print(mirror([1, 4, [6, 7, [8, 9]], 3, 4, 5, 2, 7]))
    print()
