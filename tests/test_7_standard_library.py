def test_functools() -> None:
    import functools
    import operator

    def sum(x: int, y: int) -> int:
        return x + y

    f = functools.partial(sum, y=10)
    assert f(1) == 11

    assert functools.reduce(operator.add, [1, 2, 3]) == 6
    assert functools.reduce(operator.truediv, [18, 3, 3]) == 2  # (18 / 3) / 3 = 2


def test_itertools() -> None:
    import itertools

    count_it = itertools.count(10, 5)
    assert next(count_it) == 10
    assert next(count_it) == 15
    assert next(count_it) == 20

    cycle_it = itertools.cycle([1, 2])
    assert next(cycle_it) == 1
    assert next(cycle_it) == 2
    assert next(cycle_it) == 1
    assert next(cycle_it) == 2

    chain_it = itertools.chain(["a"], (1,))
    assert next(chain_it) == "a"
    assert next(chain_it) == 1


def test_asyncio() -> None:
    import asyncio
    from collections.abc import AsyncGenerator

    sleep = 0

    async def async_generator(value: int) -> AsyncGenerator[int, None]:
        for i in reversed(range(value)):
            await asyncio.sleep(sleep)
            yield i

    async def coroutine() -> None:
        await asyncio.sleep(sleep)

        values: list[int] = []
        async for x in async_generator(2):
            values.append(x)
        assert values == [1, 0]

        # Asynchronous generator comprehension
        generator = (-1 * i async for i in async_generator(2))
        # Asynchronous list comprehension
        values = [i async for i in generator]
        assert values == [-1, 0]

        # An asynchronous context manager is a context manager that is able to
        # suspend execution in its enter and exit methods
        # async with EXPRESSION as TARGET:
        #     SUITE

    asyncio.run(coroutine())


def test_regex():
    import re
    from collections.abc import Iterator

    # Gready
    # {m}   -> m repetitions
    # {m,n} -> from m to n repetitions
    # *     -> {0,}
    # +     -> {1,}
    # ?     -> {0,1}
    # Non-gready
    # {m,n}?    *?    +?    ??
    # \b -> matches the empty string, but only at the beginning or end of a word
    # \B -> matches the empty string, but only when it is not at the beginning or end of a word
    # ____________________________________________________________________________________
    # Determine if the RE matches at the beginning of the string.

    if match := re.match(r"abc", "abc-def-abc"):
        assert match.group() == "abc"
        assert match.span() == (0, 3)
    else:
        assert False

    # ____________________________________________________________________________________
    # Scan through a string, looking for any location where this RE matches.

    if match := re.search(r"abc", "def-abc-abc"):
        assert match.group() == "abc"
        assert match.span() == (4, 7)
    else:
        assert False

    # ____________________________________________________________________________________
    # Find all substrings where the RE matches, and returns them as an iterator

    it: Iterator[re.Match[str]] = re.finditer(r"abc", "abc-def-abc")
    assert [match.span() for match in it] == [(0, 3), (8, 11)]

    # ____________________________________________________________________________________
    # IGNORECASE mode

    regex, string = r"abc", "ABC-def-abc"
    assert re.findall(regex, string) == ["abc"]
    assert re.findall(regex, string, re.IGNORECASE) == ["ABC", "abc"]

    # ____________________________________________________________________________________
    # DOTALL mode
    # .     ->  any character except a newline
    #           in DOTALL mode -> also matches a newline

    regex, string = r".*", "a\nb"
    assert re.findall(regex, string) == ["a", "", "b", ""]
    assert re.findall(regex, string, re.DOTALL) == ["a\nb", ""]

    # ____________________________________________________________________________________
    # ASCII mode

    regex, string = r"\w+", "perché"
    assert re.findall(regex, string) == ["perché"]
    assert re.findall(regex, string, re.ASCII) == ["perch"]

    # ____________________________________________________________________________________
    # MULTILINE mode
    # ^     ->  the start of the string
    #           in MULTILINE mode -> also matches immediately after each newline
    # $     ->  the end of the string or just before the newline at the end of the string
    #           in MULTILINE mode -> also matches before a newline
    # \A    ->  matches only at the start of the string
    # \Z    ->  matches only at the end of the string

    regex, string = r"^.*", "a\nb"
    assert re.findall(regex, string) == ["a"]
    assert re.findall(regex, string, re.MULTILINE) == ["a", "b"]

    # ____________________________________________________________________________________
    # Verbose mode
    # Whitespace in the regular expression that isn’t inside a character class
    # is ignored

    regex = r"""
        \w+ # matches Unicode word characters
    """
    assert re.findall(regex, "abc-def-abc", re.VERBOSE) == ["abc", "def", "abc"]

    # ____________________________________________________________________________________
    # Grouping

    regex, string = r"(\d)-(\d)", "1-2 3-4"
    assert re.findall(regex, string) == [("1", "2"), ("3", "4")]

    # Named Groups
    regex = r"(?P<num1>\d)-(?P<num2>\d)"
    match = next(re.finditer(regex, string))
    assert match.groupdict() == {"num1": "1", "num2": "2"}
    assert match.group("num1") == "1"

    # ----------------------------------------
    # Backreferences

    regex, string = r"(\d)-\1", "1-2 3-3"
    assert re.findall(regex, string) == ["3"]

    # Named Groups
    regex = r"(?P<num>\d)-(?P=num)"
    it = re.finditer(regex, string)
    y = next(it)
    assert y.group("num") == "3"

    # ----------------------------------------
    # Non-capturing

    if match := re.search(r"(\d)+", "z 1223"):
        assert match.groups() == ("3",)
    else:
        assert False

    if match := re.search(r"(?:\d)", "z 1223"):
        assert match.groups() == ()
    else:
        assert False

    # ----------------------------------------
    # Lookahead Assertions
    # (?=...) -> Positive lookahead assertion
    # (?!...) -> Negative lookahead assertion

    regex = "1(?!-$).*"
    assert re.findall(regex, "1-") == []
    assert re.findall(regex, "1--") == ["1--"]

    # ____________________________________________________________________________________
    # Split strings

    assert re.split("-", "abc-def-ghi") == ["abc", "def", "ghi"]

    # ____________________________________________________________________________________
    # Search and Replace

    assert re.sub("-", "|", "abc-def-ghi") == "abc|def|ghi"
    assert re.subn("-", "|", "abc-def-ghi") == ("abc|def|ghi", 2)

    regex = r"(?P<num1>\d)-(?P<num2>\d)"
    repl = r"\g<num2>-\g<num1>"
    string = "1-2 3-4"
    result = "2-1 4-3"

    assert re.sub(regex, repl, string) == result
    assert (
        re.sub(regex, lambda m: m.group("num2") + "-" + m.group("num1"), string)
        == result
    )
