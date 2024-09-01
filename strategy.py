"""
Паттерн Стратегия

Данный паттерн позволяет нам инкапсулировать информацию о том
или ином конкретном алгоритме, предоставляя общий интерфейс для управления.

В данном случае мы определили протокол SortStrategy - он требует создания от всех
реализующих данный протокол классов метода sort(). Далее мы просто реализуем данные
классы, реализуя также этот интерфейс, тем самым становлясь некими "стратегиями" сортировки.
И также у нас есть простой класс Sorter - интерфейс, позволяющий выбрать ту или иную
стратегию сортировки и вызвать один единственный метод - sort
"""

from typing import Protocol


class SortStrategy(Protocol):
    def sort(self, data: list[int]) -> list[int]:
        ...


class BubbleSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        n = len(data)
        for i in range(n):
            for j in range(0, n-i-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]

        return data


class QuickSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]

        return self.sort(left) + middle + self.sort(right)


class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data: list[int]) -> list[int]:
        return self._strategy.sort(data)


if __name__ == "__main__":
    data = [5, 2, 9, 1, 5, 6]

    # Используем пузырьковую сортировку
    sorter = Sorter(BubbleSort())
    print("Bubble Sort:", sorter.sort(data.copy()))

    # Переключаемся на быструю сортировку
    sorter.set_strategy(QuickSort())
    print("Quick Sort:", sorter.sort(data.copy()))
