#Base code by https://refactoring.guru
#Implementation by Giovanni Guzmán

from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from random import shuffle
from typing import List
import threading


class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass


class ConcreteSubject(Subject):
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """

    _state: int = 0
    
    """
    For the sake of simplicity, the Subject's state, essential to all
    subscribers, is stored in this variable.
    """

    _observers: List[Observer] = []
    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    def attach(self, observer: Observer) -> None:
        print(f"A new bidder has entered with ${observer._money}")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        print(f"Bidder {observer._name} left the bid :(")
        self._observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        for observer in self._observers:
            observer.update(self)

    def some_business_logic(self) -> None:
        """
        Usually, the subscription logic is only a fraction of what a Subject can
        really do. Subjects commonly hold some important business logic, that
        triggers a notification method whenever something important is about to
        happen (or after it).
        """
        rounds = 3
        print(f"There will be {rounds} rounds")
        for x in range(1, rounds+1):
            print(f"this is round {x}")
            print(f"Auctioneer: I notify to all of you that there's a new Highest bid, which is {self._state}")

            shuffle(self._observers)
            self.notify()

            for observer in self._observers:
                if observer._money < self._state:
                    self.detach(observer)
        
        if len(self._observers) > 1:
            print("There is no winner, the bid is now closed")
        else:
            print(f"Bidder {self._observers[0]._name} won the auction!")


        


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """
        pass


"""
Concrete Observers react to the updates issued by the Subject they had been
attached to.
"""


class ConcreteObserver(Observer):

    def __init__(self, name):
        self._name = name
        self._money: int = randrange(1, 16)

    def update(self, subject: Subject) -> None:
        print(f"Bidder {self._name} gets notified of the new highest bid")
        if subject._state < self._money:
            print(f"Bidder {self._name} raises its hand to raise the highest bid")
            subject._state = self._money
            
if __name__ == "__main__":
    # The client code.

    count = 5

    auctioneer = ConcreteSubject()

    for x in range(0, count):
        auctioneer.attach(ConcreteObserver(x))

    auctioneer.some_business_logic()

