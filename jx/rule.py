# coding: utf-8

import rule_engine
from jx.sqlalchemy_env import *
from jx.model_dict import KpiObjectBase

# define object module to get dynamic class name
try:
    module = __import__('jx.module', fromlist=(["module"]))
except ImportError:
    module = __import__('module')


# define the custom context to set the resolver
context = rule_engine.Context(resolver=rule_engine.resolve_attribute)


class KH_JXKHGZ(Base, KpiObjectBase):  # 绩效考核规则
    """
        Rule object mataches with rule.
        sqlalchemy: https://www.cnblogs.com/robertx/p/11122851.html

        # 考核数据对象: object to be applied in rule
        # 规则条件: rule engine in string for condition check
        # 绩效分数计算: rule engine in string for value calculation
        # 考核明细模版: 使用python语言字符串%格式化  # python '%()s' % {}
        # 考核结果对象: object storing the rule's value
    """

    __tablename__ = "kh_jxkhgz"  # 绩效考核规则

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID

    GZH = Column('GZH', String(128), unique=True, default='')  # 规则号
    DWH = Column('DWH', String(16), default='')  # 单位号
    KHLX = Column('KHLX', String(32), default='')  # 考核类型
    KHZL = Column('KHZL', String(32), default='')  # 考核子类
    XXKLZL = Column('XXKLZL', String(32), default='')  # 详细考核子类
    KHMC = Column('KHMC', String(256), default='')  # 考核名称
    KHSJDX = Column('KHSJDX', String(64), default='')  # 考核数据对象
    GZTJ = Column('GZTJ', String(2056), default='')  # 规则条件
    JXFSJS = Column('JXFSJS', String(2056), default='')  # 绩效分数计算
    KHMXMB = Column('KHMXMB', Text, default='')  # 考核明细模版
    KHJGDX = Column('KHJGDX', String(64), default='')  # 考核结果对象

    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(2056), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_jxkhgz AS
            SELECT 
                kh.id AS id,
                kh.GZH AS GZH,
                kh.DWH AS DWH,
                kh.KHLX AS KHLX,
                kh.KHZL AS KHZL,
                kh.XXKLZL AS XXKLZL,
                kh.KHMC AS KHMC,
                kh.KHSJDX AS KHSJDX,
                kh.GZTJ AS GZTJ,
                kh.JXFSJS AS JXFSJS,
                kh.KHMXMB AS KHMXMB,
                kh.KHJGDX AS KHJGDX,
                kh.stamp AS stamp,
                kh.note AS note            
            FROM kh_jxkhgz kh
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '规则号': ['GZH'],
            '单位号': ['DWH'],
            '考核类型': ['KHLX'],
            '考核子类': ['KHZL'],
            '详细考核子类': ['XXKLZL'],
            '考核名称': ['KHMC'],
            '考核数据对象': ['KHSJDX'],
            '规则条件': ['GZTJ'],
            '绩效分数计算': ['JXFSJS'],
            '考核明细模版': ['KHMXMB'],
            '考核结果对象': ['KHJGDX'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['GZH']

    # TODO: edit as view_sql
    @staticmethod
    def get_search_columns() -> List[str]:
        return ['GZH', 'DWH', 'DWMC', 'KHLX', 'KHZL', 'XXKLZL', 'KHMC', 'KHSJDX']

    # TODO: edit as view_sql
    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', },
            {'field': 'GZH', 'title': '规则号', 'editable': 'True', 'type': 'text', },
            {'field': 'DWH', 'title': '单位号', 'editable': 'True', 'type': 'text', },
            {'field': 'DWMC', 'title': '单位名称', 'editable': 'True', 'type': 'text', },
            {'field': 'KHLX', 'title': '考核类型', 'editable': 'True', 'type': 'text', },
            {'field': 'KHZL', 'title': '考核子类', 'editable': 'True', 'type': 'text', },
            {'field': 'XXKLZL', 'title': '详细考核子类', 'editable': 'True', 'type': 'text', },
            {'field': 'KHMC', 'title': '考核名称', 'editable': 'True', 'type': 'text', },
            {'field': 'KHSJDX', 'title': '考核数据对象', 'editable': 'True', 'type': 'text', },
            {'field': 'GZTJ', 'title': '规则条件', 'editable': 'True', 'type': 'text', },
            {'field': 'JXFSJS', 'title': '绩效分数计算', 'editable': 'True', 'type': 'text', },
            {'field': 'KHMXMB', 'title': '考核明细模版', 'editable': 'True', 'type': 'text', },
            {'field': 'KHJGDX', 'title': '考核结果对象', 'editable': 'True', 'type': 'text', },
            {'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', },
            {'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', },
        ]

    def __init__(self, GZH, DWH, KHLX, KHZL, XXKLZL, KHMC, KHSJDX, GZTJ, JXFSJS, KHMXMB, KHJGDX, stamp=now(), note=''):
        """
        :param GZTJ:  # str format rule engine for condition check
        :param JXFSJS:  # str format rule engine for value calculation
        :param
        """
        self.GZH = GZH
        self.DWH = DWH
        self.KHLX = KHLX
        self.KHZL = KHZL
        self.XXKLZL = XXKLZL
        self.KHMC = KHMC
        self.KHSJDX = KHSJDX
        self.GZTJ = GZTJ
        self.JXFSJS = JXFSJS
        self.KHMXMB = KHMXMB
        self.KHJGDX = KHJGDX
        self.stamp = stamp
        self.note = note

    def get_input_class(self):
        """
        :return: rule calculation class by string format input_object
        """
        return getattr(module, ('view_' + self.KHSJDX).upper())

    def get_output_class(self):
        """
        Return object storing the rule's value, which can be defined in module or other place.
        The return's object should have method to keep the calculation value to database.

        :return: class by string format output_object, which store the value calculated while condition is true
        """
        return 'KH_' + self.KHJGDX

    def get_output_template(self):
        return self.KHMXMB

    def match(self, obj):
        """
        :return: rule condition is true or false
        """
        condition = rule_engine.Rule(self.GZTJ, context=context)
        return condition.matches(obj) if len(self.GZTJ) else False

    def calculate(self, obj):
        """
        :return: value calculated while condition is true
        """
        value = rule_engine.Rule(self.JXFSJS, context=context)
        return value.evaluate(obj) if len(self.JXFSJS) else 0.0


