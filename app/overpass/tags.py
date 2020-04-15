import requests
import pandas as pd


class Tags:

    @property
    def popular_tags(self):
        response = requests.get(url=self._url, params=self._payload).json()
        popular = pd.json_normalize(response, 'data')
        wiki_only = popular[popular['in_wiki'] == 1].reset_index()
        wiki_only.loc[:, 'node'] = wiki_only['count_nodes'] > 0
        wiki_only.loc[:, 'way'] = wiki_only['count_ways'] > 0
        wiki_only.loc[:, 'relation'] = wiki_only['count_relations'] > 0
        columns = ['key', 'value', 'node', 'way', 'relation']
        return wiki_only[columns]

    @property
    def _url(self):
        return 'https://taginfo.openstreetmap.org/api/4/tags/popular'

    @property
    def _payload(self):
        return {'qtype': 'tag', 'format': 'json_pretty'}


if __name__ == '__main__':
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    pd.options.display.width = 800
    tags = Tags()
    print(tags.popular_tags)
