def type_strings() -> None:
    a_string: str = "Hello, world!"
    a_string = '"'
    a_string = """\
a
b\
c
"""

    assert len("AB") == 2
    assert "AB"[0] == "A"
    assert "abc"[2:] == "c"

    # Unicode
    assert "\U0001F1EE\U0001F1F9" == "🇮🇹"

    # Raw strings
    assert r"\n" == "\\n"

    # Formatted strings
    assert f"{1+2}-A" == "3-A"
    assert f"{1+2 = }-A" == "1+2 = 3-A"
    # conversion fields
    assert f"{'à'!s}" == "à"  # it calls str()
    assert f"{'à'!r}" == "'à'"  # it calls repr()
    assert f"{'à'!a}" == "'\\xe0'"  # it calls ascii()
    # format specifier
    assert f"{123.456:7.5}" == " 123.46"
    assert f"{16:#0x}" == "0x10"

    # formatted raw string
    assert fr"{1}-A\n" == "1-A\\n"

    # Concatenate
    assert "A" "B" == "AB"
    assert "A" + "B" == "AB"
    assert "".join(["A", "B"]) == "AB"  # recommended idiom

    # Format
    assert "{0} - {1}".format("A", "B") == "A - B"
    assert "{A} - {B}".format(A="A", B="B") == "A - B"


def type_bytes() -> None:
    bytes_value: bytes = b"Hello, world!"
    raw_bytes_value: bytes = rb"Hello, world!"


def type_tuples() -> None:
    tuple_1: tuple = ()
    assert tuple_1 == ()

    tuple_2 = (1,)
    assert tuple_2[0] == 1

    assert tuple_2 + (2, 3) == (1, 2, 3)

    a, b, c = 1, 2, 3
    a, *l, c = 1, 2, 3, 4
    assert l == [2, 3]

    assert tuple([1, 2, 3]) == (1, 2, 3)
    assert tuple(tuple_1) is tuple_1  # It does not make a copy


def type_lists() -> None:
    a_list: list[int] = []
    a_list = [1, 2, 3, 4]

    assert a_list[0] == 1
    assert a_list[-1] == 4
    assert a_list[0:2] == [1, 2]
    assert a_list[:2] == [1, 2]
    assert a_list[::2] == [1, 3]  # step
    assert a_list[::-1] == [4, 3, 2, 1]  # negative step
    assert a_list[1::-1] == [2, 1]  # negative step
    assert a_list[:1:-1] == [4, 3]  # negative step
    assert a_list[-2:1:-2] == [3]  # negative step

    # In
    assert 1 in a_list

    # Is
    a_list2 = a_list
    assert a_list2 is a_list
    assert a_list[:] is not a_list  # copy
    assert list(a_list) is not a_list  # copy

    # Append
    a_list.append(5)

    # Delete
    a_list = [1, 2, 3, 4]
    del a_list[2]
    assert a_list == [1, 2, 4]

    # Remove
    a_list = [1, 2, 3, 4]
    a_list.remove(4)
    assert a_list == [1, 2, 3]

    # List comprehension
    assert [x for x in [3, 4, 5, 6, 7] if x > 5] == [6, 7]
    assert [j for i in [1, 2] for j in range(i)] == [0, 0, 1]


def type_dictionaries() -> None:
    dictionary: dict[str, int] = {}

    a_dict = dict(one=1, two=2, three=3)
    a_dict = {"one": 1, "two": 2, "three": 3}
    assert list(a_dict) == ["one", "two", "three"]

    # Iterate
    for key, value in a_dict.items():
        pass

    # Get & Set
    assert a_dict["one"] == 1
    assert a_dict.get("one") == 1

    # a_dict["four"] # Error
    assert a_dict.get("four") == None
    assert a_dict.get("four", 4) == 4

    # Set default
    # If the key does not exist, insert the key
    a_dict.setdefault("five", 5)
    assert a_dict.get("five") == 5
    a_dict.setdefault("five", 6)
    assert a_dict.get("five") == 5

    # Delete
    del a_dict["one"]
    assert a_dict.get("one") == None

    # Dictionary comprehension
    assert {x: x ** 2 for x in range(5)} == {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}


def type_sets() -> None:
    a_set: set[int] = set()
    a_set = {1, 1, 2, 2, 3, 4}
    a_set.add(2)

    assert a_set & {4, 2} == {2, 4}

    # Set comprehensions
    assert {x for x in "abcddeef" if x not in "abc"} == {"d", "e", "f"}
