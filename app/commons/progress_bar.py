import time


class ProgressBar:
    GREEN_BOX = '\033[;32m█\033[0m'
    BLACK_BOX = '█'

    def __init__(self, total, prefix='', length=50):
        self._total = total
        self._prefix = prefix
        self._length = length
        self._counter = 0
        self._started_at = time.time()

    def update(self, step=1):
        self._counter += step
        percentage = self._counter / float(self._total)
        filled_length = self._length * self._counter // self._total
        completed = self.GREEN_BOX * filled_length
        uncompleted = self.BLACK_BOX * (self._length - filled_length)
        bar = f"\r{self._prefix:45} \u2615 |{completed}{uncompleted}| {percentage:.1%} - {self._time_delta}"
        print(bar, end='')
        if self._counter == self._total:
            print()

    @property
    def _time_delta(self):
        seconds = round(time.time() - self._started_at)
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)
