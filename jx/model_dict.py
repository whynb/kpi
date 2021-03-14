# coding=utf-8
# 定义导入数据模型，与东大校标一致

from typing import List


class KpiObjectBase:

    @staticmethod
    def sql() -> str:
        return 'SELECT 0'

    @staticmethod
    def get_upload_tables() -> List[str]:
        return []

    @staticmethod
    def get_delete_tables() -> List[str]:
        return []

    @staticmethod
    def get_create_tables() -> List[str]:
        return []

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['id']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp']

    @staticmethod
    def get_edit_columns() -> List[str]:  # NOTE: useless due to function moved to get_title_columns
        return ['note']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', },
            {'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', },
            {'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', },
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['note']

    def save(self):
        """
        Save to database
        :return: self
        """
        from jx.sqlalchemy_env import db
        db.add(self)
        db.commit()
        return self
