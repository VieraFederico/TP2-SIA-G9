from abc import ABC, abstractmethod

from PIL import Image

from genetics_algorithm.models.Individual import Individual


class FitnessFunction(ABC):
    @abstractmethod
    def evaluate(self, individual: Individual, target: Image.Image) -> float:
        ...
