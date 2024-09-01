"""
Паттерн Наблюдатель

Данный паттерн позволяет создать гибкую архитектуру за счет того, что у нас имеется некий
наблюдатель (в данном случае класс Obserser) - который определяет, как должен выглядеть
потенциальный наблюдатель, а также есть родительский класс (Observable) - который содержит
в себе список наблюдателей а также дополнительные методы. Дабы подключиться к наблюдению - мы
должны унаследоваться от класса Observable и каждый раз, при изменении своего состояния вызывать
метод _notify_observers() - который уведомляет всех НАБЛЮДЕТЕЛЕЙ, который подписались на
этот наблюдаемый объект (тоесть присутствуют в списке наблюдателей (_observers) в классе Observable)
"""

import json
import time
from typing import Protocol


class Observer(Protocol):
    def __call__(self) -> None:
        ...


class Observable:
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
    
    def _notify_observers(self) -> None:
        for observer in self._observers:
            observer()


Hand = list[int]

class ZonkHandHistory(Observable):
    def __init__(self, player: str, diceSet: Dice) -> None:
        super().__init__()
        self.player = player
        self.diceSet = diceSet
        self.rolls: list[Hand]
    
    def start(self) -> Hand:
        self.diceSet.roll()
        self.rolls = [self.diceSet.dice]
        self._notify_observers()
        
        return self.diceSet.dice
    
    def roll(self) -> Hand:
        self.diceSet.roll()
        self.rolls.append(self.diceSet.dice)
        self._notify_observers()

        return self.diceSet.dice
    

class SaveZonkHand(Observer):
    def __init__(self, hand: ZonkHandHistory) -> None:
        self.hand = hand
        self.count = 0
    
    def __call__(self) -> None:
        self.count += 1
        message = {
            "player": self.hand.player,
            "sequence": self.count,
            "hands": json.dumps(self.hand.rolls),
            "time": time.time()
        }
        print(f"SaveZonkHand {message}")