# coding: utf-8
# 规则引擎使用，不需要移植到数据库；view模型改变后，需重新手工执行rule.py
# NOTE: view performance. possible to move view to table and sync between tables

from jx.sqlalchemy_env import Base, cursor, conn, db
from sqlalchemy import *
from jx.util import now, sys_info, logger
from typing import List

# Document and example
'''
class ExampleModule(Base):
    """
    The class in module matches with database data source and inherits from SQLAlchemy Base.
    __tablename__: database table or view
    __tablename__CH__: database table or view name to show in FE
    
    Below is an example:
    """

    __table_args__ = {'extend_existing': True}  # Just copy this line which is used while creating database view  
    __tablename__ = 'view_examplemodule'  # SHOULD be same as class name
    __tablename__CH__ = '视图模型中文名称'

    # Below columns is used by role engine. 4 columns "id|JZGH|stamp|note" SHOULD be included in each module.
    id = Column('id', Integer, primary_key=True)  # ID
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注
    
    # Other columns defined
    
    @staticmethod
    def sql() -> str:
        """
        SQL to create view __tablename__.
        不在上面定义的字段也可以加入VIEW中，这些字段仅会被前端页面使用，而不会被规则引擎使用。
        数据时间条件字段可以设置为stamp，例如：论文录用时间；教职工号应设置为JZGH。
        """
        sql_v1 = """
            CREATE VIEW view_tablename AS
            SELECT 
                dr.id AS id,            
                dr.JZGH AS JZGH,
                jz.DWH AS DWH,
                dw.DWMC AS DWMC,
                dr.BRRQ AS stamp,
                dr.note AS note
            FROM dr_xmjfxx dr
            LEFT JOIN dc_xmjfxx dc ON dc.XMBH=dr.XMBH
            LEFT JOIN dr_jzgjcsjxx jz ON jz.JZGH=dr.JZGH
            LEFT JOIN dr_zzjgjbsjxx dw ON dw.DWH=jz.DWH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        """
        定义视图数据会被更新到哪些数据表
        """
        return ['dr_xmjfxx', 'dr_zzjgjbsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        """
        定义删除数据时应从哪些表中进行删除；删除时会依赖于被删除表模型的唯一性条件 get_unique_condition()。
        """
        return ['dr_xmjfxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        """
        定义新增数据时哪些表需要进行新增；新增时会依赖于新增表模型的唯一性条件 get_unique_condition()。
        如果新增表数据的唯一性条件满足，即数据存在，则提示；不满足，则新增。
        """
        return ['dr_xmjfxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        """
        定义前端表格中哪些字段需要隐藏，元素应与 get_title_columns() 中的 field 一致。
        """
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        """
        定义前端渲染时所需的所有字段信息：
        table: 定义数据真实来源表，用于增删改
        field: 字段标识，用于标识 FE 表格列，应与 view 中一致
        title: 字段标题，用于表示 FE 表格列名
        editable: 该表格元素前端可编辑，True|true|T|t or False|false|F|f
        create: 新增数据时该字段是否显示， False|false|F|f or True|true|T|t
        type: 定义数据类型，用于前端渲染，text｜year|month|date｜enum｜static｜table|inline|class
        value: 当 type 为 enum｜static｜table|inline|class 时使用
            enum-> 'value': ['未启用', '已启用'],
            static｜table|inline-> 'value': 'dr_zzjgjbsjxx:DWH,DWMC', -> 表:字段列表 -> 字段可以使用 AS｜as 关键字
            class-> 仅绩效考核规则使用 
        where: 当 type 为 static｜table|inline 时使用, 全部数据时为 ''，目前可用一下条件（如有新条件需要定制开发）:
            'where': 'DWH IN %(departments)s'},
            'where': "DWH IN %(departments)s AND JZGH!='admin'",
        action: 定义页面元素的动作(目前实现 onclick), 创建时选择项的 click->onChange() 的级联操作，例如：选择单位->选择该单位的员工    
            'action': [{
                'type': 'onclick',
                'content': {'value': 'view_jzgjcsjxx:JZGH,XM', 'where': 'DWH IN :this', 'to': 'JZGH:JZGH,XM', },
            }],
            content说明:
                value: 定义数据从哪里来
                where: 定义获得数据时的附加条件, 为防止SQL注入, 变量使用':'开始，变量名会作为GET参数传递到BE;
                    目前支持变量: ':this' - 本选择框的选取值
                to: 将BE返回值设置到哪个选择框
                    
        下面为实际例子，其中：
            负责人员号（BE）/负责人姓名（FE）联动，单位号（BE）/单位名称（FE）联动
            成果获奖类别码/奖励等级码 与静态表关联，前端仅显示中文，模型和后端仅用标识字段
        """
        return [
            {'table': 'dr_hjcgjbsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'HJCGBH', 'title': '获奖成果编号', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'FZRYH', 'title': '负责人员号', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'FZRXM', 'title': '负责人姓名', 'editable': 'T', 'type': 'table', 'value': 'dr_jzgjcsjxx:JZGH AS FZRYH,XM AS FZRXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'T', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'F', 'type': 'text', 'create': 'false', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_hjcgjbsjxx', 'field': 'HJRQ', 'title': '获奖日期', 'editable': 'true', 'type': 'date', 'create': 'True', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'CGHJLBM', 'title': '成果获奖类别码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_ky_cghjlb:DM AS CGHJLBM,MC', 'where': ''},
            {'table': 'dr_hjcgjbsjxx', 'field': 'JLDJM', 'title': '奖励等级码', 'editable': 'true', 'type': 'inline', 'create': 'T', 'value': 'st_jldj:JLDJM,JLDJMC', 'where': ''},
            {'table': 'dr_hjcgjbsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
            
            # NOTE: fields cascade example for type->table
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {
                'table': 'dr_zzjgjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'False',
                'type': 'table', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s', 'create': 'T',
                'action': [{
                    'type': 'onclick',
                    'content': {'value': 'view_jzgjcsjxx:JZGH,XM', 'where': 'DWH IN :this', 'to': 'JZGH:JZGH,XM', },
                }],
            },
            {'table': 'dr_xmjfxx', 'field': 'JZGH', 'title': '教职工号', 'editable': 'F', 'type': 'inline', 'create': 'T', },
        ]

    @staticmethod
    def get_search_columns() -> List:
        """
        定义前端表格中搜索功能的搜索字段范围，元素应与 get_title_columns() 中的 field 一致。
        """
        return ['JZGH', 'DWH', 'DWMC', 'XMBH', 'JBRXM']

'''


