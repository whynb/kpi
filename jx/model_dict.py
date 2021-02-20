# coding=utf-8
# 定义导入数据模型，与东大校标一致

# TODO: use data dictionary to generate models by class templates


class KpiObjectBase:

    @staticmethod
    def sql() -> str:
        return 'SELECT 0'

    @staticmethod
    def get_column_label() -> dict:
        return {}

    @staticmethod
    def get_unique_condition() -> []:
        return ['id']

    @staticmethod
    def get_hide_columns() -> []:
        return ['id']

    @staticmethod
    def get_edit_columns() -> []:
        return ['note']

    @staticmethod
    def get_title_columns() -> []:
        return ['note']

    @staticmethod
    def get_search_columns() -> []:
        return ['note']
