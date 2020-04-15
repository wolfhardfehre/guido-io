import abc


class Layer(abc.ABC):

    @property
    @abc.abstractmethod
    def layer(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def empty(self):
        raise NotImplementedError