class VIEW_ZZJGJBSJXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_zzjgjbsjxx'
    __tablename__CH__ = '组织机构基本数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    DWH = Column('DWH', String(128), unique=True, default='')  # 单位号
    DWMC = Column('DWMC', String(128), default='')  # 单位名称
    DWYWMC = Column('DWYWMC', String(128), default='')  # 单位英文名称
    DWJC = Column('DWJC', String(128), default='')  # 单位简称
    DWYWJC = Column('DWYWJC', String(128), default='')  # 单位英文简称
    DWJP = Column('DWJP', String(128), default='')  # 单位简拼
    DWDZ = Column('DWDZ', String(128), default='')  # 单位地址
    SZXQ = Column('SZXQ', String(128), default='')  # 所在校区
    LSDWH = Column('LSDWH', String(128), default='')  # 隶属单位号
    DWLBM = Column('DWLBM', String(128), default='')  # 单位类别码
    DWBBM = Column('DWBBM', String(128), default='')  # 单位办别码
    DWYXBS = Column('DWYXBS', String(128), default='')  # 单位有效标识
    SXRQ = Column('SXRQ', DateTime, default=now)  # 失效日期
    SFST = Column('SFST', String(128), default='')  # 是否实体
    JLNY = Column('JLNY', DateTime, default=now())  # 建立年月
    DWFZRH = Column('DWFZRH', String(128), default='')  # 单位负责人号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_zzjgjbsjxx AS
            SELECT 
                dr.id AS id,
                dr.DWH AS DWH,
                dr.DWMC AS DWMC,
                dr.DWYWMC AS DWYWMC,            
                dr.DWJC AS DWJC,            
                dr.DWYWJC AS DWYWJC,            
                dr.DWJP AS DWJP,            
                dr.DWDZ AS DWDZ,            
                dr.SZXQ AS SZXQ,
                dr.LSDWH AS LSDWH,
                dr.DWLBM AS DWLBM,
                dr.DWBBM AS DWBBM,
                dr.DWYXBS AS DWYXBS,
                dr.SXRQ AS SXRQ,
                dr.SFST AS SFST,
                dr.JLNY AS JLNY,
                dr.DWFZRH AS DWFZRH,
                dr.stamp AS stamp,
                dr.note AS note            
            FROM dr_zzjgjbsjxx dr
            LEFT JOIN dc_zzjgjbsjxx dc ON dc.DWH=dr.DWH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_zzjgjbsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_zzjgjbsjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_zzjgjbsjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note', 'DWBBM', 'SFST', 'SZXQ', 'DWFZRH']

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['DWMC']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_zzjgjbsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'True', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWYWMC', 'title': '单位英文名称', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWJC', 'title': '单位简称', 'editable': 'True', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWYWJC', 'title': '单位英文简称', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWJP', 'title': '单位简拼', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWDZ', 'title': '单位地址', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'SZXQ', 'title': '所在校区', 'editable': 'T', 'type': 'text', 'create': 'T', },

            # TODO: 'type': 'inline', 'exclude' by WHERE: DWH!=%(department)s AND 显示上级单位但是不可更改/在submit时二次判断
            {'table': 'dr_zzjgjbsjxx', 'field': 'LSDWH', 'title': '隶属单位', 'editable': 'T', 'type': 'text', 'create': 'T', 'value': 'dr_zzjgjbsjxx:DWH AS LSDWH,DWMC AS LSDWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWLBM', 'title': '单位类别码', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWBBM', 'title': '单位办别码', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWYXBS', 'title': '单位有效标识', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'SXRQ', 'title': '失效日期', 'editable': 'T', 'type': 'date', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'SFST', 'title': '是否实体', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'JLNY', 'title': '建立年月', 'editable': 'T', 'type': 'month', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWFZRH', 'title': '单位负责人号', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'F', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'F', },
        ]

    @staticmethod
    def get_managed_departments(_department_id) -> list:
        if not _department_id or str(_department_id) in ('', 'None'):
            return []

        from sqlalchemy.exc import PendingRollbackError
        from jx.sqlalchemy_env import db

        departments = [_department_id]
        try:
            dpmts_query = db.query(VIEW_ZZJGJBSJXX)
            dpmts_query = dpmts_query.filter(VIEW_ZZJGJBSJXX.LSDWH == str(_department_id))
            dpmts = dpmts_query.all()

            for dpmt in dpmts:
                if dpmt:
                    departments.extend(VIEW_ZZJGJBSJXX.get_managed_departments(str(dpmt.DWH)))

        except PendingRollbackError:
            db.rollback()
            logger.error(sys_info())

        except:
            logger.error(sys_info())

        return list(set(departments))

    @staticmethod
    def get_parent_department(_department_id) -> str:
        if not _department_id or str(_department_id) in ('', 'None'):
            return ''

        from sqlalchemy.exc import PendingRollbackError
        from jx.sqlalchemy_env import db

        try:
            dpmts_query = db.query(VIEW_ZZJGJBSJXX)
            dpmts_query = dpmts_query.filter(VIEW_ZZJGJBSJXX.DWH == str(_department_id))
            dpmts = dpmts_query.all()

            for dpmt in dpmts:
                return str(dpmt.LSDWH)

        except PendingRollbackError:
            db.rollback()
            logger.error(sys_info())

        except:
            logger.error(sys_info())

        return ''


