def add(a: int, b: int) -> int:
  return a + b

def substract(a: int, b: int) -> int:
  return b - a

def multiply(a: int, b: int) -> int:
  return a * b

def divide(a: int, b: int) -> int:
  return b // a


def test_add() -> None:
  assert add(1,1) == 2

def  test_substract() -> None:
  assert substract(2, 5) == 3

def test_multiply() -> None:
  assert multiply(2,3) == 6

def test_divide() -> None:
  assert divide(25, 100) == 4

