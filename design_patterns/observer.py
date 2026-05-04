"""
Design Patterns: Observer
"""

from abc import ABC, abstractmethod
from typing import Callable


class Observer(ABC):
    @abstractmethod
    def update(self, subject: "Subject") -> None:
        pass


class Subject:
    def __init__(self):
        self._observers: list[Observer] = []
        self._state = 0

    @property
    def state(self) -> int:
        return self._state

    @state.setter
    def state(self, value: int) -> None:
        self._state = value
        self.notify()

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)


# Concrete observers
class PropertyObserver(Observer):
    def __init__(self, name: str):
        self.name = name
        self.last_value = None

    def update(self, subject: Subject) -> None:
        print(f"Observer {self.name}: State changed to {subject.state}")


class UpperThresholdObserver(Observer):
    def __init__(self, threshold: int):
        self.threshold = threshold

    def update(self, subject: Subject) -> None:
        if subject.state > self.threshold:
            print(f"Alert! State {subject.state} exceeds threshold {self.threshold}")


# Usage
subject = Subject()
obs1 = PropertyObserver("A")
obs2 = PropertyObserver("B")
alert = UpperThresholdObserver(10)

subject.attach(obs1)
subject.attach(obs2)
subject.attach(alert)

print("Setting state to 5:")
subject.state = 5

print("\nSetting state to 15:")
subject.state = 15

print("\nDetaching observer B, setting state to 7:")
subject.detach(obs2)
subject.state = 7