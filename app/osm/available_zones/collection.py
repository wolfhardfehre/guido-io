from dataclasses import dataclass, field
from typing import List, Union
import pandas as pd


@dataclass
class Collection:
    frames: List[pd.DataFrame] = field(default_factory=list)
    countries_to_drop: List[str] = field(default_factory=list)
    continent: Union[pd.Series, None] = None

    @property
    def url_tree(self) -> pd.DataFrame:
        merged = pd.concat(self.frames, ignore_index=True)
        merged['continent'] = self._get(merged, 'continent')
        merged['country'] = self._get(merged, 'country')
        merged.loc[~merged['state_link'].isnull(), 'state'] = self._get(merged, 'state')
        return merged[['continent', 'country', 'state']]

    @staticmethod
    def _get(frame: pd.DataFrame, area: str):
        return frame[f'{area}_link'] \
            .str.replace('-latest.osm.pbf', '', regex=False) \
            .str.split('/') \
            .str[-1]
