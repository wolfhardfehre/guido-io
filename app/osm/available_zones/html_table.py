import pandas as pd
from bs4 import Tag


class HtmlTable:
    _RENAME_ = dict(quick_links_link='download_link')

    def __init__(self, table_tag: Tag):
        self._table = table_tag

    @property
    def frame(self):
        frame = pd.DataFrame.from_records(self._records)
        return frame.rename(columns=self._RENAME_)

    @property
    def _records(self):
        columns = self._columns
        records = []
        for rows in self._rows:
            if self._header_cells(rows):
                continue
            record = {}
            for cell, column in self._cells_with_column(rows, columns):
                link = cell.find('a')
                if link:
                    record.update({f'{column}_link': link['href']})
                record.update({column: cell.text})
            records.append(record)
        return records

    def _cells_with_column(self, rows, columns):
        cells = self._record_cells(rows)
        return zip(cells, columns)

    @property
    def _columns(self):
        columns = []
        for rows in self._rows:
            for cell in self._header_cells(rows):
                columns.append(cell.text)
        return [column.replace(' ', '_').lower() for column in columns]

    @property
    def _rows(self):
        return self._table.findAll("tr")

    @staticmethod
    def _header_cells(rows):
        return rows.findAll("th")

    @staticmethod
    def _record_cells(rows):
        return rows.findAll("td")
