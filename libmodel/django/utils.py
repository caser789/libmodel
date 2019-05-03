def static_module(n):
    """
    >>> class A:
    ...     m = static_module(10)
    ...
    >>> a = A()
    >>> a.m(12345)
    5
    """
    def func(num):
        return num % n
    return staticmethod(func)


def static_div(divisor):
    """
    >>> class A:
    ...     m = static_div(10)
    ...
    >>> a = A()
    >>> a.m(12345)
    1234
    """
    def func(divident):
        return divident // divisor
    return staticmethod(func)


def static_lower():
    """
    >>> class A:
    ...     m = static_lower()
    ...
    >>> a = A()
    >>> a.m('Hello')
    'hello'
    """
    def func(s):
        return s.lower()
    return staticmethod(func)


def static_upper():
    """
    >>> class A:
    ...     m = static_upper()
    ...
    >>> a = A()
    >>> a.m('Hello')
    'HELLO'
    """
    def func(s):
        return s.upper()
    return staticmethod(func)
