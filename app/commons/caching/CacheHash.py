import inspect
from dataclasses import dataclass
from typing import Any, Callable

import joblib


@dataclass
class CacheHash:
    args: Any
    kwargs: Any
    function: Callable
    class_name: str = 'Function'

    @property
    def filename(self) -> str:
        args = list(self.args)
        function_name = self.function.__name__
        if self.args and inspect.isclass(args[0]):
            self.class_name = args.pop(0).__name__
        elif self.args and getattr(args[0], function_name, False):
            self.class_name = args.pop(0).__class__.__name__
        name = f'{self.class_name}.{function_name}'
        name += f'_{joblib.hash(args)}' if args else ''
        name += f'_{joblib.hash(tuple(self.kwargs.values()))}' if self.kwargs else ''
        return f'{name}.pkl'
