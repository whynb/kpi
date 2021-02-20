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


# TODO: create below modules
todo = """
考核批次
    单位号
    激活状态
    年份
    发布状态
    日期起点
    日期终点
    备注

规则定制
    单位号
    年份
    规则号
    规则启用 (1-是，0-否)        

考核结果汇总
    单位号
    隶属单位号
    考核年份
    规则号
    考核绩点合计
"""


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
            {'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', },
        ]

    def __init__(self, GZH, DWH, KHLX, KHZL, XXKLZL, KHMC, KHSJDX, GZTJ, JXFSJS, KHMXMB, KHJGDX, note=''):
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

    def save(self):
        """
        Save to database
        :return: self
        """
        db.add(self)
        db.commit()
        return self


class KH_KHJGMX(Base, KpiObjectBase):  # 考核结果明细

    __tablename__ = "kh_khjgmx"  # 考核结果明细

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID

    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    DWH = Column('DWH', String(16), default='')  # 单位号
    GZH = Column('GZH', String(128), default='')  # 规则号
    KHNF = Column('KHNF', DateTime, default=now())  # 考核年份
    KHJD = Column('KHJD', Float, default=0.0)  # 考核绩点
    KHMX = Column('KHMX', Text, default='')  # 考核明细

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
    def get_title_columns() -> List[str]:
        return [
            {'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', },
            {'field': 'JZGH', 'title': '教职工号', 'editable': 'False', 'type': 'text', },
            {'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', },
            {'field': 'GZH', 'title': '规则号', 'editable': 'False', 'type': 'text', },
            {'field': 'KHNF', 'title': '考核年份', 'editable': 'False', 'type': 'date', },
            {'field': 'KHJD', 'title': '考核绩点', 'editable': 'False', 'type': 'text', },
            {'field': 'KHMX', 'title': '考核明细', 'editable': 'False', 'type': 'text', },
            {'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', },
        ]

    def __init__(self, JZGH, DWH, GZH, KHJD, KHMX, KHNF=now(), note=''):
        self.JZGH = JZGH
        self.DWH = DWH
        self.GZH = GZH
        self.KHNF = KHNF
        self.KHJD = KHJD
        self.KHMX = KHMX
        self.note = note

    def save(self):
        db.add(self)
        db.commit()
        return self


if __name__ == '__main__':
    # from module import VIEW_ZZJGJBSJXX
    # print(VIEW_ZZJGJBSJXX.get_managed_departments('00000B'))

    exit(0)

    # Base.metadata.create_all(engine)  # CREATE ALL
    # exit(0)

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