class VIEW_BKSJXZXS(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_bksjxzxs'
    __tablename__CH__ = '本科生教学总学时'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JZGH = Column('JZGH', String(16), unique=True, default='')  # 教职工号
    KCH = Column('KCH', String(16), unique=True, default='')  # 课程号
    JHXSS = Column('JHXSS', String(16), default='')  # 计划学时数
    KCJBM = Column('KCJBM', String(16), default='')  # 课程级别码
    JXMSJBM = Column('JXMSJBM', String(16), default='')  # 教学名师级别码
    WYKCTJM = Column('WYKCTJM', String(16), default='')  # 外语课程调节码
    ZLXS = Column('ZLXS', String(16), default='')  # 质量系数
    XQDM = Column('XQDM', String(16), default='')  # 学期
    XNDM = Column('XNDM', DateTime, default='')  # 学年
    HBS = Column('HBS', String(16), default='')  # 合班数
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_bksjxzxs AS
            SELECT 
                pk.id AS id,            
                pk.JSGH AS JZGH,            
                pk.KKXND AS XNDM,            
                pk.KKXQM AS XQDM,            
                kc.LLXS AS JHXSS,            
                pk.ZLXS AS ZLXS,            
                pk.HBS AS HBS,            
                pk.WYKCTJM AS WYKCTJM,            
                pk.JXMSJBM AS JXMSJBM,     
                kc.KCH AS KCH,         
                jp.KCJBM AS KCJBM,             
                pk.stamp AS stamp,            
                pk.note AS note            
            FROM dr_pksjxx pk
            LEFT JOIN dr_kcsjxx kc ON kc.KCH=pk.KCH
            LEFT JOIN dr_xnxqxx xn ON xn.XNDM=pk.KKXND
            LEFT JOIN dr_bks_jpkc jp ON jp.KCH=pk.KCH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_pksjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_pksjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_pksjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_pksjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_pksjxx', 'field': 'JZGH', 'title': '教职工号', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_pksjxx', 'field': 'KCH', 'title': '课程号', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_pksjxx', 'field': 'JHXSS', 'title': '计划学时数', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_pksjxx', 'field': 'KCJBM', 'title': '课程级别码', 'editable': 'True', 'type': 'text', },
            {'table': 'dr_pksjxx', 'field': 'JXMSJBM', 'title': '教学名师级别码', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'WYKCTJM', 'title': '外语课程调节码', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'ZLXS', 'title': '质量系数', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'XQDM', 'title': '学期', 'editable': 'False', 'type': 'date', },
            {'table': 'dr_jzgjcsjxx', 'field': 'XNDM', 'title': '学年', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'HBS', 'title': '合班数', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', },
            {'table': 'dr_jzgjcsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', },
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['JZGH']


class VIEW_JZGJCSJXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_jzgjcsjxx'
    __tablename__CH__ = '教职工基础数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JZGH = Column('JZGH', String(16), unique=True, default='')  # 教职工号
    DWH = Column('DWH', String(16), default='')  # 单位号
    DWMC = Column('DWMC', String(128), default='')  # 单位名称
    XM = Column('XM', String(16), default='')  # 姓名
    YWXM = Column('YWXM', String(16), default='')  # 英文姓名
    XMPY = Column('XMPY', String(16), default='')  # 姓名拼音
    CYM = Column('CYM', String(16), default='')  # 曾用名
    XBM = Column('XBM', String(16), default='')  # 性别码
    CSRQ = Column('CSRQ', DateTime, default=now())  # 出生日期
    CSDM = Column('CSDM', String(16), default='')  # 出生地码
    BZLBM = Column('BZLBM', String(16), default='')  # 编制类别码
    JZGLBM = Column('JZGLBM', String(16), default='')  # 教职工类别码
    DQZTM = Column('DQZTM', String(16), default='')  # 当前状态码
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_jzgjcsjxx AS
            SELECT 
                dr.id AS id,            
                dr.JZGH AS JZGH,            
                dr.DWH AS DWH,            
                zzjg.DWMC AS DWMC,            
                dr.XM AS XM,            
                dr.YWXM AS YWXM,            
                dr.XMPY AS XMPY,            
                dr.CYM AS CYM,            
                dr.XBM AS XBM,            
                dr.CSRQ AS CSRQ,            
                dr.CSDM AS CSDM,            
                dr.BZLBM AS BZLBM,            
                dr.JZGLBM AS JZGLBM,            
                dr.DQZTM AS DQZTM,            
                dr.stamp AS stamp,            
                dr.note AS note            
            FROM dr_jzgjcsjxx dr
            LEFT JOIN dc_jzgjcsjxx dc ON dc.JZGH=dr.JZGH
            LEFT JOIN dr_zzjgjbsjxx zzjg ON zzjg.DWH=dr.DWH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_jzgjcsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_jzgjcsjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_jzgjcsjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'DWH', 'stamp', 'note', 'CSDM', 'BZLBM', 'JZGLBM', 'DQZTM']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_jzgjcsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_jzgjcsjxx', 'field': 'JZGH', 'title': '教职工号', 'editable': 'False', 'type': 'text', 'create': 'T', },
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'T', 'type': 'table', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s', 'create': 'True', },
            {'table': 'dr_jzgjcsjxx', 'field': 'XM', 'title': '姓名', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_jzgjcsjxx', 'field': 'YWXM', 'title': '英文姓名', 'editable': 'True', 'type': 'text', 'create': 'T', },
            {'table': 'dr_jzgjcsjxx', 'field': 'XMPY', 'title': '姓名拼音', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_jzgjcsjxx', 'field': 'CYM', 'title': '曾用名', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_jzgjcsjxx', 'field': 'XBM', 'title': '性别码', 'editable': 'T', 'type': 'enum', 'value': ['男', '女'], 'create': 'T', },
            {'table': 'dr_jzgjcsjxx', 'field': 'CSRQ', 'title': '出生日期', 'editable': 'T', 'type': 'date', 'create': 'T', },
            {'table': 'dr_jzgjcsjxx', 'field': 'CSDM', 'title': '出生地码', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_jzgjcsjxx', 'field': 'BZLBM', 'title': '编制类别码', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_jzgjcsjxx', 'field': 'JZGLBM', 'title': '教职工类别码', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_jzgjcsjxx', 'field': 'DQZTM', 'title': '当前状态码', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_jzgjcsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'F', },
            {'table': 'dr_jzgjcsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'F', },
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['XM', 'DWMC', ]

    @staticmethod
    def get_managed_departments(_payroll) -> List[str]:
        if not _payroll or str(_payroll) in ('', 'None'):
            return []

        try:
            users_query = db.query(VIEW_JZGJCSJXX)
            users_query = users_query.filter(VIEW_JZGJCSJXX.JZGH == str(_payroll))
            users = users_query.all()
            return VIEW_ZZJGJBSJXX.get_managed_departments(users[0].DWH) if users else []
        except:
            return []


class VIEW_XMJFXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_xmjfxx'
    __tablename__CH__ = '项目经费信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JHJFZE = Column('JHJFZE', Float, default=0.0)  # 计划经费总额
    XMJFLYM = Column('XMJFLYM', String(16), default='')  # 项目经费来源码
    BRRQ = Column('BRRQ', DateTime, default=now())  # 拨入日期
    BKS = Column('BKS', Float, default=0.0)  # 拨款数
    ZCRQ = Column('ZCRQ', DateTime, default=now())  # 支出日期
    BFXZDWJF = Column('BFXZDWJF', Float, default=0.0)  # 拨付协作单位经费
    XMPZBH = Column('XMPZBH', String(64), default='')  # 项目凭证编号
    JBRXM = Column('JBRXM', String(32), default=now())  # 经办人姓名
    XMBH = Column('XMBH', String(64), unique=True, default='')  # 项目编号
    ZZKS = Column('ZZKS', Float, default=0.0)  # 支出款数
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    DWH = Column('DWH', String(16), default='')  # 单位号
    DWMC = Column('DWMC', String(128), default='')  # 单位名称
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_xmjfxx AS
            SELECT 
                dr.id AS id,            
                dr.JHJFZE AS JHJFZE,            
                dr.XMJFLYM AS XMJFLYM,            
                dr.BRRQ AS BRRQ,            
                dr.BKS AS BKS,            
                dr.ZCRQ AS ZCRQ,            
                dr.BFXZDWJF AS BFXZDWJF,            
                dr.XMPZBH AS XMPZBH,            
                dr.JBRXM AS JBRXM,            
                dr.XMBH AS XMBH,            
                dr.ZZKS AS ZZKS,            
                dr.JZGH AS JZGH,
                jz.DWH AS DWH,
                dw.DWMC AS DWMC,
                dr.BRRQ AS stamp,
                dr.note AS note
            FROM dr_xmjfxx dr
            LEFT JOIN dc_xmjfxx dc ON dc.XMBH=dr.XMBH
            LEFT JOIN dr_jzgjcsjxx jz ON jz.JZGH=dr.JZGH
            LEFT JOIN dr_zzjgjbsjxx dw ON dw.DWH=jz.DWH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_xmjfxx', 'dr_zzjgjbsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_xmjfxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_xmjfxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_xmjfxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },

            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {
                'table': 'dr_zzjgjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'False',
                'type': 'table', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s', 'create': 'True',
                'action': [{
                    'type': 'onclick',
                    'content': {'value': 'view_jzgjcsjxx:JZGH,XM', 'where': 'DWH IN :this', 'to': 'JZGH:JZGH,XM', },
                }],
            },
            {'table': 'dr_xmjfxx', 'field': 'JZGH', 'title': '教职工号', 'editable': 'False', 'type': 'inline', 'create': 'True', },

            {'table': 'dr_xmjfxx', 'field': 'JHJFZE', 'title': '计划经费总额', 'editable': 'True', 'type': 'float', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'XMJFLYM', 'title': '项目经费来源码', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'BRRQ', 'title': '拨入日期', 'editable': 'False', 'type': 'date', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'BKS', 'title': '拨款数', 'editable': 'True', 'type': 'float', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'ZCRQ', 'title': '支出日期', 'editable': 'True', 'type': 'date', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'BFXZDWJF', 'title': '拨付协作单位经费', 'editable': 'True', 'type': 'float', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'XMPZBH', 'title': '项目凭证编号', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'JBRXM', 'title': '经办人姓名', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'XMBH', 'title': '项目编号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'ZZKS', 'title': '支出款数', 'editable': 'True', 'type': 'float', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_xmjfxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List:
        return ['JZGH', 'DWH', 'DWMC', 'XMBH', 'JBRXM']

#zouyang
class VIEW_KJCGRYXX_LW(Base):  # 科技成果(论文)人员信息
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_kjcgryxx_lw'  # 科技成果(论文)人员信息
    __tablename__CH__ = '科技成果(论文)人员信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    DWH = Column('DWH', String(16), default='')  # 单位号
    SLLX = Column('SLLX', String(16), default='')  # 收录类型
    SLBH = Column('SLBH', String(16), default='')  # 收录编号
    SLSJ = Column('SLSJ', String(16), default='')  # 收录时间
    SLQH = Column('SLQH', String(16), default='')  # 收录区号
    RYH = Column('RYH', String(16),default='')  # 人员号
    JSM = Column('JSM', String(16), default='')  # 角色码
    ZXZS = Column('ZXZS', String(16), default='')  # 撰写字数
    PMZRS = Column('PMZRS', String(16), default='')  # 排名/总人数
    GXL = Column('GXL', String(16), default='')  # 贡献率
    XM = Column('XM', String(16), default='')  # 姓名
    SZDW = Column('SZDW', String(16), default='')  # 所在单位
    RYLX = Column('RYLX', String(16), default='')  # 人员类型
    LWBH = Column('LWBH', String(16), default='')  # 论文编号
    KJCGRYBH = Column('KJCGRYBH', String(16), default='')  # 科技成果人员编号
    LWMC = Column('LWMC', String(128), default='')  # 论文名称
    LWLXM = Column('LWLXM', String(16), default='')  # 论文类型码
    DYZZ = Column('DYZZ', String(16), default='')  # 第一作者
    CYRY = Column('CYRY', String(128), default='')  # 参与人员
    TXZZ = Column('TXZZ', String(16), default='')  # 通讯作者
    JSQK = Column('JSQK', String(128), default='')  # 检索情况
    JQY = Column('JQY', String(128), default='')  # 卷期页
    WDWZZPX = Column('WDWZZPX', String(16), default='')  # 外单位作者排序
    BZXYBJZDSYS = Column('BZXYBJZDSYS', String(16), default='')  # 标注学院部级重点实验室
    FBRQ = Column('FBRQ', DateTime, default=now())  # 发表日期
    JH = Column('JH', String(16), default='')  # 卷号
    QH = Column('QH', String(16), default='')  # 期号
    LRSJ = Column('LRSJ', DateTime, default=now())  # 录入时间
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注
    JZGH = Column('JZGH', String(16),default='')  # 教职工号


    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_kjcgryxx_lw AS
            SELECT 
                dr.id AS id,
                jz.DWH AS DWH,
                sl.SLLX AS SLLX,
                sl.SLBH AS SLBH,
                sl.SLSJ AS SLSJ,
                sl.SLQH AS SLQH,
                dr.RYH AS RYH,
                dr.RYH AS JZGH,
                dr.JSM AS JSM,
                dr.ZXZS AS ZXZS,
                dr.PMZRS AS PMZRS,
                dr.GXL AS GXL,
                dr.XM AS XM,
                dr.SZDW AS SZDW,
                dr.RYLX AS RYLX,
                dr.LWBH AS LWBH,
                dr.KJCGRYBH AS KJCGRYBH,                         
                qk.LWMC AS LWMC,            
                qk.LWLXM AS LWLXM,            
                qk.DYZZ AS DYZZ,            
                qk.CYRY AS CYRY,            
                qk.TXZZ AS TXZZ,            
                qk.JSQK AS JSQK,            
                qk.JQY AS JQY,            
                qk.WDWZZPX AS WDWZZPX,            
                qk.BZXYBJZDSYS AS BZXYBJZDSYS,            
                kj.FBRQ AS FBRQ,      
                kj.JH AS JH,
                kj.QH AS QH,
                kj.LRSJ AS LRSJ,
                kj.FBRQ AS stamp,            
                dr.note AS note     
            FROM dr_kjcgryxx_lw dr
            LEFT JOIN dc_kjcgryxx_lw dc ON dc.LWBH=dr.LWBH
            LEFT JOIN dr_kjlwslqk sl ON sl.LWBH=dr.LWBH
            LEFT JOIN dr_kjqklwjbsjxx qk ON qk.LWBH=dr.LWBH
            LEFT JOIN dr_kjlwfbxx kj ON kj.LWBH=dr.LWBH
            LEFT JOIN dr_jzgjcsjxx jz ON jz.JZGH=dr.RYH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_hide_columns() -> []:
        return ['id', 'LRSJ']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_kjcgryxx_lw','dr_kjlwslqk','dr_kjqklwjbsjxx','dr_kjlwfbxx',]

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_kjcgryxx_lw','dr_kjlwslqk','dr_kjqklwjbsjxx','dr_kjlwfbxx',]

    @staticmethod
    def get_title_columns() -> []:
        return [
            {'table': 'dr_kjcgryxx_lw','field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False',},
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_kjlwslqk', 'field': 'SLLX', 'title': '收录类型', 'editable': 'True', 'type': 'inline', 'value': 'st_ky_lzsl:DM AS SLLX,MC', 'where': '', 'create': 'True', },
            {'table': 'dr_kjlwslqk', 'field': 'SLBH', 'title': '收录编号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjlwslqk', 'field': 'SLSJ', 'title': '收录时间', 'editable': 'False', 'type': 'date', 'create': 'True', },
            {'table': 'dr_kjlwslqk', 'field': 'SLQH', 'title': '收录区号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_lw','field': 'RYH', 'title': '人员号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_lw', 'field': 'JSM', 'title': '角色码', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_lw', 'field': 'ZXZS', 'title': '撰写字数', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_lw', 'field': 'PMZRS', 'title': '排名/总人数', 'editable': 'False', 'type': 'text','create': 'True', },
            {'table': 'dr_kjcgryxx_lw', 'field': 'GXL', 'title': '贡献率', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_lw', 'field': 'XM', 'title': '姓名', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_lw', 'field': 'SZDW', 'title': '所在单位', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_lw', 'field': 'RYLX', 'title': '人员类型', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_lw', 'field': 'LWBH', 'title': '论文编号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_lw', 'field': 'KJCGRYBH', 'title': '科技成果人员编号', 'editable': 'False', 'type': 'text','create': 'True', },
            {'table': 'dr_kjqklwjbsjxx','field': 'LWMC', 'title': '论文名称', 'editable': 'False', 'type': 'text', 'create': 'True',},
            {'table': 'dr_kjqklwjbsjxx','field': 'LWLXM', 'title': '论文类型码', 'editable': 'True', 'type': 'text', 'create': 'True',},
            {'table': 'dr_kjqklwjbsjxx','field': 'DYZZ', 'title': '第一作者', 'editable': 'False', 'type': 'text', 'create': 'True',},
            {'table': 'dr_kjqklwjbsjxx','field': 'CYRY', 'title': '参与人员', 'editable': 'False', 'type': 'text', 'create': 'True',},
            {'table': 'dr_kjqklwjbsjxx','field': 'TXZZ', 'title': '通讯作者', 'editable': 'False', 'type': 'text', 'create': 'True',},
            {'table': 'dr_kjqklwjbsjxx','field': 'JSQK', 'title': '检索情况', 'editable': 'False', 'type': 'text', 'create': 'True',},
            {'table': 'dr_kjqklwjbsjxx','field': 'JQY', 'title': '卷期页', 'editable': 'False', 'type': 'text', 'create': 'True',},
            {'table': 'dr_kjqklwjbsjxx','field': 'WDWZZPX', 'title': '外单位作者排序', 'editable': 'True', 'type': 'enum', 'value': ['0','1','2', '3','4'],'create': 'True', },
            {'table': 'dr_kjqklwjbsjxx','field': 'BZXYBJZDSYS', 'title': '标注学院部级重点实验室', 'editable': 'True', 'type': 'enum','value': ['无','未收录','收录'],'create': 'True', },
            {'table': 'dr_kjlwfbxx', 'field': 'FBRQ', 'title': '发表日期', 'editable': 'True', 'type': 'date', 'create': 'True', },
            {'table': 'dr_kjlwfbxx','field': 'JH', 'title': '卷号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjlwfbxx','field': 'QH', 'title': '期号', 'editable': 'False', 'type': 'text', 'create': 'True',},
            {'table': 'dr_kjlwfbxx','field': 'LRSJ', 'title': '录入时间', 'editable': 'True', 'type': 'date', 'create': 'True',},
        ]

    @staticmethod
    def get_search_columns() -> []:
        return ['LWBH']


class VIEW_HJCGJBSJXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_hjcgjbsjxx'
    __tablename__CH__ = '获奖成果基本数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    HJCGBH = Column('HJCGBH', String(16), default='')  # 获奖成果编号
    HJCGMC = Column('HJCGMC', String(16), default='')  # 获奖成果名称
    XMLYM = Column('XMLYM', String(16), default='')  # 项目来源码
    DWH = Column('DWH', String(16), default='')  # 单位号
    HJRQ = Column('HJRQ', DateTime, default=now())  # 获奖日期
    CGHJLBM = Column('CGHJLBM', String(16), default='')  # 成果获奖类别码
    KJJLB = Column('KJJLB', String(16), default='')  # 科技奖类别
    JLDJM = Column('JLDJM', String(16), default='')  # 奖励等级码
    HJJBM = Column('HJJBM', String(16), default='')  # 获奖级别码
    XKLYM = Column('XKLYM', String(16), default='')  # 学科领域
    BJDW = Column('BJDW', String(16), default='')  # 颁奖单位
    SSXMBH = Column('SSXMBH', String(16), default='')  # 所属项目编号
    DWPM = Column('DWPM', String(16), default='')  # 单位排名
    XKMLKJM = Column('XKMLKJM', String(16), default='')  # 学科门类(科技)码
    FZRYH = Column('FZRYH', String(16), default='')  # 负责人员号
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    FZRXM = Column('FZRXM', String(16), default='')  # 负责人姓名
    YJXK = Column('YJXK', String(16), default='')  # 一级学科
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    YJSMC = Column('YJSMC', String(16), default='')  # 研究所名称
    CGXS = Column('CGXS', String(16), default='')  # 成果形式
    HJMC = Column('HJMC', String(16), default='')  # 获奖名称
    HJBH = Column('HJBH', String(16), default='')  # 获奖编号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_hjcgjbsjxx AS
            SELECT
               dr_hjcg.id AS id,
               dr_hjcg.HJCGBH AS HJCGBH,
               dr_hjcg.HJCGMC AS HJCGMC,
               dr_hjcg.XMLYM AS XMLYM,
               dr_hjcg.DWH AS DWH,
               dr_hjcg.HJRQ AS HJRQ,
               dr_hjcg.CGHJLBM AS CGHJLBM,
               dr_hjcg.KJJLB AS KJJLB,
               dr_hjcg.JLDJM AS JLDJM,
               dr_hjcg.HJJBM AS HJJBM,
               dr_hjcg.XKLYM AS XKLYM,
               dr_hjcg.BJDW AS BJDW,
               dr_hjcg.SSXMBH AS SSXMBH,
               dr_hjcg.DWPM AS DWPM,
               dr_hjcg.XKMLKJM AS XKMLKJM,
               dr_hjcg.FZRYH AS FZRYH,
               dr_hjcg.FZRYH AS JZGH,
               dr_hjcg.FZRXM AS FZRXM,
               dr_hjcg.YJXK AS YJXK,
               dr_hjcg.DWMC AS DWMC,
               dr_hjcg.YJSMC AS YJSMC,
               dr_hjcg.CGXS AS CGXS,
               dr_hjcg.HJMC AS HJMC,
               dr_hjcg.HJBH AS HJBH,
               dr_hjcg.HJRQ AS stamp,
               dr_hjcg.note AS note
            FROM dr_hjcgjbsjxx dr_hjcg
            LEFT JOIN dc_hjcgjbsjxx dc_hjcg ON dr_hjcg.HJCGBH = dr_hjcg.HJCGBH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_hjcgjbsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_hjcgjbsjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_hjcgjbsjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note', 'RYH']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_hjcgjbsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'HJCGBH', 'title': '获奖成果编号', 'editable': 'false', 'type': 'text', 'create': 'True', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'HJCGMC', 'title': '获奖成果名称', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'FZRYH', 'title': '负责人员号', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'FZRXM', 'title': '负责人姓名', 'editable': 'T', 'type': 'table', 'value': 'dr_jzgjcsjxx:JZGH AS FZRYH,XM AS FZRXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'T', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'F', 'type': 'text', 'create': 'false', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_hjcgjbsjxx', 'field': 'YJSMC', 'title': '研究所名称', 'editable': 'T', 'type': 'text', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'HJRQ', 'title': '获奖日期', 'editable': 'true', 'type': 'date', 'create': 'True', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'CGHJLBM', 'title': '成果获奖类别码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_ky_cghjlb:DM AS CGHJLBM,MC', 'where': ''},
            {'table': 'dr_hjcgjbsjxx', 'field': 'KJJLB', 'title': '科技奖类别', 'editable': 'true', 'type': 'text', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'JLDJM', 'title': '奖励等级码', 'editable': 'true', 'type': 'inline', 'create': 'True', 'value': 'st_jldj:DM AS JLDJM ,MC', 'where': ''},
            {'table': 'dr_hjcgjbsjxx', 'field': 'HJJBM', 'title': '获奖级别码', 'editable': 'true', 'type': 'inline', 'create': 'True', 'value': 'st_xx_jb:DM AS HJJBM ,MC', 'where': ''},
            {'table': 'dr_hjcgjbsjxx', 'field': 'BJDW', 'title': '颁奖单位', 'editable': 'T', 'type': 'text', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'SSXMBH', 'title': '所属项目编号', 'editable': 'T', 'type': 'text', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'DWPM', 'title': '单位排名', 'editable': 'T', 'type': 'text', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'CGXS', 'title': '成果形式', 'editable': 'T', 'type': 'text', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]


    @staticmethod
    def get_search_columns() -> []:
        return ['HJCGMC', 'FZRXM']


class VIEW_KJCGRYXX_JL(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_kjcgryxx_jl'
    __tablename__CH__ = '科技成果(获奖成果)人员信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    RYH = Column('RYH', String(16), unique=True, default='')  # 人员号
    JSM = Column('JSM', String(16), default='')  # 角色码
    ZXZS = Column('ZXZS', String(16), default='')  # 撰写字数
    PMZRS = Column('PMZRS', String(16), default='')  # 排名/总人数
    GXL = Column('GXL', Float, default=0.0)  # 贡献率
    XM = Column('XM', String(16), default='')  # 姓名
    SZDW = Column('SZDW', String(16), default='')  # 所在单位
    DWH = Column('DWH', String(16), default='')  # 单位号
    RYLX = Column('RYLX', String(16), default='')  # 人员类型
    HJCGBH = Column('HJCGBH', String(16), default='')  # 获奖成果编号
    KJCGRYBH = Column('KJCGRYBH', String(16), default='')  # 科技成果人员编号
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注
    JLDJM = Column('JLDJM', String(16), default='')  # 奖励等级码
    HJJBM = Column('HJJBM', String(16), default='')  # 获奖级别码
    CGHJLBM = Column('CGHJLBM', String(16), default='')  # 成果获奖类别码
    FZRXM = Column('FZRXM', String(16), default='')  # 负责人姓名

    @staticmethod
    def sql() -> str:
        sql_v1 = """
        CREATE VIEW view_kjcgryxx_jl AS
        select
           dr_kjcg_jl.id AS id,
           dr_kjcg_jl.RYH AS RYH,
           dr_kjcg_jl.XM AS XM,
           dr_kjcg_jl.JSM AS JSM,
           dr_kjcg_jl.ZXZS AS ZXZS,
           dr_kjcg_jl.PMZRS AS PMZRS,
           dr_kjcg_jl.GXL AS GXL,
           dr_kjcg_jl.SZDW AS SZDW,
           dr_kjcg_jl.RYLX AS RYLX,
           dr_kjcg_jl.HJCGBH AS HJCGBH,
           dr_kjcg_jl.KJCGRYBH AS KJCGRYBH,
           dr_kjcg_jl.RYH AS JZGH,
           dr_hjcg.HJRQ AS stamp,
           dr_kjcg_jl.note AS note,
           dr_hjcg.HJRQ AS HJRQ,
           dr_hjcg.FZRXM AS FZRXM,
           dr_hjcg.DWMC AS DWMC,
           dr_hjcg.DWH AS DWH,
           dr_hjcg.CGHJLBM AS CGHJLBM,
           dr_hjcg.JLDJM AS JLDJM,
           dr_hjcg.HJJBM AS HJJBM
        from dr_kjcgryxx_jl dr_kjcg_jl
        LEFT JOIN dr_hjcgjbsjxx dr_hjcg on dr_kjcg_jl.HJCGBH = dr_hjcg.HJCGBH
        WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_kjcgryxx_jl', 'dr_hjcgjbsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_kjcgryxx_jl']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_kjcgryxx_jl']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_kjcgryxx_jl', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_kjcgryxx_jl', 'field': 'HJCGBH', 'title': '获奖成果名称', 'editable': 'T', 'type': 'inline', 'create': 'T', 'value': 'dr_hjcgjbsjxx:HJCGBH,HJCGMC', 'where': '',},
            {'table': 'dr_kjcgryxx_jl', 'field': 'RYH', 'title': '人员号', 'editable': 'T', 'type': 'text', 'create': 'F', },
            {'table': 'dr_kjcgryxx_jl', 'field': 'XM', 'title': '姓名', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_jzgjcsjxx:JZGH AS RYH,XM', 'where': "DWH IN %(departments)s AND JZGH!='admin'" },
            {'table': 'dr_kjcgryxx_jl', 'field': 'PMZRS', 'title': '排名/总人数', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_jl', 'field': 'GXL', 'title': '贡献率', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'CGHJLBM', 'title': '成果获奖类别码', 'editable': 'False', 'type': 'inline','create': 'False', 'value': 'st_ky_cghjlb:DM AS CGHJLBM,MC', 'where': ''},
            {'table': 'dr_hjcgjbsjxx', 'field': 'JLDJM', 'title': '奖励等级码', 'editable': 'False', 'type': 'inline','create': 'False', 'value': 'st_jldj:JLDJM,JLDJMC', 'where': ''},
            {'table': 'dr_hjcgjbsjxx', 'field': 'HJJBM', 'title': '获奖级别码', 'editable': 'False', 'type': 'text','create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'KJJLB', 'title': '科技奖类别', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]


    @staticmethod
    def get_search_columns() -> []:
        return ['XM']



#yangchen
class VIEW_ZLCGJBSJXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_zlcgjbsjxx'
    __tablename__CH__ = '专利成果基本数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    ZLCGBH = Column('ZLCGBH', String(16), default='')  # 专利成果编号
    ZLCGMC = Column('ZLCGMC', String(128),default='')  # 专利成果名称
    DWH = Column('DWH', String(128),default='')  # 单位号
    SQBH= Column('SQBH', String(16), default='')  # 申请编号
    XKLYM= Column('XKLYM', String(16), default='')  # 学科领域
    ZLLXM = Column('ZLLXM', String(16), default='')  # 专利类型码
    PZRQ= Column('PZRQ', DateTime, default=now())  # 批准日期
    PZXSM = Column('PZXSM', String(16),  default='')  # 批准形式码
    ZLZSBH = Column('ZLZSBH', String(16),  default='')  # 专利证书编号
    FLZTM = Column('FLZTM', String(16), default='')  # 法律状态码
    JNZLNFRQ = Column('JNZLNFRQ', DateTime, default=now())  # 交纳专利年费日期
    JNJE = Column('JNJE', String(16), default='')  # 交纳金额
    SSXMBH = Column('SSXMBH', String(16), default='')  # 所属项目编号
    GJDQM = Column('GJDQM', String(16), default='')  # 国籍/地区码
    GJZLZFLH = Column('GJZLZFLH', String(16), default='')  # 国际专利主分类号
    PCTHZLGJDQM = Column('PCTHZLGJDQM', String(16), default='')  # PCT 或专利国家/地区码
    SQGGH = Column('SQGGH', String(16), default='')  # 授权公告号
    SQGGRQ = Column('SQGGRQ', DateTime, default=now())  # 授权公告日期
    SQMC = Column('SQMC', String(16), default='')  # 申请名称
    ZLDLJG = Column('ZLDLJG', String(30), default='')  # 专利代理机构
    ZLDLR = Column('ZLDLR', String(16), default='')  # 专利代理人
    ZLQR = Column('ZLQR', String(16), default='')  # 专利权人
    ZLZZRQ = Column('ZLZZRQ', DateTime, default=now())  # 专利终止日期
    XKMLKJM = Column('XKMLKJM', String(16), default='')  # 学科门类(科技)码
    ZLSQRQ = Column('ZLSQRQ', DateTime, default=now())  # 专利申请日期
    ZZM = Column('ZZM', String(16), default='')  # 作者名
    ZZBH = Column('ZZBH', String(16), default='')  # 作者编号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
        CREATE VIEW view_zlcgjbsjxx AS
        select
           dr_zl.id as id,
           dr_zl.ZLCGBH as ZLCGBH,
           dr_zl.ZLCGMC as ZLCGMC,
           dr_zl.DWH as DWH,
           dr_zl.SQBH as SQBH,
           dr_zl.XKLYM as XKLYM,
           dr_zl.ZLLXM as ZLLXM,
           dr_zl.PZRQ as PZRQ,
           dr_zl.PZXSM as PZXSM,
           dr_zl.ZLZSBH as ZLZSBH,
           dr_zl.FLZTM as FLZTM,
           dr_zl.JNZLNFRQ as JNZLNFRQ,
           dr_zl.JNJE as JNJE,
           dr_zl.SSXMBH as SSXMBH,
           dr_zl.GJDQM as GJDQM,
           dr_zl.GJZLZFLH as GJZLZFLH,
           dr_zl.PCTHZLGJDQM as PCTHZLGJDQM,
           dr_zl.SQGGH as SQGGH,
           dr_zl.SQGGRQ as SQGGRQ,
           dr_zl.SQMC as SQMC,
           dr_zl.ZLDLJG as ZLDLJG,
           dr_zl.ZLDLR as ZLDLR,
           dr_zl.ZLQR as ZLQR,
           dr_zl.ZLZZRQ as ZLZZRQ,
           dr_zl.XKMLKJM as XKMLKJM,
           dr_zl.ZLSQRQ as ZLSQRQ,
           dr_zl.ZZM as ZZM,
           dr_zl.ZZBH as ZZBH,
           dr_zl.PZRQ as stamp,
           dr_zl.note as note
        from dr_zlcgjbsjxx dr_zl
        left join dc_zlcgjbsjxx dc_zl on dr_zl.ZLCGBH = dc_zl.ZLCGBH
        where 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_zlcgjbsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_zlcgjbsjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_zlcgjbsjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return[
            {'table': 'dr_zlcgjbsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text','create': 'False', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLCGBH', 'title': '专利成果编号', 'editable': 'T', 'type': 'text','create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLCGMC', 'title': '专利成果名称', 'editable': 'T', 'type': 'text','create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'T', 'type': 'inline','create': 'T', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_zlcgjbsjxx', 'field': 'SQBH', 'title': '申请编号', 'editable': 'T', 'type': 'text','create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLLXM', 'title': '专利类型码', 'editable': 'T', 'type': 'inline','create': 'T', },#need value
            {'table': 'dr_zlcgjbsjxx', 'field': 'PZRQ', 'title': '批准日期', 'editable': 'T', 'type': 'date','create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'PZXSM', 'title': '批准形式码', 'editable': 'T', 'type': 'inline','create': 'T', }, #need value
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLZSBH', 'title': '专利证书编号', 'editable': 'T', 'type': 'text','create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'FLZTM', 'title': '法律状态码', 'editable': 'T', 'type': 'inline','create': 'T', }, #need value
            {'table': 'dr_zlcgjbsjxx', 'field': 'SQGGH', 'title': '授权公告号', 'editable': 'T', 'type': 'text','create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'SQGGRQ', 'title': '授权公告日期', 'editable': 'T', 'type': 'data','create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'SQMC', 'title': '申请名称', 'editable': 'T', 'type': 'text','create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLDLJG', 'title': '专利代理机构', 'editable': 'T', 'type': 'text','create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLDLR', 'title': '专利代理人', 'editable': 'T', 'type': 'text','create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLQR', 'title': '专利权人', 'editable': 'T', 'type': 'text','create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'XKMLKJM', 'title': '学科门类(科技)码', 'editable': 'T', 'type': 'text','create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLSQRQ', 'title': '专利申请日期', 'editable': 'T', 'type': 'data','create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZZM', 'title': '作者名', 'editable': 'T', 'type': 'table','create': 'T', 'value': 'dr_jzgjcsjxx:JZGH AS ZZBH,XM AS ZZM', 'where': "DWH IN %(departments)s AND JZGH!='admin'"},
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZZBH', 'title': '作者编号', 'editable': 'T', 'type': 'text','create': 'F',},
        ]

    @staticmethod
    def get_search_columns() -> []:
        return ['ZLCGMC']


class VIEW_XMRYXX(Base):
    # FanMing
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_xmryxx'
    __tablename__CH__ = '项目人员信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    XMBH = Column('XMBH', String(16), default='')  # 项目编号
    RYH = Column('RYH', String(16), default='')  # 人员号
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    XM = Column('XM', String(16), default='')  # 姓名
    DWH = Column('DWH', String(16), default='')  # 单位号
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    CSRQ = Column('CSRQ', DateTime, default=now())  # 出生日期
    GZL = Column('GZL', Float, default=0.0)  # 工作量
    MNGZYS = Column('MNGZYS', Float, default=0.0)  # 每年工作月数
    JSM = Column('JSM', String(16), default='')  # 角色码
    RYLX = Column('RYLX', String(16), default='')  # 人员类型
    SMSX = Column('SMSX', String(16), default='')  # 署名顺序
    XMBH = Column('XMBH', String(16), default='')  # 项目编号
    XKMLKJM = Column('XKMLKJM', String(16), default='')  # 学科门类(科技)码
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_xmryxx AS
            SELECT 
                dr.id AS id,            
                dr.RYH AS RYH, 
                dr.RYH AS JZGH, 
                jz.XM AS XM,
                jz.DWH AS DWH,
                jz.DWMC AS DWMC, 
                jz.CSRQ AS CSRQ,   
                dr.XMBH AS XMBH,
                dr.GZL AS GZL,
                dr.MNGZYS AS MNGZYS,
                dr.JSM AS JSM,
                dr.RYLX AS RYLX,
                dr.SMSX AS SMSX,
                dr.XKMLKJM AS XKMLKJM,
                dr.stamp AS stamp,
                dr.note AS note
            FROM dr_xmryxx dr
            LEFT JOIN view_jzgjcsjxx jz ON jz.JZGH=dr.RYH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_xmryxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_xmryxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_xmryxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_xmryxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },

            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {
                'table': 'dr_zzjgjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'False',
                'type': 'table', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s', 'create': 'True',
                'action': [{
                    'type': 'onclick',
                    'content': {'value': 'view_jzgjcsjxx:JZGH,XM', 'where': 'DWH IN :this', 'to': 'RYH:JZGH,XM', },
                }],
            },
            {'table': 'dr_xmryxx', 'field': 'RYH', 'title': '人员号', 'editable': 'False', 'type': 'inline', 'create': 'T', },

            {'table': 'dr_jzgjcsjxx', 'field': 'XM', 'title': '姓名', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_xmryxx', 'field': 'XMBH', 'title': '项目编号', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmryxx', 'field': 'GZL', 'title': '工作量', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmryxx', 'field': 'MNGZYS', 'title': '每年工作月数', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmryxx', 'field': 'JSM', 'title': '角色码', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmryxx', 'field': 'RYLX', 'title': '人员类型', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmryxx', 'field': 'SMSX', 'title': '署名顺序', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmryxx', 'field': 'XKMLKJM', 'title': '学科门类(科技)码', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmryxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_xmryxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List:
        return ['JZGH', 'XMBH']


class_dict = {key: var for key, var in locals().items() if isinstance(var, type)}


def generate_class_view(name='module', create_view=True):
    """
    Generate view for rule_engine/FE to run after module.py changed.
    :param name: module to generate
    :param create_view: True - drop/create view, False - generate view structure for FE
    :return:
    """
    cdf = []

    try:
        module = __import__('jx.' + name, fromlist=([name]))
    except ImportError:
        module = __import__(name)
    from pymysql.err import Error

    for k, v in module.class_dict.items():
        if k.find('VIEW_') == -1 and k.find('KH_') == -1:
            continue

        v_class = getattr(module, k)

        if create_view:  # drop/create view
            print('Processing ' + k + ':')
            try:
                print("1. DROP VIEW " + v_class.__tablename__.replace('kh_', 'view_'))
                cursor.execute("DROP VIEW " + v_class.__tablename__.replace('kh_', 'view_'))
            except Error as e:
                print(e)
            except Exception as e:
                print(e)

            print('2. ' + v_class.sql())
            cursor.execute(v_class.sql())

        else:  # generate view structure for FE
            cdf.append({
                'class': k[k.find('VIEW_') + 5:],
                'name': v_class.__tablename__CH__,
                'columns': v_class.get_title_columns()
            })

    return cdf


def modify_table_stamp(name='model_dr'):
    try:
        module = __import__('jx.' + name, fromlist=([name]))
    except ImportError:
        module = __import__(name)
    from pymysql.err import Error

    for k, v in module.class_dict.items():
        if k.find('DR_') == -1 and k.find('DC_') == -1:
            continue

        print('Processing ' + k + ':')
        v_class = getattr(module, k)

        try:
            print("ALTER TABLE " + v_class.__tablename__ + " MODIFY stamp TIMESTAMP(6);")
            cursor.execute("ALTER TABLE " + v_class.__tablename__ + " MODIFY stamp TIMESTAMP(6);")
        except Error as e:
            print(e)
        except Exception as e:
            print(e)

    return


def generate_sysuser_view():
    from pymysql.err import Error
    try:
        # DON'T touch below SQL which related to auto management
        sql_drop = "DROP VIEW view_sysuser"
        sql_create = """
            CREATE VIEW view_sysuser AS
            SELECT su.*, ro.role_name, jg.JZGH, jg.XM, jg.DWH, zz.DWMC
            FROM jx_sysuser su
            LEFT JOIN jx_role ro ON ro.id=su.role_id
            LEFT JOIN view_jzgjcsjxx jg ON jg.JZGH=su.payroll
            LEFT JOIN view_zzjgjbsjxx zz ON zz.DWH=jg.DWH
        """
        print(sql_drop)
        cursor.execute(sql_drop)
        print(sql_create)
        cursor.execute(sql_create)
    except Error as e:
        print(e)
    except Exception as e:
        print(e)

    return


if __name__ == '__main__':

    print(generate_class_view(name='module', create_view=False))
    generate_class_view()

    modify_table_stamp('model_dr')
    modify_table_stamp('model_dc')

    generate_sysuser_view()

    exit(0)