# TODO: 手工增减业绩点???
class KH_KHJGMX(Base, KpiObjectBase):  # 考核结果明细

    __tablename__ = "kh_khjgmx"  # 考核结果明细

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID

    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    DWH = Column('DWH', String(16), default='')  # 单位号
    GZH = Column('GZH', String(128), default='')  # 规则号
    KHNF = Column('KHNF', DateTime, default=now())  # 考核年份
    KHJD = Column('KHJD', Float, default=0.0)  # 考核绩点
    KHMX = Column('KHMX', Text, default='')  # 考核明细

    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(2056), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_khjgmx AS
            SELECT 
                kh.id AS id,
                kh.JZGH AS JZGH,
                kh.DWH AS DWH,
                kh.GZH AS GZH,
                kh.KHNF AS KHNF,
                kh.KHJD AS KHJD,
                kh.KHMX AS KHMX,
                kh.stamp AS stamp,
                kh.note AS note           
            FROM kh_khjgmx kh
            WHERE 1=1
        """
        return sql_v1

    # TODO: edit as view_sql
    @staticmethod
    def get_search_columns() -> List[str]:
        return ['JZGH', 'DWH', 'GZH', 'KHNF', 'KHMX']

    # TODO: edit as view_sql
    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', },
            {'field': 'JZGH', 'title': '教职工号', 'editable': 'False', 'type': 'text', },
            {'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', },
            {'field': 'GZH', 'title': '规则号', 'editable': 'False', 'type': 'text', },
            {'field': 'KHNF', 'title': '考核年份', 'editable': 'False', 'type': 'date', },
            {'field': 'KHJD', 'title': '考核绩点', 'editable': 'False', 'type': 'text', },
            {'field': 'KHMX', 'title': '考核明细', 'editable': 'False', 'type': 'text', },
            {'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', },
            {'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', },
        ]

    def __init__(self, JZGH, DWH, GZH, KHJD, KHMX, KHNF=now(), stamp=now(), note=''):
        self.JZGH = JZGH
        self.DWH = DWH
        self.GZH = GZH
        self.KHNF = KHNF
        self.KHJD = KHJD
        self.KHMX = KHMX
        self.stamp = stamp
        self.note = note


"""
ALTER TABLE KH_JXKHGZ ADD stamp TIMESTAMP(6);
ALTER TABLE KH_KHJGMX ADD stamp TIMESTAMP(6);
"""


class KH_KHPC(Base, KpiObjectBase):  # 考核批次

    __tablename__ = "kh_khpc"  # 考核批次
    __table_args__ = (UniqueConstraint('DWH', 'KHNF', name='_kh_khpc_dwh_khnf_uc'),)

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    DWH = Column('DWH', String(16), default='')  # 单位号
    KHNF = Column('KHNF', DateTime, default=now())  # 考核年份
    RQQD = Column('RQQD', DateTime, default=now())  # 日期起点
    RQZD = Column('RQZD', DateTime, default=now())  # 日期终点
    JHZT = Column('JHZT', Enum('未激活', '已激活'), default='已激活')  # 激活状态
    FBZT = Column('FBZT', Enum('未发布', '已发布'), default='已发布')  # 发布状态
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(2056), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_khpc AS
            SELECT 
                kh.id AS id,
                kh.DWH AS DWH,
                dr.DWMC AS DWMC,
                kh.KHNF AS KHNF,
                kh.RQQD AS RQQD,
                kh.RQZD AS RQZD,
                kh.JHZT AS JHZT,
                kh.FBZT AS FBZT,
                kh.stamp AS stamp,
                kh.note AS note           
            FROM kh_khpc kh
            LEFT JOIN dr_zzjgjbsjxx dr ON dr.DWH=kh.DWH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '单位号': ['DWH'],
            '考核年份': ['KHNF', 'DateTime'],
            '日期起点': ['RQQD', 'DateTime'],
            '日期终点': ['RQZD', 'DateTime'],
            '激活状态': ['JHZT', 'Enum', ['未激活', '已激活']],
            '发布状态': ['FBZT', 'Enum', ['未发布', '已发布']],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['DWH', 'KHNF']

    # TODO: edit as view_sql
    @staticmethod
    def get_search_columns() -> List[str]:
        return ['DWMC', 'DWH', 'KHNF']

    # TODO: edit as view_sql
    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', },
            {'field': 'DWH', 'title': '单位号', 'editable': 'True', 'type': 'text', },
            {'field': 'DWMC', 'title': '单位名称', 'editable': 'False', 'type': 'text', },
            {'field': 'KHNF', 'title': '考核年份', 'editable': 'True', 'type': 'year', },  # TODO: type.year
            {'field': 'RQQD', 'title': '日期起点', 'editable': 'True', 'type': 'date', },
            {'field': 'RQZD', 'title': '日期终点', 'editable': 'True', 'type': 'date', },
            {'field': 'JHZT', 'title': '激活状态', 'editable': 'True', 'type': 'enum', 'value': ['未激活', '已激活'], },  # TODO: type.enum, value set/1st default
            {'field': 'FBZT', 'title': '发布状态', 'editable': 'True', 'type': 'enum', 'value': ['未发布', '已发布'], },
            {'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', },
            {'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', },
        ]

    def __init__(self, DWH, KHNF=now(), RQQD=now(), RQZD=now(), JHZT='已激活', FBZT='已发布', stamp=now(), note=''):
        self.DWH = DWH
        self.KHNF = KHNF
        self.RQQD = RQQD
        self.RQZD = RQZD
        self.JHZT = JHZT
        self.FBZT = FBZT
        self.stamp = stamp
        self.note = note


class KH_KHGZDZ(Base, KpiObjectBase):  # 考核规则定制

    __tablename__ = "kh_khgzdz"  # 考核规则定制
    __table_args__ = (UniqueConstraint('DWH', 'KHNF', 'GZH', name='_kh_khgzdz_dwh_khnf_gzh_uc'),)

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    DWH = Column('DWH', String(16), default='')  # 单位号
    KHNF = Column('KHNF', DateTime, default=now())  # 考核年份
    GZH = Column('GZH', String(128), default='')  # 规则号
    GZQY = Column('GZQY', Enum('未启用', '已启用'), default='已启用')  # 规则启用
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(2056), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_khgzdz AS
            SELECT 
                kh.id AS id,
                kh.DWH AS DWH,
                dr.DWMC AS DWMC,
                kh.KHNF AS KHNF,
                kh.GZH AS GZH,
                kh.GZQY AS GZQY,
                gz.KHMC AS KHMC,
                kh.stamp AS stamp,
                kh.note AS note           
            FROM kh_khgzdz kh
            LEFT JOIN dr_zzjgjbsjxx dr ON dr.DWH=kh.DWH
            LEFT JOIN kh_jxkhgz gz ON gz.GZH=kh.GZH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '单位号': ['DWH'],
            '考核年份': ['KHNF', 'DateTime'],
            '规则号': ['GZH'],
            '规则启用': ['GZQY', 'Enum', ['未启用', '已启用']],  # Note: 1st one is default value
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['DWH', 'KHNF', 'GZH']

    # TODO: edit as view_sql
    @staticmethod
    def get_search_columns() -> List[str]:
        return ['DWMC', 'DWH', 'KHNF', 'GZH', 'KHMC']

    # TODO: edit as view_sql
    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', },
            {'field': 'DWH', 'title': '单位号', 'editable': 'True', 'type': 'text', },
            {'field': 'DWMC', 'title': '单位名称', 'editable': 'False', 'type': 'text', },
            {'field': 'KHNF', 'title': '考核年份', 'editable': 'True', 'type': 'year', },
            {'field': 'GZH', 'title': '规则号', 'editable': 'True', 'type': 'text', },
            {'field': 'KHMC', 'title': '考核名称', 'editable': 'False', 'type': 'text', },
            {'field': 'GZQY', 'title': '规则启用', 'editable': 'True', 'type': 'enum', 'value': ['未启用', '已启用'], },
            {'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', },
            {'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', },
        ]

    def __init__(self, DWH, KHNF, GZH, GZQY='已启用', stamp=now(), note=''):
        self.DWH = DWH
        self.KHNF = KHNF
        self.GZH = GZH
        self.GZQY = GZQY
        self.stamp = stamp
        self.note = note


class KH_KHJGHZ(Base, KpiObjectBase):  # 考核结果汇总

    __tablename__ = "kh_khjghz"  # 考核结果汇总
    __table_args__ = (UniqueConstraint('DWH', 'KHNF', 'GZH', name='_kh_khjghz_dwh_khnf_gzh_uc'),)

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    DWH = Column('DWH', String(16), default='')  # 单位号
    LSDWH = Column('LSDWH', String(16), default='')  # 隶属单位号
    KHNF = Column('KHNF', DateTime, default=now())  # 考核年份
    GZH = Column('GZH', String(128), default='')  # 规则号
    KHJDHJ = Column('KHJDHJ', Float, default=0.0)  # 考核绩点合计
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(2056), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_khjghz AS
            SELECT 
                kh.id AS id,
                kh.DWH AS DWH,
                dr.DWMC AS DWMC,
                kh.LSDWH AS LSDWH,
                ls.DWMC AS LSDWMC,
                kh.KHNF AS KHNF,
                kh.GZH AS GZH,
                gz.KHMC AS KHMC,
                kh.KHJDHJ AS KHJDHJ,
                kh.stamp AS stamp,
                kh.note AS note           
            FROM kh_khjghz kh
            LEFT JOIN dr_zzjgjbsjxx dr ON dr.DWH=kh.DWH
            LEFT JOIN dr_zzjgjbsjxx ls ON ls.DWH=kh.LSDWH
            LEFT JOIN kh_jxkhgz gz ON gz.GZH=kh.GZH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '单位号': ['DWH'],
            '考核年份': ['KHNF', 'DateTime'],
            '规则号': ['GZH'],
            '考核绩点合计': ['KHJDHJ'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['DWH', 'KHNF', 'GZH']

    # TODO: edit as view_sql
    @staticmethod
    def get_search_columns() -> List[str]:
        return ['DWMC', 'DWH', 'LSDWMC', 'LSDWH', 'KHNF', 'GZH', 'KHMC']

    # TODO: edit as view_sql
    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', },
            {'field': 'DWH', 'title': '单位号', 'editable': 'True', 'type': 'text', },
            {'field': 'DWMC', 'title': '单位名称', 'editable': 'False', 'type': 'text', },
            {'field': 'LSDWH', 'title': '隶属单位号', 'editable': 'False', 'type': 'text', },
            {'field': 'LSDWMC', 'title': '隶属单位名称', 'editable': 'False', 'type': 'text', },
            {'field': 'KHNF', 'title': '考核年份', 'editable': 'True', 'type': 'year', },
            {'field': 'GZH', 'title': '规则号', 'editable': 'True', 'type': 'text', },
            {'field': 'KHMC', 'title': '考核名称', 'editable': 'False', 'type': 'text', },
            {'field': 'KHJDHJ', 'title': '考核绩点合计', 'editable': 'False', 'type': 'text', },
            {'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', },
            {'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', },
        ]

    def __init__(self, DWH, KHNF, GZH, KHJDHJ, stamp=now(), note=''):
        from jx.module import VIEW_ZZJGJBSJXX
        self.DWH = DWH
        self.LSDWH = VIEW_ZZJGJBSJXX.get_parent_department(DWH)
        self.KHNF = KHNF
        self.GZH = GZH
        self.KHJDHJ = KHJDHJ
        self.stamp = stamp
        self.note = note


if __name__ == '__main__':
    # from module import VIEW_ZZJGJBSJXX
    # print(VIEW_ZZJGJBSJXX.get_managed_departments('00000B'))
    # exit(0)

    Base.metadata.create_all(engine)  # CREATE ALL
    exit(0)

    # Example: SQLAlchemy add-commit-rollback
    # try:
    #     for x in range(17):
    #         code = ''
    #         for i in range(3):
    #             code += random.choice('abcdefghijklmnopqrstuvwxyz'.upper())
    #         for i in range(3):
    #             code += random.choice('0123456789')
    #         app = ApplyCode(code=code, uid=str(uuid.uuid4()))
    #         db.add(app)
    #     db.commit()
    # except:
    #     print('exception')
    #     db.rollback()

    # Example: dynamic class and instance by module-classname
    # a_class = getattr(module, 'ApplyCode')
    # a_instance = a_class(366, '123456', 0, '1234567890')  # OR: obj = new.instance(a_class)
    # print(a_instance.id)

    # Init a rule object. Rules objects can be defined and filtered out using SQLAlchemy ORM method
    # rule_obj = RuleObject(
    #     name='Test',
    #     department='Yejin',
    #     parent='DD',
    #     level='A',
    #     sub_level='A-A1',
    #     input_object='ApplyCode',
    #     condition='id == 33 or id == 32',
    #     value='id * 3',
    #     output_object='ApplyCode',
    #     note=''
    # ).save()

    # Save to database
    # db.add(rule_obj)
    # # db.add_all([User(name='用户2'), User(name='用户3'),])  # 2. 添加多条数据
    # db.commit()  # 结束记得提交, 数据才能保存在数据库中
    # db.close()  # 关闭会话

    # run_kpi()

    # print(get_class_attribute())  # TODO: provide as URL

    # TODO:
    """
        0. DONE: Upgrade python3/django
        1. DONE: Module/rule definition method 
        2. Rule's showing in FE
        3. Rule Editor in FE: a) simple string. b) GUI editor
        4. DONE: Rule calculation save method
        5. BE to summarize all level KPIs
    """

    exit(0)
