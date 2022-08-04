from typing import Optional, List, Tuple

from overload import Overload

overload = Overload(debug=True)


class TestArrays:
    @overload
    def fetch(self, a: Optional[List] = None) -> List:
        return list()

    @overload
    def fetch(self, a: List) -> List:
        return list()

    @overload
    def fetch(self, a: Tuple) -> Tuple:
        return tuple()


t = TestArrays()
# TODO t.fetch(None) works
print(t.fetch(None))
# TODO t.fetch(None) TypeError: TestArrays.fetch()
#       missing 1 required positional argument: 'a'
#       bug details inside of overload.__call__
print(t.fetch())

# print(t.fetch(list()))
# print(t.fetch(tuple()))
