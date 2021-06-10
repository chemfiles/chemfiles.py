from typing import TypeVar, Iterable, Protocol

DType = TypeVar("DType", covariant=True)


# until we are able to use numpy 1.21 and `ndarray[shape, dtype]` everywhere, we
# can use a baseline of Iterable[DType] to indicate where a numpy array is
# expected as input. For output, using `np.ndarray` is nicer since it allows
# users to access all the methods
class ArrayLike(Protocol, Iterable[DType]):
    def __getitem__(self, key):
        # type: (int) -> DType
        ...
