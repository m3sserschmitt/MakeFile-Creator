from typing import Iterable


class Set(list):
    def __init__(self, iterable: Iterable = ()):
        super().__init__(iterable)

    def append(self, __object) -> None:
        if __object not in self:
            super().append(__object)

    def extend(self, __iterable: Iterable) -> None:
        for __item in __iterable:
            if __item not in self:
                super().append(__item)

    def update(self, __iterable: Iterable) -> None:
        self.extend(__iterable)

    def __setitem__(self, key, value):
        if value in self:
            raise Exception("Item already in list.")
        super().__setitem__(key, value)
