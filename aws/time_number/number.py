import random
import string
import sys
import uuid


__all__ = ['rand_int', 'rand_ints', 'random_num', 'random_cate', 'random_int', 'random_float', 'unique_key']


def rand_int(low, high):
    if low > high:
        raise Exception("arguments error, infra.rand_int: low should be less than high")
    return random.randint(low, high)


def rand_ints(low, high, num):
    result = []
    for i in range(num):
        result.append(rand_int(low, high))
    return result


def random_num(_len=8, rand=False):
    d1 = ''.join(random.sample(string.ascii_letters + string.digits, _len))
    d2 = str(random.randint(00000000, 99999999))
    if rand:
        return str(d1 + "-" + d2)
    return str(d1.lower() + "-" + d2)


def random_cate(cate, category):
    value = random.choice(category[cate])
    return value.upper()


def random_int(low=0, high=sys.maxsize):
    return random.randint(low, high)


def random_float(high, low=0):
    return round(random.random(low, high), 2)


def unique_key():
    return uuid.uuid4().hex
