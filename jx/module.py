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

            if dpmts:
                for dpmt in dpmts:
                    import time
                    time.sleep(0.001)
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

            if dpmts:
                for dpmt in dpmts:
                    return str(dpmt.LSDWH)

        except PendingRollbackError:
            db.rollback()
            logger.error(sys_info())

        except:
            logger.error(sys_info())

        return ''


class VIEW_BJSJXX(Base):
    """
班级数据信息
[描  述]本数据类规定了有关（行政）班级的基本数据项。 表 4 班级数据信息(BJSJXX)
数据项名 中文简称 类型 值空间 归属部门
BH 班号 C  教务处、研究生院、学生处
BJ 班级 C  教务处、研究生院、学生处
JBNY 建班年月 C  教务处、研究生院、学生处
RXNF 入学年份 C  教务处、研究生院、学生处
FDYH 辅导员号 C(8)  教务处、研究生院、学生处
BDS 班导师 C(8)  教务处、研究生院、学生处
SSXY 所属学院 C(6) ZZJGJBSJXX 组织机构基本数据信息 教务处、研究生院、学生处
SSZY 所属专业 C  教务处、研究生院、学生处
XSLB 学生类别 C  教务处、研究生院、学生处
QYBZ 启用标志 C  教务处、研究生院、学
    """

    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_bjsjxx'
    __tablename__CH__ = '班级数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    BH = Column('BH', String(16), default='')  # 班号
    BJ = Column('BJ', String(16), default='')  # 班级
    JBNY = Column('JBNY', DateTime, default=now())  # 建班年月
    RXNF = Column('RXNF', DateTime, default=now())  # 入学年份
    FDYH = Column('FDYH', String(16), default='')  # 辅导员号
    BDS = Column('BDS', String(16), default='')  # 班导师
    SSXY = Column('SSXY', String(16), default='')  # 所属学院
    SSZY = Column('SSZY', String(16), default='')  # 所属专业
    XSLB = Column('XSLB', String(16), default='')  # 学生类别
    QYBZ = Column('QYBZ', String(16), default='')  # 启用标志

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_bjsjxx AS
            SELECT 
                dr.id AS id,            
                dr.BH AS BH,            
                dr.BJ AS BJ,            
                dr.JBNY AS JBNY,            
                dr.RXNF AS RXNF,             
                dr.FDYH AS FDYH,            
                fdy.XM AS FDYXM,            
                dr.BDS AS BDS,            
                bds.XM AS BDSXM,            
                dr.SSXY AS DWH,            
                dr.SSXY AS SSXY,            
                zzjg.DWMC AS SSXYMC,            
                dr.SSZY AS SSZY,     
                dr.XSLB AS XSLB,         
                dr.QYBZ AS QYBZ,    
                dr.stamp AS stamp,            
                dr.note AS note            
            FROM dr_bjsjxx dr
            LEFT JOIN dr_jzgjcsjxx bds on bds.JZGH = dr.BDS
            LEFT JOIN dr_jzgjcsjxx fdy on fdy.JZGH = dr.FDYH
            LEFT JOIN dr_zzjgjbsjxx zzjg ON zzjg.DWH=dr.SSXY
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_bjsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_bjsjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_bjsjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_bjsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_bjsjxx', 'field': 'BH', 'title': '班号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_bjsjxx', 'field': 'BJ', 'title': '班级', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_bjsjxx', 'field': 'JBNY', 'title': '建班年月', 'editable': 'True', 'type': 'date', 'create': 'True', },
            {'table': 'dr_bjsjxx', 'field': 'RXNF', 'title': '入学年份', 'editable': 'True', 'type': 'year', 'create': 'True', },
            {'table': 'dr_bjsjxx', 'field': 'FDYH', 'title': '辅导员号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_bjsjxx', 'field': 'FDYXM', 'title': '辅导员姓名', 'editable': 'True', 'type': 'table', 'create': 'True','value': 'dr_jzgjcsjxx:JZGH AS FDYH,XM AS FDYXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", },
            {'table': 'dr_bjsjxx', 'field': 'BDS', 'title': '班导师', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_bjsjxx', 'field': 'BDSXM', 'title': '班导师姓名', 'editable': 'True', 'type': 'table', 'create': 'True', 'value': 'dr_jzgjcsjxx:JZGH AS BDS,XM AS BDSXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'",},
            {'table': 'dr_bjsjxx', 'field': 'SSXY', 'title': '所属学院', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_bjsjxx', 'field': 'SSXYMC', 'title': '所属学院名称', 'editable': 'True', 'type': 'table', 'create': 'True', 'value': 'dr_zzjgjbsjxx:DWH AS SSXY,DWMC AS SSXYMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_bjsjxx', 'field': 'SSZY', 'title': '所属专业', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_bjsjxx', 'field': 'XSLB', 'title': '学生类别', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_bjsjxx', 'field': 'QYBZ', 'title': '启用标志', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_bjsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_bjsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['BH', 'BJ', 'SSXYMC']


class VIEW_KCSJXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_kcsjxx'
    __tablename__CH__ = '课程数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    DWH = Column('DWH', String(16), default='')  # 单位号
    KCH = Column('KCH', String(16), unique=True, default='')  # 课程号
    KCMC = Column('KCMC', String(16), default='')  # 课程名称
    ZXS = Column('ZXS', String(16), default='')  # 总学时
    LLXS = Column('LLXS', String(16), default='')  # 理论学时
    SYXS = Column('SYXS', String(16), default='')  # 实验学时
    SJXS = Column('SJXS', String(16), default='')  # 实践学时
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_kcsjxx AS
            SELECT 
                kc.id AS id,            
                kc.JZGH AS JZGH,     
                kc.KCH AS KCH,            
                kc.KCMC AS KCMC,            
                kc.ZXS AS ZXS,            
                kc.LLXS AS LLXS,  
                kc.SYXS AS SYXS,  
                kc.SJXS AS SJXS,                             
                dr_jzg.DWH AS DWH,        
                kc.stamp AS stamp,          
                kc.note AS note      
            FROM dr_kcsjxx kc
            left join dr_jzgjcsjxx dr_jzg on dr_jzg.JZGH = kc.JZGH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_kcsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_kcsjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_kcsjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note','KCMC','DWH']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_kcsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_kcsjxx', 'field': 'JZGH', 'title': '教职工号', 'editable': 'False', 'type': 'text','create': 'False', },
            {'table': 'dr_kcsjxx', 'field': 'KCH', 'title': '课程号', 'editable': 'False', 'type': 'text','create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'KCMC', 'title': '课程名称', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_kcsjxx', 'field': 'ZXS', 'title': '总学时', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'LLXS', 'title': '理论学时', 'editable': 'False', 'type': 'text','create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'SYXS', 'title': '实验学时', 'editable': 'True', 'type': 'text','create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'SJXS', 'title': '实践学时', 'editable': 'True', 'type': 'text','create': 'True', },
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text','create': 'false', },
            {'table': 'dr_kcsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_kcsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['KCH']


class VIEW_XNXQXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_xnxqxx'
    __tablename__CH__ = '学年学期信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    XQQSSJ = Column('XQQSSJ', DateTime, default=now())  # 学期起始时间
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    DWH = Column('DWH', String(16), default='')  # 单位号
    XQMC = Column('XQMC', String(16), default='')  # 学期名称
    XNXQM = Column('XNXQM', String(16), default='')  # 学年学期名
    XNDM = Column('XNDM', String(16), default='')  # 学年代码
    XQDM = Column('XQDM', String(16), default='')  # 学期代码
    XNMC = Column('XNMC', String(16), default='')  # 学年名称
    QSSKZ = Column('QSSKZ', String(16), default='')  # 起始上课周
    ZZSKZ = Column('ZZSKZ', String(16), default='')  # 终止上课周
    XQLXDM = Column('XQLXDM', String(16), default='')  # 学期类型代码
    XQLXMC = Column('XQLXMC', String(16), default='')  # 学期类型名称
    SFDQXQ = Column('SFDQXQ', String(16), default='')  # 是否当前学期
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_xnxqxx AS
            SELECT 
                xn.id AS id,            
                xn.JZGH AS JZGH, 
                xn.XQMC AS XQMC,     
                xn.XQQSSJ AS XQQSSJ,            
                xn.XNXQM AS XNXQM,            
                xn.XNDM AS XNDM,            
                xn.XQDM AS XQDM,  
                xn.XNMC AS XNMC,  
                xn.QSSKZ AS QSSKZ,    
                xn.ZZSKZ AS ZZSKZ,   
                xn.XQLXDM AS XQLXDM,            
                xn.XQLXMC AS XQLXMC,            
                xn.SFDQXQ AS SFDQXQ,  
                dr_jzg.DWH AS DWH,        
                xn.XQQSSJ AS stamp,          
                xn.note AS note      
            FROM dr_xnxqxx xn
            left join dr_jzgjcsjxx dr_jzg on dr_jzg.JZGH = xn.JZGH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_xnxqxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_xnxqxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_xnxqxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note','SFDQXQ','XQMC','XNXQM','XNMC','XQLXDM','XQLXMC','DWH']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_xnxqxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_xnxqxx', 'field': 'JZGH', 'title': '教职工号', 'editable': 'False', 'type': 'text','create': 'False', },
            {'table': 'dr_xnxqxx', 'field': 'XQMC', 'title': '学期名称', 'editable': 'False', 'type': 'text','create': 'False', },
            {'table': 'dr_xnxqxx', 'field': 'XNXQM', 'title': '学年学期名', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_xnxqxx', 'field': 'XNDM', 'title': '学年代码', 'editable': 'False', 'type': 'year', 'create': 'True', },
            {'table': 'dr_xnxqxx', 'field': 'XQDM', 'title': '学期代码', 'editable': 'False', 'type': 'month','create': 'True', },
            {'table': 'dr_xnxqxx', 'field': 'XNMC', 'title': '学年名称', 'editable': 'True', 'type': 'inline','create': 'False', },
            {'table': 'dr_xnxqxx', 'field': 'QSSKZ', 'title': '起始上课周', 'editable': 'True', 'type': 'date','create': 'True', },
            {'table': 'dr_xnxqxx', 'field': 'ZZSKZ', 'title': '终止上课周', 'editable': 'True', 'type': 'date','create': 'True', },
            {'table': 'dr_xnxqxx', 'field': 'XQLXDM', 'title': '学期类型代码', 'editable': 'True', 'type': 'inline','create': 'False', },
            {'table': 'dr_xnxqxx', 'field': 'XQLXMC', 'title': '学期类型名称', 'editable': 'True', 'type': 'inline','create': 'False', },
            {'table': 'dr_xnxqxx', 'field': 'SFDQXQ', 'title': '是否当前学期', 'editable': 'True', 'type': 'inline','create': 'False', },
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text','create': 'false', },
            {'table': 'dr_xnxqxx', 'field': 'XQQSSJ', 'title': '学期起始时间', 'editable': 'True', 'type': 'date','create': 'True', },
            {'table': 'dr_xnxqxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_xnxqxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['XNDM']


class VIEW_BKS_JPKC(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_bks_jpkc'
    __tablename__CH__ = '本科生精品课程'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    FZRGH = Column('FZRGH', String(16), default='')  # 负责人工号
    FZRXM = Column('FZRXM', String(16), default='')  # 负责人姓名
    KCH = Column('KCH', String(16), default='')  # 课程号
    KCMC = Column('KCMC', String(16), default='')  # 课程名称
    KCJBM = Column('KCJBM', String(16), default='')  # 课程级别码
    DWH = Column('DWH', String(16), default='')  # 单位号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_bks_jpkc AS
            SELECT 
                jp.id AS id,            
                jp.KCH AS KCH,            
                jp.KCMC AS KCMC,            
                jp.KCJBM AS KCJBM,            
                jp.FZRGH AS FZRGH,  
                jp.FZRXM AS FZRXM,  
                jp.DWH AS DWH,    
                jp.stamp AS stamp,            
                jp.note AS note      
            FROM dr_bks_jpkc jp
            LEFT JOIN dr_kcsjxx kc ON kc.KCH=jp.KCH
            LEFT JOIN dr_zzjgjbsjxx zzjg ON zzjg.DWH=jp.DWH
            left join dr_jzgjcsjxx dr_jzg on dr_jzg.JZGH = jp.FZRGH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_bks_jpkc']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_bks_jpkc']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_bks_jpkc']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_bks_jpkc', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_bks_jpkc', 'field': 'FZRGH', 'title': '负责人工号', 'editable': 'False', 'type': 'text','create': 'False', },
            {'table': 'dr_bks_jpkc', 'field': 'FZRXM', 'title': '负责人姓名', 'editable': 'False', 'type': 'inline', 'value': "dr_jzgjcsjxx:JZGH AS FZRGH,XM AS FZRXM", 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'True', },
            {'table': 'dr_bks_jpkc', 'field': 'KCH', 'title': '课程号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_bks_jpkc', 'field': 'KCMC', 'title': '课程名称', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_bks_jpkc', 'field': 'KCJBM', 'title': '课程级别码', 'editable': 'False', 'type': 'text','create': 'True', },
            {'table': 'dr_bks_jpkc', 'field': 'DWH', 'title': '单位号', 'editable': 'True', 'type': 'inline','create': 'True', },
            {'table': 'dr_bks_jpkc', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_bks_jpkc', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['KCH']


class VIEW_YJSJXZXS(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_yjsjxzxs'
    __tablename__CH__ = '研究生理论课学时数'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JZGH = Column('JZGH', String(16), default='')  # 教师工号
    JSGH = Column('JSGH', String(16), default='')  # 教师工号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KCH = Column('KCH', String(16), unique=True, default='')  # 课程号
    KKXND = Column('KKXND', String(16), default='')  # 开课学年度
    SKBJH = Column('SKBJH', String(16), default='')  # 上课班级号
    KKXQM = Column('KKXQM', DateTime, default=now())  # 开课学期码
    ZKJHXS = Column('ZKJHXS', String(16), default='')  # 助课计划学时
    JHXSS = Column('JHXSS', Float(16), default='')  # 计划学时数
    KCJBM = Column('KCJBM', String(16), default='')  # 课程级别码
    JXMSJBM = Column('JXMSJBM', String(16), default='')  # 教学名师级别码
    WYKCTJM = Column('WYKCTJM', String(16), default='')  # 外语课程调节码
    ZLXS = Column('ZLXS', String(16), default='')  # 质量系数
    # BH = Column('BH', String(16), default='')  # 班号
    HBS = Column('HBS', String(16), default='')  # 合班数
    DWH = Column('DWH', String(16), default='')  # 单位号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_yjsjxzxs AS
            SELECT 
                pk.id AS id,            
                pk.JSGH AS JSGH, 
                pk.JSGH AS JZGH, 
                pk.JSXM AS JSXM,            
                pk.KKXND AS KKXND,            
                pk.KKXQM AS KKXQM,            
                kc.LLXS AS JHXSS,  
                pk.ZKJHXS AS ZKJHXS,     
                pk.ZLXS AS ZLXS,            
                pk.HBS AS HBS,      
                pk.SKBJH AS SKBJH,         
                pk.WYKCTJM AS WYKCTJM,            
                pk.JXMSJBM AS JXMSJBM,     
                pk.KCJBM AS KCJBM, 
                kc.KCH AS KCH,           
                dr_jzg.DWH AS DWH,        
                xn.XQQSSJ AS stamp,            
                pk.note AS note            
            FROM dr_yjspksjxx pk
            LEFT JOIN dr_kcsjxx kc ON kc.KCH=pk.KCH
            LEFT JOIN dr_xnxqxx xn ON xn.XQQSSJ=pk.KKXQM
            # LEFT JOIN dr_bks_jpkc jp ON jp.KCH=pk.KCH
            left join dr_jzgjcsjxx dr_jzg on dr_jzg.JZGH = pk.JSGH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_yjspksjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_yjspksjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_yjspksjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note','DWH','ZKJHXS','JXMSJBM','ZLXS','HBS','SKBJH']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_yjspksjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_yjspksjxx', 'field': 'JSGH', 'title': '教师工号', 'editable': 'False', 'type': 'text','create': 'False', },
            {'table': 'dr_yjspksjxx', 'field': 'JSXM', 'title': '教师姓名', 'editable': 'False', 'type': 'table','value': "dr_jzgjcsjxx:JZGH AS JSGH,XM AS JSXM", 'where': "DWH IN %(departments)s AND JZGH!='admin'",'create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'KCH', 'title': '课程号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'JHXSS', 'title': '计划学时数', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_yjspksjxx', 'field': 'ZKJHXS', 'title': '助课计划学时', 'editable': 'False', 'type': 'text','create': 'False', },

            # {'table': 'dr_bks_jpkc', 'field': 'KCJBM', 'title': '课程级别码', 'editable': 'True', 'type': 'text', 'create': 'True', },
            # {'table': 'dr_pksjxx', 'field': 'JXMSJBM', 'title': '教学名师级别码', 'editable': 'False', 'type': 'text', 'create': 'True', },
            # {'table': 'dr_pksjxx', 'field': 'WYKCTJM', 'title': '外语课程调节码', 'editable': 'False', 'type': 'text', 'create': 'True', },

            {'table': 'dr_yjspksjxx', 'field': 'KCJBM', 'title': '课程级别码', 'editable': 'True', 'type': 'inline','create': 'True', 'value': 'st_kcjbm:DM AS KCJBM,MC', 'where': ''},
            {'table': 'dr_yjspksjxx', 'field': 'JXMSJBM', 'title': '教学名师级别码', 'editable': 'T', 'type': 'inline','create': 'False', 'value': 'st_jxmsjbm:DM AS JXMSJBM,MC', 'where': ''},
            {'table': 'dr_yjspksjxx', 'field': 'WYKCTJM', 'title': '外语课程调节码', 'editable': 'T', 'type': 'inline','create': 'True', 'value': 'st_wykctjm:DM AS WYKCTJM,MC', 'where': ''},

            {'table': 'dr_yjspksjxx', 'field': 'ZLXS', 'title': '质量系数', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_yjspksjxx', 'field': 'KKXQM', 'title': '开课学期码', 'editable': 'False', 'type': 'date', 'create': 'True', },
            {'table': 'dr_yjspksjxx', 'field': 'KKXND', 'title': '开课学年度', 'editable': 'False', 'type': 'year', 'create': 'True', },
            {'table': 'dr_yjspksjxx', 'field': 'HBS', 'title': '合班数', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_yjspksjxx', 'field': 'SKBJH', 'title': '上课班级号', 'editable': 'T', 'type': 'text', 'create': 'False', },
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'false', },
            {'table': 'dr_yjspksjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_yjspksjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['JZGH']


# looks like out of date by why@20210524
'''
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
'''


class VIEW_BKSJXZXS(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_bksjxzxs'
    __tablename__CH__ = '本科生理论课学时数'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JZGH = Column('JZGH', String(16), default='')  # 教师工号
    JSGH = Column('JSGH', String(16), default='')  # 教师工号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KCH = Column('KCH', String(16), unique=True, default='')  # 课程号
    KKXND = Column('KKXND', String(16), default='')  # 开课学年度
    SKBJH = Column('SKBJH', String(16), default='')  # 上课班级号
    KKXQM = Column('KKXQM', DateTime, default=now())  # 开课学期码
    ZKJHXS = Column('ZKJHXS', String(16), default='')  # 助课计划学时
    JHXSS = Column('JHXSS', Float(16), default='')  # 计划学时数
    KCJBM = Column('KCJBM', String(16), default='')  # 课程级别码
    JXMSJBM = Column('JXMSJBM', String(16), default='')  # 教学名师级别码
    WYKCTJM = Column('WYKCTJM', String(16), default='')  # 外语课程调节码
    ZLXS = Column('ZLXS', Float(16), default='')  # 质量系数
    HBS = Column('HBS', Float(16), default='')  # 合班数
    DWH = Column('DWH', String(16), default='')  # 单位号
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_bksjxzxs AS
            SELECT 
                pk.id AS id,            
                pk.JSGH AS JSGH, 
                pk.JSGH AS JZGH, 
                pk.JSXM AS JSXM,            
                pk.KKXND AS KKXND,            
                pk.KKXQM AS KKXQM,            
                kc.LLXS AS JHXSS,  
                pk.ZKJHXS AS ZKJHXS,     
                pk.ZLXS AS ZLXS,            
                pk.HBS AS HBS,      
                pk.SKBJH AS SKBJH,         
                pk.WYKCTJM AS WYKCTJM,            
                pk.JXMSJBM AS JXMSJBM,     
                pk.KCJBM AS KCJBM, 
                kc.KCH AS KCH,           
                pk.DWH AS DWH,        
                pk.DWMC AS DWMC,
                xn.XQQSSJ AS stamp,            
                pk.note AS note            
            FROM dr_pksjxx pk
            LEFT JOIN dr_kcsjxx kc ON kc.KCH=pk.KCH
            LEFT JOIN dr_xnxqxx xn ON xn.XQQSSJ=pk.KKXQM
            LEFT JOIN dr_zzjgjbsjxx zz ON zz.DWH=pk.DWH
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
        return ['id', 'stamp', 'note','DWH','DWMC']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_pksjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_pksjxx', 'field': 'JSGH', 'title': '教师工号', 'editable': 'False', 'type': 'text','create': 'False', },
            {'table': 'dr_pksjxx', 'field': 'JSXM', 'title': '教师姓名', 'editable': 'False', 'type': 'table','value': "dr_jzgjcsjxx:JZGH AS JSGH,XM AS JSXM", 'where': "DWH IN %(departments)s AND JZGH!='admin'",'create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'KCH', 'title': '课程号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'JHXSS', 'title': '计划学时数', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_pksjxx', 'field': 'ZKJHXS', 'title': '助课计划学时', 'editable': 'False', 'type': 'text','create': 'True', },

            # {'table': 'dr_bks_jpkc', 'field': 'KCJBM', 'title': '课程级别码', 'editable': 'True', 'type': 'text', 'create': 'True', },
            # {'table': 'dr_pksjxx', 'field': 'JXMSJBM', 'title': '教学名师级别码', 'editable': 'False', 'type': 'text', 'create': 'True', },
            # {'table': 'dr_pksjxx', 'field': 'WYKCTJM', 'title': '外语课程调节码', 'editable': 'False', 'type': 'text', 'create': 'True', },

            {'table': 'dr_pksjxx', 'field': 'KCJBM', 'title': '课程级别码', 'editable': 'True', 'type': 'inline','create': 'True', 'value': 'st_kcjbm:DM AS KCJBM,MC', 'where': ''},
            {'table': 'dr_pksjxx', 'field': 'JXMSJBM', 'title': '教学名师级别码', 'editable': 'T', 'type': 'inline','create': 'True', 'value': 'st_jxmsjbm:DM AS JXMSJBM,MC', 'where': ''},
            {'table': 'dr_pksjxx', 'field': 'WYKCTJM', 'title': '外语课程调节码', 'editable': 'T', 'type': 'inline','create': 'True', 'value': 'st_wykctjm:DM AS WYKCTJM,MC', 'where': ''},

            {'table': 'dr_pksjxx', 'field': 'ZLXS', 'title': '质量系数', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_pksjxx', 'field': 'KKXQM', 'title': '开课学期码', 'editable': 'False', 'type': 'date', 'create': 'True', },
            {'table': 'dr_pksjxx', 'field': 'KKXND', 'title': '开课学年度', 'editable': 'False', 'type': 'year', 'create': 'True', },
            {'table': 'dr_pksjxx', 'field': 'HBS', 'title': '合班数', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_pksjxx', 'field': 'SKBJH', 'title': '上课班级号', 'editable': 'T', 'type': 'text', 'create': 'True', },

            {'table': 'dr_pksjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'F', 'type': 'text', 'create': 'false', },
            {'table': 'dr_pksjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'F', 'type': 'table', 'create': 'T', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},

            {'table': 'dr_pksjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_pksjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['JZGH']


class VIEW_BKSZKJXZXS(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_bkszkjxzxs'
    __tablename__CH__ = '本科生理论课助课学时数'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JZGH = Column('JZGH', String(16), default='')  # 教师工号
    JSGH = Column('JSGH', String(16), default='')  # 教师工号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KCH = Column('KCH', String(16), unique=True, default='')  # 课程号
    KKXND = Column('KKXND', String(16), default='')  # 开课学年度
    SKBJH = Column('SKBJH', String(16), default='')  # 上课班级号
    KKXQM = Column('KKXQM', DateTime, default=now())  # 开课学期码
    ZKJHXS = Column('ZKJHXS', Float(16), default='')  # 助课计划学时
    JHXSS = Column('JHXSS', Float(16), default='')  # 计划学时数
    KCJBM = Column('KCJBM', String(16), default='')  # 课程级别码
    JXMSJBM = Column('JXMSJBM', String(16), default='')  # 教学名师级别码
    WYKCTJM = Column('WYKCTJM', String(16), default='')  # 外语课程调节码
    ZLXS = Column('ZLXS', String(16), default='')  # 质量系数
    HBS = Column('HBS', Float(16), default='')  # 合班数
    DWH = Column('DWH', String(16), default='')  # 单位号
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_bkszkjxzxs AS
            SELECT 
                pk.id AS id,            
                pk.JSGH AS JSGH, 
                pk.JSGH AS JZGH, 
                pk.JSXM AS JSXM,            
                pk.KKXND AS KKXND,            
                pk.KKXQM AS KKXQM,            
                kc.LLXS AS JHXSS,  
                pk.ZKJHXS AS ZKJHXS,     
                pk.ZLXS AS ZLXS,            
                pk.HBS AS HBS,      
                pk.SKBJH AS SKBJH,         
                pk.WYKCTJM AS WYKCTJM,            
                pk.JXMSJBM AS JXMSJBM,     
                pk.KCJBM AS KCJBM, 
                kc.KCH AS KCH,           
                pk.DWH AS DWH,        
                pk.DWMC AS DWMC,
                xn.XQQSSJ AS stamp,            
                pk.note AS note            
            FROM dr_pkzksjxx pk
            LEFT JOIN dr_kcsjxx kc ON kc.KCH=pk.KCH
            LEFT JOIN dr_xnxqxx xn ON xn.XQQSSJ=pk.KKXQM
            LEFT JOIN dr_zzjgjbsjxx zz ON zz.DWH=pk.DWH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_pkzksjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_pkzksjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_pkzksjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note','DWH','DWMC','KCJBM','JXMSJBM','WYKCTJM','ZLXS','JHXSS']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_pkzksjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_pkzksjxx', 'field': 'JSGH', 'title': '教师工号', 'editable': 'False', 'type': 'text','create': 'False', },
            {'table': 'dr_pkzksjxx', 'field': 'JSXM', 'title': '教师姓名', 'editable': 'False', 'type': 'table','value': "dr_jzgjcsjxx:JZGH AS JSGH,XM AS JSXM", 'where': "DWH IN %(departments)s AND JZGH!='admin'",'create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'KCH', 'title': '课程号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'JHXSS', 'title': '计划学时数', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_pkzksjxx', 'field': 'ZKJHXS', 'title': '助课计划学时', 'editable': 'False', 'type': 'text','create': 'True', },

            # {'table': 'dr_bks_jpkc', 'field': 'KCJBM', 'title': '课程级别码', 'editable': 'True', 'type': 'text', 'create': 'True', },
            # {'table': 'dr_pksjxx', 'field': 'JXMSJBM', 'title': '教学名师级别码', 'editable': 'False', 'type': 'text', 'create': 'True', },
            # {'table': 'dr_pksjxx', 'field': 'WYKCTJM', 'title': '外语课程调节码', 'editable': 'False', 'type': 'text', 'create': 'True', },

            {'table': 'dr_pkzksjxx', 'field': 'KCJBM', 'title': '课程级别码', 'editable': 'F', 'type': 'inline','create': 'F', 'value': 'st_kcjbm:DM AS KCJBM,MC', 'where': ''},
            {'table': 'dr_pkzksjxx', 'field': 'JXMSJBM', 'title': '教学名师级别码', 'editable': 'F', 'type': 'inline','create': 'F', 'value': 'st_jxmsjbm:DM AS JXMSJBM,MC', 'where': ''},
            {'table': 'dr_pkzksjxx', 'field': 'WYKCTJM', 'title': '外语课程调节码', 'editable': 'F', 'type': 'inline','create': 'F', 'value': 'st_wykctjm:DM AS WYKCTJM,MC', 'where': ''},

            {'table': 'dr_pkzksjxx', 'field': 'ZLXS', 'title': '质量系数', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_pkzksjxx', 'field': 'KKXQM', 'title': '开课学期码', 'editable': 'False', 'type': 'date', 'create': 'True', },
            {'table': 'dr_pkzksjxx', 'field': 'KKXND', 'title': '开课学年度', 'editable': 'False', 'type': 'year', 'create': 'True', },
            {'table': 'dr_pkzksjxx', 'field': 'HBS', 'title': '合班数', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_pkzksjxx', 'field': 'SKBJH', 'title': '上课班级号', 'editable': 'T', 'type': 'text', 'create': 'True', },

            {'table': 'dr_pkzksjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'F', 'type': 'text', 'create': 'false', },
            {'table': 'dr_pkzksjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'F', 'type': 'table', 'create': 'T', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},

            {'table': 'dr_pkzksjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_pkzksjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['JZGH']


class VIEW_SXXSS(Base):  # 实习学时数
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_sxxss'  # 实习学时数
    __tablename__CH__ = '实习学时数'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JSGH = Column('JSGH', String(16), default='')  # 教师工号
    JZGH = Column('JZGH', String(16), default='')  # 教师工号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KCH = Column('KCH', String(16), unique=True, default='')  # 课程号
    KKXQM = Column('KKXQM', DateTime, default=now())  # 学期
    KKXND = Column('KKXND', String(16), default='')  # 学年
    HBS = Column('HBS', Float(16), default='')  # 合班数
    SXZS = Column('SXZS', Float(16), default='')  # 实习周数
    ZLXS = Column('ZLXS', String(16), default='')  # 质量系数
    DWH = Column('DWH', String(16), default='')  # 单位号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_sxxss AS
            SELECT 
                pk.id AS id,            
                pk.JSGH AS JSGH, 
                pk.JSGH AS JZGH,      
                pk.JSXM AS JSXM,          
                pk.KKXND AS KKXND,            
                pk.KKXQM AS KKXQM,                    
                pk.HBS AS HBS,            
                pk.SXZS AS SXZS,      
                pk.ZLXS AS ZLXS,            
                kc.KCH AS KCH,         
                dr_jzg.DWH AS DWH,            
                xn.XQQSSJ AS stamp,            
                pk.note AS note            
            FROM dr_sspksjxx pk
            LEFT JOIN dr_kcsjxx kc ON kc.KCH=pk.KCH
            LEFT JOIN dr_xnxqxx xn ON xn.XQQSSJ=pk.KKXQM
            LEFT JOIN dr_jzgjcsjxx dr_jzg ON dr_jzg.JZGH = pk.JSGH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_sspksjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_sspksjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_sspksjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note','DWH']

    @staticmethod
    def get_title_columns() -> List[str]:
        # NOTE: enum data: 'type': 'enum', 'value': ['未启用', '已启用'],
        # NOTE: static data from db: 'type': 'static', 'value': 'jx_usertype:id:usertype_name', 'where': ''
        # NOTE: SQL data from db: 'type': 'table', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'
        return [
            {'table': 'dr_sspksjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_sspksjxx', 'field': 'JSGH', 'title': '教师工号', 'editable': 'False', 'type': 'text','create': 'False', },
            {'table': 'dr_sspksjxx', 'field': 'JSXM', 'title': '教师姓名', 'editable': 'False', 'type': 'table','value': "dr_jzgjcsjxx:JZGH AS JSGH,XM AS JSXM", 'where': "DWH IN %(departments)s AND JZGH!='admin'",'create': 'True', },{'table': 'dr_kcsjxx', 'field': 'KCH', 'title': '课程号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_sspksjxx', 'field': 'KKXQM', 'title': '学期', 'editable': 'False', 'type': 'date', 'create': 'True', },
            {'table': 'dr_sspksjxx', 'field': 'KKXND', 'title': '学年', 'editable': 'False', 'type': 'year', 'create': 'True', },
            {'table': 'dr_sspksjxx', 'field': 'HBS', 'title': '合班数', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_sspksjxx', 'field': 'SXZS', 'title': '实习周数', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_sspksjxx', 'field': 'ZLXS', 'title': '质量系数', 'editable': 'False', 'type': 'text','create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'KCH', 'title': '课程号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text','create': 'false', },
            {'table': 'dr_sspksjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_sspksjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List:
        return ['JZGH']


class VIEW_KCSJXSS(Base):  # 课程设计学时数
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_kcsjxss'  # 课程设计学时数
    __tablename__CH__ = '课程设计学时数'
    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JSGH = Column('JSGH', String(16), default='')  # 教师工号
    JZGH = Column('JZGH', String(16), default='')  # 教师工号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KCH = Column('KCH', String(16), unique=True, default='')  # 课程号
    KKXQM = Column('KKXQM', DateTime, default=now())  # 学期
    KKXND = Column('KKXND', String(16), default='')  # 学年
    HBS = Column('HBS', Float(16), default='')  # 合班数
    SXZS = Column('SXZS', Float(16), default='')  # 课程设计周数
    ZLXS = Column('ZLXS', String(16), default='')  # 质量系数
    DWH = Column('DWH', String(16), default='')  # 单位号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_kcsjxss AS
            SELECT 
                pk.id AS id,            
                pk.JSGH AS JSGH, 
                pk.JSGH AS JZGH,      
                pk.JSXM AS JSXM,          
                pk.KKXND AS KKXND,            
                pk.KKXQM AS KKXQM,                        
                pk.HBS AS HBS,               
                pk.ZLXS AS ZLXS,            
                kc.KCH AS KCH,         
                dr_jzg.DWH AS DWH,   
                pk.SXZS AS SXZS,               
                xn.XQQSSJ AS stamp,            
                pk.note AS note            
            FROM dr_kcsjsjxx pk
            LEFT JOIN dr_kcsjxx kc ON kc.KCH=pk.KCH
            LEFT JOIN dr_xnxqxx xn ON xn.XQQSSJ=pk.KKXQM
            LEFT JOIN dr_jzgjcsjxx dr_jzg ON dr_jzg.JZGH = pk.JSGH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_kcsjsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_kcsjsjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_kcsjsjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note','DWH']

    @staticmethod
    def get_title_columns() -> List[str]:
        # NOTE: enum data: 'type': 'enum', 'value': ['未启用', '已启用'],
        # NOTE: static data from db: 'type': 'static', 'value': 'jx_usertype:id:usertype_name', 'where': ''
        # NOTE: SQL data from db: 'type': 'table', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'
        return [
            {'table': 'dr_kcsjsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_kcsjsjxx', 'field': 'JSGH', 'title': '教师工号', 'editable': 'False', 'type': 'text','create': 'False', },
            {'table': 'dr_kcsjsjxx', 'field': 'JSXM', 'title': '教师姓名', 'editable': 'False', 'type': 'table','value': "dr_jzgjcsjxx:JZGH AS JSGH,XM AS JSXM", 'where': "DWH IN %(departments)s AND JZGH!='admin'",'create': 'True', },
            {'table': 'dr_kcsjsjxx', 'field': 'KKXQM', 'title': '学期', 'editable': 'False', 'type': 'date', 'create': 'True', },
            {'table': 'dr_kcsjsjxx', 'field': 'KKXND', 'title': '学年', 'editable': 'False', 'type': 'year', 'create': 'True', },
            {'table': 'dr_kcsjsjxx', 'field': 'HBS', 'title': '合班数', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kcsjsjxx', 'field': 'ZLXS', 'title': '质量系数', 'editable': 'False', 'type': 'text','create': 'True', },
            {'table': 'dr_kcsjsjxx', 'field': 'SXZS', 'title': '课程设计周数', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'KCH', 'title': '课程号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text','create': 'false', },
            {'table': 'dr_kcsjsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_kcsjsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List:
        return ['JZGH']


class VIEW_ZDSYXSS(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_zdsyxss'
    __tablename__CH__ = '指导实验学时数'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JSGH = Column('JSGH', String(16), default='')  # 教师工号
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KCH = Column('KCH', String(16), unique=True, default='')  # 课程号
    KKXND = Column('KKXND', String(16), default='')  # 开课学年度
    KKXQM = Column('KKXQM', DateTime, default=now())  # 开课学期码
    SYXS = Column('SYXS', Float(16), default='')  # 实验学时
    KCJBM = Column('KCJBM', String(16), default='')  # 课程级别码
    SYZS = Column('SYZS', Float(16), default='')  # 实验组数
    DWH = Column('DWH', String(16), default='')  # 课程级别码
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_zdsyxss AS
            SELECT 
                pk.id AS id,            
                pk.JSGH AS JSGH,            
                pk.JSGH AS JZGH, 
                pk.JSXM AS JSXM,             
                pk.KKXND AS KKXND,            
                pk.KKXQM AS KKXQM,            
                kc.SYXS AS SYXS,    
                pk.KCJBM AS KCJBM, 
                pk.SYZS AS SYZS,                   
                kc.KCH AS KCH,           
                dr_jzg.DWH AS DWH,        
                xn.XQQSSJ AS stamp,            
                pk.note AS note            
            FROM dr_sypksjxx pk
            LEFT JOIN dr_kcsjxx kc ON kc.KCH=pk.KCH
            LEFT JOIN dr_xnxqxx xn ON xn.XQQSSJ=pk.KKXQM
            LEFT JOIN dr_jzgjcsjxx dr_jzg ON dr_jzg.JZGH=pk.JSGH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_sypksjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_sypksjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_sypksjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note','DWH']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_sypksjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_kcsjsjxx', 'field': 'JSGH', 'title': '教师工号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_kcsjsjxx', 'field': 'JSXM', 'title': '教师姓名', 'editable': 'False', 'type': 'table', 'value': "dr_jzgjcsjxx:JZGH AS JSGH,XM AS JSXM", 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'KCH', 'title': '课程号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kcsjxx', 'field': 'SYXS', 'title': '实验学时', 'editable': 'True', 'type': 'float', 'create': 'F', },
            {'table': 'dr_kcsjxx', 'field': 'SYZS', 'title': '实验组数', 'editable': 'True', 'type': 'float','create': 'True', },
            {'table': 'dr_sypksjxx', 'field': 'KKXQM', 'title': '学期', 'editable': 'False', 'type': 'date', 'create': 'True', },
            {'table': 'dr_sypksjxx', 'field': 'KKXND', 'title': '学年', 'editable': 'False', 'type': 'year', 'create': 'True', },
            {'table': 'dr_sypksjxx', 'field': 'KCJBM', 'title': '课程级别码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_kcjbm:DM AS KCJBM,MC', 'where': ''},
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'false', },
            {'table': 'dr_sypksjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_sypksjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['JZGH']


class VIEW_KSAPXX(Base):
    """
KSRQ     考试日期 C  教务处、研究生院
KSSC     考试时长 N  教务处、研究生院
KSFSLXM  考试方式类型码 C(1) JX_KSFS 考试方式代码 教务处、研究生院
KCH      课程号 C  教务处、研究生院
JKRGH    监考人工号 C(8)  教务处、研究生院
KSJSH    考试教室号 C  教务处、研究生院
JKRXM    监考人姓名 C  教务处、研究生院
KSRS     考试人数 N  教务处、研究生院
    """

    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_ksapxx'
    __tablename__CH__ = '考试安排信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注
    JZGH = Column('JZGH', String(16), default='')  # 教师工号
    KSRQ = Column('KSRQ', DateTime, default=now())  # 考试日期
    KSSC = Column('KSSC', String(16), default='')  # 考试时长
    KSFSLXM = Column('KSFSLXM', String(16), default='')  # 考试方式类型码
    KCH = Column('KCH', String(16), default='')  # 课程号
    KSJSH = Column('KSJSH', String(16), default='')  # 考试教室号
    JKRXM = Column('JKRXM', String(16), default='')  # 监考人姓名
    KSRS = Column('KSRS', String(16), default='')  # 考试人数
    SSXY = Column('SSXY', String(16), default='')  # 本次考试所属学院
    JSSSXY = Column('JSSSXY', String(16), default='')  # 教师所属学院

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_ksapxx AS
            SELECT 
                dr.id AS id,         
                dr.JKRGH AS JZGH,
                dr.KSRQ AS stamp,            
                dr.note AS note,        
                dr.KSRQ AS KSRQ,            
                dr.KSSC AS KSSC,            
                dr.KSFSLXM AS KSFSLXM,            
                dr.KCH AS KCH,                   
                dr.KSJSH AS KSJSH,            
                dr.JKRXM AS JKRXM,            
                dr.KSRS AS KSRS,  
                dr.SSXY AS SSXY,
                jkr.DWH AS JSSSXY                                 
            FROM dr_ksapxx dr
            LEFT JOIN dr_jzgjcsjxx jkr ON jkr.JZGH = dr.JKRGH
            LEFT JOIN dr_pksjxx pk ON pk.KCH=dr.KCH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_ksapxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_ksapxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_ksapxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note','JSSSXY','KSJSH','KSFSLXM']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_ksapxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_ksapxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_ksapxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },

            {'table': 'dr_ksapxx', 'field': 'KSRQ', 'title': '考试日期', 'editable': 'False', 'type': 'date', 'create': 'True', },
            {'table': 'dr_ksapxx', 'field': 'KSSC', 'title': '考试时长', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_ksapxx', 'field': 'KSFSLXM', 'title': '考试方式类型码', 'editable': 'True', 'type': 'text', 'create': 'False', },
            {'table': 'dr_ksapxx', 'field': 'KCH', 'title': '课程号', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_ksapxx', 'field': 'JZGH', 'title': '教职工号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_ksapxx', 'field': 'KSJSH', 'title': '考试教室号', 'editable': 'True', 'type': 'text', 'create': 'False', },
            {'table': 'dr_ksapxx', 'field': 'JKRXM', 'title': '监考人姓名', 'editable': 'True', 'type': 'table', 'create': 'True', 'value': 'dr_jzgjcsjxx:JZGH AS JZGH,XM AS JKRXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", },
            {'table': 'dr_ksapxx', 'field': 'KSRS', 'title': '考试人数', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_ksapxx', 'field': 'SSXY', 'title': '本次考试所属学院', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jzgjcsjxx', 'field': 'JSSSXY', 'title': '教师所属学院', 'editable': 'False', 'type': 'text','create': 'False', },
        ]
    @staticmethod
    def get_search_columns() -> List[str]:
        return ['KCH', 'SSXY', 'JZGH', 'JKRXM']


class VIEW_JKXSS(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_jkxss'
    __tablename__CH__ = '监考学时数'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JZGH = Column('JZGH', String(16), default='')  # 教师工号
    KCH = Column('KCH', String(16), default='')  # 课程号
    KSRQ = Column('KSRQ', DateTime, default=now())  # 考试日期
    KSSC = Column('KSSC', Float(16), default='')  # 考试时长
    KSFSLXM = Column('KSFSLXM', String(16), default='')  # 考试方式类型码
    JKRGH = Column('JKRGH', String(16), default='')  # 监考人工号
    KSJSH = Column('KSJSH', String(16), default='')  # 考试教室号
    JKRXM = Column('JKRXM', String(16), default='')  # 监考人姓名
    KSRS = Column('KSRS', String(16), default='')  # 考试人数
    SSXY = Column('SSXY', String(16), default='')  # 本次考试所属学院
    JSSSXY = Column('JSSSXY', String(16), default='')  # 教师所属学院
    DWH = Column('DWH', String(16), default='')  # 单位号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_jkxss AS
            SELECT 
                dr.id AS id,            
                dr.KSRQ AS KSRQ,            
                dr.KSSC AS KSSC,            
                dr.KSFSLXM AS KSFSLXM,            
                dr.KCH AS KCH,     
                dr.JKRGH AS JZGH,        
                dr.JKRGH AS JKRGH,            
                dr.KSJSH AS KSJSH,            
                dr.JKRXM AS JKRXM,            
                dr.KSRS AS KSRS,  
                dr.SSXY AS SSXY,
                jkr.DWH AS JSSSXY,            
                jkr.DWH AS DWH,      
                dr.KSRQ AS stamp,            
                dr.note AS note            
            FROM dr_ksapxx dr
            LEFT JOIN dr_jzgjcsjxx jkr ON jkr.JZGH = dr.JKRGH
            LEFT JOIN dr_pksjxx pk ON pk.KCH=dr.KCH
            WHERE 1=1
        """
            # LEFT JOIN dr_zzjgjbsjxx zzjg ON zzjg.DWH=jkr.DWH
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_ksapxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_ksapxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_ksapxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note', 'DWH', 'JSSSXY', 'KSJSH', 'KSFSLXM']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_ksapxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_ksapxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_ksapxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
            {'table': 'dr_ksapxx', 'field': 'KSRQ', 'title': '考试日期', 'editable': 'True', 'type': 'date', 'create': 'True', },
            {'table': 'dr_ksapxx', 'field': 'KSSC', 'title': '考试时长', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_ksapxx', 'field': 'KSFSLXM', 'title': '考试方式类型码', 'editable': 'True', 'type': 'text', 'create': 'False', },
            {'table': 'dr_ksapxx', 'field': 'KCH', 'title': '课程号', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_ksapxx', 'field': 'JKRGH', 'title': '监考人工号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_ksapxx', 'field': 'KSJSH', 'title': '考试教室号', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_ksapxx', 'field': 'JKRXM', 'title': '监考人姓名', 'editable': 'True', 'type': 'table', 'create': 'True', 'value': 'dr_jzgjcsjxx:JZGH AS JKRGH,XM AS JKRXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", },
            {'table': 'dr_ksapxx', 'field': 'KSRS', 'title': '考试人数', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_ksapxx', 'field': 'SSXY', 'title': '本次考试所属学院', 'editable': 'False', 'type': 'text','create': 'True', },
            {'table': 'dr_jzgjcsjxx', 'field': 'JSSSXY', 'title': '教师所属学院', 'editable': 'False', 'type': 'text','create': 'False', },
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['KCH', 'SSXY', 'JKRGH', 'JKRXM']


class VIEW_ZDBYLWXSS(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_zdbylwxss'
    __tablename__CH__ = '指导毕业论文学时数'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    DWH = Column('DWH', String(16), default='')  # 单位号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注
    JZGH = Column('JZGH', String(16), default='')  # 教师工号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    ZDZS = Column('ZDZS', Float(16), default='')  # 指导周数
    ZDPTXSS = Column('ZDPTXSS', Float(16), default='')  # 指导普通学生数
    ZDSYXSS = Column('ZDSYXSS', Float(16), default='')  # 指导双语学生数
    JXMSJBM = Column('JXMSJBM', String(16), default='')  # 教学名师级别码
    XQ = Column('XQ', DateTime, default=now())  # 指导学期

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_zdbylwxss AS
            SELECT 
                dr.id AS id,
                jkr.DWH AS DWH,     
                dr.XQ AS stamp,            
                dr.note AS note,   
                dr.XQ AS XQ,            
                dr.JZGH AS JZGH,            
                dr.JSXM AS JSXM,            
                dr.ZDZS AS ZDZS,             
                dr.ZDPTXSS AS ZDPTXSS,            
                dr.ZDSYXSS AS ZDSYXSS,            
                dr.JXMSJBM AS JXMSJBM                              
            FROM dr_zdbylwsjxx dr
            LEFT JOIN dr_jzgjcsjxx jkr ON jkr.JZGH = dr.JZGH
            WHERE 1=1
        """
            # LEFT JOIN dr_xnxqxx PK ON PK.XQQSSJ=dr.XQ
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_zdbylwsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_zdbylwsjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_zdbylwsjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note','DWH']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_zdbylwsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_zdbylwsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_zdbylwsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_zdbylwsjxx', 'field': 'XQ', 'title': '指导学期', 'editable': 'True', 'type': 'date', 'create': 'True', },
            {'table': 'dr_zdbylwsjxx', 'field': 'JZGH', 'title': '教师工号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_zdbylwsjxx', 'field': 'JSXM', 'title': '教师姓名', 'editable': 'True', 'type': 'table', 'create': 'True', 'value': 'dr_jzgjcsjxx:JZGH AS JZGH,XM AS JSXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", },
            {'table': 'dr_zdbylwsjxx', 'field': 'ZDZS', 'title': '指导周数', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_zdbylwsjxx', 'field': 'ZDPTXSS', 'title': '指导普通学生数', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_zdbylwsjxx', 'field': 'ZDSYXSS', 'title': '指导双语学生数', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_zdbylwsjxx', 'field': 'JXMSJBM', 'title': '教学名师级别码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_jxmsjbm:DM AS JXMSJBM,MC', 'where': ''},
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['JZGH','JSXM']


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


# FROM Fanming 2nd time by why@20210528
class VIEW_XMJFXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_xmjfxx'
    __tablename__CH__ = '项目经费信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    XMBH = Column('XMBH', String(64), unique=True, default='')  # 项目编号
    XMMC = Column('XMMC', String(64), unique=True, default='')  # 项目名称
    FZRH = Column('FZRH', String(16), default='')  # 负责人号
    XMJFLYM = Column('XMJFLYM', String(16), default='')  # 项目经费来源码
    BRRQ = Column('BRRQ', DateTime, default=now())  # 拨入日期
    ZCRQ = Column('ZCRQ', DateTime, default=now())  # 支出日期
    XMSJJK = Column('XMSJJK', Float, default=0.0)  # 项目实际进款
    KYXMLX = Column('KYXMLX', String(16), default='')  # 科研项目类型
    KYJFLX = Column('KYJFLX', String(16), default='')  # 科研经费类型
    XMPZBH = Column('XMPZBH', String(64), default='')  # 项目凭证编号
    JBRXM = Column('JBRXM', String(32), default=now())  # 经办人姓名
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
                dr.XMBH AS XMBH,            
                dr.XMMC AS XMMC,            
                dr.FZRH AS FZRH,            
                dr.XMJFLYM AS XMJFLYM,            
                dr.BRRQ AS BRRQ,            
                dr.ZCRQ AS ZCRQ,            
                dr.XMSJJK AS XMSJJK,            
                dr.KYXMLX AS KYXMLX,            
                dr.KYJFLX AS KYJFLX,            
                dr.XMPZBH AS XMPZBH,            
                dr.JBRXM AS JBRXM,            
                dr.FZRH AS JZGH,
                jz.DWH AS DWH,
                jz.XM AS XM,
                dw.DWMC AS DWMC,
                dr.BRRQ AS stamp,
                dr.note AS note
            FROM dr_xmjfxx dr
            LEFT JOIN dr_jzgjcsjxx jz ON jz.JZGH=dr.FZRH
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
            {'table': 'dr_xmjfxx', 'field': 'DWH', 'title': '单位号', 'editable': 'F', 'type': 'text', 'create': 'false', },
            {'table': 'dr_xmjfxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_xmjfxx', 'field': 'FZRH', 'title': '负责人号', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_xmjfxx', 'field': 'XM', 'title': '姓名', 'editable': 'T', 'type': 'table', 'value': 'dr_jzgjcsjxx:JZGH AS FZRH,XM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'T', },
            {'table': 'dr_xmjfxx', 'field': 'XMBH', 'title': '项目编号', 'editable': 'False', 'type': 'text','create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'XMMC', 'title': '项目名称', 'editable': 'False', 'type': 'text','create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'XMJFLYM', 'title': '项目经费来源码', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'BRRQ', 'title': '拨入日期', 'editable': 'False', 'type': 'date','create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'ZCRQ', 'title': '支出日期', 'editable': 'True', 'type': 'date','create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'XMSJJK', 'title': '项目实际进款', 'editable': 'T', 'type': 'text','create': 'T', },
            {'table': 'dr_xmjfxx', 'field': 'KYXMLX', 'title': '科研项目类型', 'editable': 'T', 'type': 'inline', 'create': 'T', 'value': 'st_kyxmlx:DM AS KYXMLX,MC', 'where': ''},
            {'table': 'dr_xmjfxx', 'field': 'KYJFLX', 'title': '科研经费类型', 'editable': 'T', 'type': 'inline', 'create': 'T', 'value': 'st_kyjflx:DM AS KYJFLX,MC', 'where': ''},
            {'table': 'dr_xmjfxx', 'field': 'XMPZBH', 'title': '项目凭证编号', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'JBRXM', 'title': '经办人姓名', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_xmjfxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List:
        return ['JZGH', 'DWH', 'DWMC', 'XMBH', 'JBRXM']


# FROM Fanming 2nd time by why@20210528
class VIEW_XMRYXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_xmryxx'
    __tablename__CH__ = '项目人员信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    XMBH = Column('XMBH', String(16), default='')  # 项目编号
    XMMC = Column('XMMC', String(16), default='')  # 项目名称
    RYH = Column('RYH', String(16), default='')  # 人员号
    GXL = Column('GXL', Float, default=0.0)  # 贡献率
    XMSJJK = Column('XMSJJK', Float, default=0.0)  # 项目实际进款
    KYXMLX = Column('KYXMLX', String(16), default='')  # 科研项目类型
    KYJFLX = Column('KYJFLX', String(16), default='')  # 科研经费类型
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    XM = Column('XM', String(16), default='')  # 姓名
    DWH = Column('DWH', String(16), default='')  # 单位号
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    MNGZYS = Column('MNGZYS', Float, default=0.0)  # 每年工作月数
    JSM = Column('JSM', String(16), default='')  # 角色码
    RYLX = Column('RYLX', String(16), default='')  # 人员类型
    SMSX = Column('SMSX', String(16), default='')  # 署名顺序
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
                dr.GXL AS GXL, 
                xm.XMSJJK AS XMSJJK, 
                xm.KYXMLX AS KYXMLX, 
                xm.KYJFLX AS KYJFLX, 
                jz.XM AS XM,
                jz.DWH AS DWH,
                jz.DWMC AS DWMC, 
                dr.XMBH AS XMBH,
                dr.XMMC AS XMMC,
                dr.MNGZYS AS MNGZYS,
                dr.JSM AS JSM,
                dr.RYLX AS RYLX,
                dr.SMSX AS SMSX,
                dr.XKMLKJM AS XKMLKJM,
                dr.stamp AS stamp,
                dr.note AS note
            FROM dr_xmryxx dr
            LEFT JOIN view_jzgjcsjxx jz ON jz.JZGH=dr.RYH
            LEFT JOIN dr_xmjfxx xm ON xm.XMBH=dr.XMBH
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
            {'table': 'dr_xmryxx', 'field': 'DWH', 'title': '单位号', 'editable': 'F', 'type': 'text','create': 'false', },
            {'table': 'dr_xmryxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_xmryxx', 'field': 'RYH', 'title': '人员号', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_xmryxx', 'field': 'XM', 'title': '姓名', 'editable': 'T', 'type': 'table', 'value': 'dr_jzgjcsjxx:JZGH AS RYH,XM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'T', },
            {'table': 'dr_xmryxx', 'field': 'GXL', 'title': '贡献率', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_xmjfxx', 'field': 'XMBH', 'title': '项目编号', 'editable': 'F', 'type': 'text','create': 'false', },
            {'table': 'dr_xmjfxx', 'field': 'XMMC', 'title': '项目名称', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_xmjfxx:XMBH,XMMC', 'where': 'XMBH IN %(departments)s'},
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


# zouyang
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
    RYH = Column('RYH', String(16), default='')  # 人员号
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
    JZGH = Column('JZGH', String(16), default='')  # 教职工号

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
        return ['dr_kjcgryxx_lw', 'dr_kjlwslqk', 'dr_kjqklwjbsjxx', 'dr_kjlwfbxx', ]

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_kjcgryxx_lw', 'dr_kjlwslqk', 'dr_kjqklwjbsjxx', 'dr_kjlwfbxx', ]

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


class VIEW_JCJBSJXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_jcjbsjxx'
    __tablename__CH__ = '教材基本数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    CBH = Column('CBH', String(16), default='')  # 出版号
    JCMC = Column('JCMC', String(16), default='')  # 教材名称
    BC = Column('BC', String(16), default='')  # 版次
    DWH = Column('DWH', String(16), default='')  # 单位号
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    CBS = Column('CBS', String(16), default='')  # 出版社
    CBRQ = Column('CBRQ', DateTime, default=now())  # 出版日期
    JCBH = Column('JCBH', String(16), default='')  # 教材编号
    JCLB = Column('JCLB', String(16), default='')  # 教材类别
    JCZS = Column('JCZS', Float, default=0.0)   # 教材字数
    DYZBH = Column('DYZBH', String(16), default='')  # 第一主编号
    DYZBXM = Column('DYZBXM', String(16), default='')  # 第一主编姓名
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_jcjbsjxx AS
            SELECT
               dr_jcxx.id AS id,
               dr_jcxx.CBH AS CBH,
               dr_jcxx.JCMC AS JCMC,
               dr_jcxx.BC AS BC,
               dr_jcxx.DWH AS DWH,
               dr_jcxx.DWMC AS DWMC,
               dr_jcxx.CBS AS CBS,
               dr_jcxx.CBRQ AS CBRQ,
               dr_jcxx.JCBH AS JCBH,
               dr_jcxx.JCLB AS JCLB,
               dr_jcxx.JCZS AS JCZS,
               dr_jcxx.DYZBH AS DYZBH,
               dr_jcxx.DYZBH AS JZGH,
               dr_jcxx.DYZBXM AS DYZBXM,
               dr_jcxx.CBRQ AS stamp,
               dr_jcxx.note AS note
            FROM dr_jcjbsjxx dr_jcxx
            LEFT JOIN dc_jcjbsjxx dc_jcxx ON dc_jcxx.JCBH = dr_jcxx.JCBH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_jcjbsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_jcjbsjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_jcjbsjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_jcjbsjxx', 'field': 'id', 'title': 'ID', 'editable': 'T', 'type': 'text', 'create': 'F', },
            {'table': 'dr_jcjbsjxx', 'field': 'JCMC', 'title': '教材名称', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jcjbsjxx', 'field': 'JCBH', 'title': '教材编号', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jcjbsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'F', 'type': 'text', 'create': 'F', },
            {'table': 'dr_jcjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'F', 'type': 'table', 'create': 'T', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_jcjbsjxx', 'field': 'JCLB', 'title': '教材类别', 'editable': 'T', 'type': 'inline', 'create': 'True', 'value': 'st_jxjclx:DM AS JCLB,MC', 'where': ''},
            {'table': 'dr_jcjbsjxx', 'field': 'JCZS', 'title': '教材字数', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_jcjbsjxx', 'field': 'DYZBH', 'title': '第一主编号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_jcjbsjxx', 'field': 'DYZBXM', 'title': '第一主编姓名', 'editable': 'T', 'type': 'table', 'value': 'dr_jzgjcsjxx:JZGH AS DYZBH,XM AS DYZBXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'T', },
            {'table': 'dr_jcjbsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'T', 'type': 'date', 'create': 'F', },
            {'table': 'dr_jcjbsjxx', 'field': 'CBRQ', 'title': '出版日期', 'editable': 'T', 'type': 'date', 'create': 'T', },
            {'table': 'dr_jcjbsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> []:
        return ['JCMC', 'CBS', 'DYZBXM', ]


class VIEW_JCBZXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_jcbzxx'
    __tablename__CH__ = '教材编者信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    BZZH = Column('BZZH', String(16), default='')  # 编著者号
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    BZZXM = Column('BZZXM', String(16), default='')  # 编著者姓名
    JCZS = Column('JCZS', Float, default=0.0)  # 教材字数
    JCLB = Column('JCLB', String(16), default='')  # 教材类别
    GXL = Column('GXL', String(16), default='')  # 贡献率
    DWH = Column('DWH', String(16), default='')  # 单位号
    DYZBH = Column('DYZBH', String(16), default='')  # 第一主编号
    DYZBXM = Column('DYZBXM', String(16), default='')  # 第一主编姓名
    BZZDW = Column('BZZDW', String(16), default='')  # 编著者单位
    JCBH = Column('JCBH', String(16), default='')  # 教材编号
    JCMC = Column('JCMC', String(16), default='')  # 教材名称
    CBRQ = Column('CBRQ', DateTime, default=now())  # 出版日期
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_jcbzxx AS
            SELECT
               dr_bzxx.id AS id,
               dr_bzxx.BZZH AS BZZH,
               dr_bzxx.BZZH AS JZGH,
               dr_bzxx.BZZXM AS BZZXM,
               dr_bzxx.DWH AS DWH,
               dr_bzxx.BZZDW AS BZZDW,
               dr_bzxx.GXL AS GXL,
               dr_jcxx.JCZS AS JCZS,
               dr_jcxx.JCLB AS JCLB,
               dr_jcxx.DYZBH AS DYZBH,
               dr_jcxx.DYZBXM AS DYZBXM,
               dr_jcxx.JCBH AS JCBH,
               dr_jcxx.JCMC AS JCMC,
               dr_jcxx.CBRQ AS CBRQ,
               dr_jcxx.CBRQ AS stamp,
               dr_jcxx.note AS note
            FROM dr_bzxx dr_bzxx
            LEFT JOIN dr_jcjbsjxx dr_jcxx on dr_bzxx.JCBH = dr_jcxx.JCBH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_jcjbsjxx', 'dr_bzxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_bzxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_bzxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_bzxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_bzxx', 'field': 'JCBH', 'title': '教材编号', 'editable': 'F', 'type': 'text', 'create': 'F', },
            {'table': 'dr_bzxx', 'field': 'JCMC', 'title': '教材名称', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_jcjbsjxx:JCBH,JCMC', 'where': '', },
            {'table': 'dr_bzxx', 'field': 'BZZXM', 'title': '编著者姓名', 'editable': 'True', 'type': 'table', 'value': 'dr_jzgjcsjxx:JZGH AS BZZH,XM AS BZZXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'T', },
            {'table': 'dr_bzxx', 'field': 'BZZH', 'title': '编著者号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_jcjbsjxx', 'field': 'JCLB', 'title': '教材类别', 'editable': 'False', 'type': 'table', 'create': 'F', 'value': 'dr_jcjbsjxx:JCLB', 'where': '', },
            {'table': 'dr_jcjbsjxx', 'field': 'DYZBH', 'title': '第一主编号', 'editable': 'False', 'type': 'text', 'create': 'False',  'value': 'dr_jcjbsjxx:DYZBH', 'where': '',},
            {'table': 'dr_jcjbsjxx', 'field': 'JCZS', 'title': '教材字数', 'editable': 'False', 'type': 'text', 'create': 'F', 'value': 'dr_jcjbsjxx:JCZS', 'where': '',},
            {'table': 'dr_jcjbsjxx', 'field': 'CBRQ', 'title': '出版日期', 'editable': 'False', 'type': 'date', 'create': 'F', 'value': 'dr_jcjbsjxx:CBRQ', 'where': '', },
            {'table': 'dr_bzxx', 'field': 'GXL', 'title': '贡献率', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_bzxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_bzxx', 'field': 'BZZDW', 'title': '编著者单位', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_zzjgjbsjxx:DWH,DWMC AS BZZDW', 'where': 'DWH IN %(departments)s'},
        ]

    @staticmethod
    def get_search_columns() -> []:
        return ['BZZXM', 'DYZBXM', 'JCMC', ]


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
            SELECT
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
            FROM dr_kjcgryxx_jl dr_kjcg_jl
            LEFT JOIN dr_hjcgjbsjxx dr_hjcg ON dr_kjcg_jl.HJCGBH = dr_hjcg.HJCGBH
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
            {'table': 'dr_kjcgryxx_jl', 'field': 'HJCGBH', 'title': '获奖成果名称', 'editable': 'T', 'type': 'inline', 'create': 'T', 'value': 'dr_hjcgjbsjxx:HJCGBH,HJCGMC', 'where': '', },
            {'table': 'dr_kjcgryxx_jl', 'field': 'RYH', 'title': '人员号', 'editable': 'T', 'type': 'text', 'create': 'F', },
            {'table': 'dr_kjcgryxx_jl', 'field': 'XM', 'title': '姓名', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_jzgjcsjxx:JZGH AS RYH,XM', 'where': "DWH IN %(departments)s AND JZGH!='admin'"},
            {'table': 'dr_kjcgryxx_jl', 'field': 'PMZRS', 'title': '排名/总人数', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_jl', 'field': 'GXL', 'title': '贡献率', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'CGHJLBM', 'title': '成果获奖类别码', 'editable': 'False', 'type': 'inline', 'create': 'False', 'value': 'st_ky_cghjlb:DM AS CGHJLBM,MC', 'where': ''},
            {'table': 'dr_hjcgjbsjxx', 'field': 'JLDJM', 'title': '奖励等级码', 'editable': 'False', 'type': 'inline', 'create': 'False', 'value': 'st_jldj:JLDJM,JLDJMC', 'where': ''},
            {'table': 'dr_hjcgjbsjxx', 'field': 'HJJBM', 'title': '获奖级别码', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'KJJLB', 'title': '科技奖类别', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> []:
        return ['XM']


# yangchen
class VIEW_ZLCGJBSJXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_zlcgjbsjxx'
    __tablename__CH__ = '专利成果基本数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    ZLCGBH = Column('ZLCGBH', String(16), default='')  # 专利成果编号
    ZLCGMC = Column('ZLCGMC', String(128), default='')  # 专利成果名称
    DWH = Column('DWH', String(128), default='')  # 单位号
    SQBH = Column('SQBH', String(16), default='')  # 申请编号
    XKLYM = Column('XKLYM', String(16), default='')  # 学科领域
    ZLLXM = Column('ZLLXM', String(16), default='')  # 专利类型码
    PZRQ = Column('PZRQ', DateTime, default=now())  # 批准日期
    PZXSM = Column('PZXSM', String(16), default='')  # 批准形式码
    ZLZSBH = Column('ZLZSBH', String(16), default='')  # 专利证书编号
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
            SELECT
               dr_zl.id AS id,
               dr_zl.ZLCGBH AS ZLCGBH,
               dr_zl.ZLCGMC AS ZLCGMC,
               dr_zl.DWH AS DWH,
               dr_zl.SQBH AS SQBH,
               dr_zl.XKLYM AS XKLYM,
               dr_zl.ZLLXM AS ZLLXM,
               dr_zl.PZRQ AS PZRQ,
               dr_zl.PZXSM AS PZXSM,
               dr_zl.ZLZSBH AS ZLZSBH,
               dr_zl.FLZTM AS FLZTM,
               dr_zl.JNZLNFRQ AS JNZLNFRQ,
               dr_zl.JNJE AS JNJE,
               dr_zl.SSXMBH AS SSXMBH,
               dr_zl.GJDQM AS GJDQM,
               dr_zl.GJZLZFLH AS GJZLZFLH,
               dr_zl.PCTHZLGJDQM AS PCTHZLGJDQM,
               dr_zl.SQGGH AS SQGGH,
               dr_zl.SQGGRQ AS SQGGRQ,
               dr_zl.SQMC AS SQMC,
               dr_zl.ZLDLJG AS ZLDLJG,
               dr_zl.ZLDLR AS ZLDLR,
               dr_zl.ZLQR AS ZLQR,
               dr_zl.ZLZZRQ AS ZLZZRQ,
               dr_zl.XKMLKJM AS XKMLKJM,
               dr_zl.ZLSQRQ AS ZLSQRQ,
               dr_zl.ZZM AS ZZM,
               dr_zl.ZZBH AS ZZBH,
               dr_zl.PZRQ AS stamp,
               dr_zl.note AS note
            FROM dr_zlcgjbsjxx dr_zl
            LEFT JOIN dc_zlcgjbsjxx dc_zl ON dr_zl.ZLCGBH = dc_zl.ZLCGBH
            WHERE 1=1
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
        return [
            {'table': 'dr_zlcgjbsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLCGBH', 'title': '专利成果编号', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLCGMC', 'title': '专利成果名称', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'T', 'type': 'inline', 'create': 'T', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_zlcgjbsjxx', 'field': 'SQBH', 'title': '申请编号', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLLXM', 'title': '专利类型码', 'editable': 'T', 'type': 'inline', 'create': 'T', },  # need value
            {'table': 'dr_zlcgjbsjxx', 'field': 'PZRQ', 'title': '批准日期', 'editable': 'T', 'type': 'date', 'create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'PZXSM', 'title': '批准形式码', 'editable': 'T', 'type': 'inline', 'create': 'T', },  # need value
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLZSBH', 'title': '专利证书编号', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'FLZTM', 'title': '法律状态码', 'editable': 'T', 'type': 'inline', 'create': 'T', },  # need value
            {'table': 'dr_zlcgjbsjxx', 'field': 'SQGGH', 'title': '授权公告号', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'SQGGRQ', 'title': '授权公告日期', 'editable': 'T', 'type': 'data', 'create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'SQMC', 'title': '申请名称', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLDLJG', 'title': '专利代理机构', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLDLR', 'title': '专利代理人', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLQR', 'title': '专利权人', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'XKMLKJM', 'title': '学科门类(科技)码', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZLSQRQ', 'title': '专利申请日期', 'editable': 'T', 'type': 'data', 'create': 'T', },
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZZM', 'title': '作者名', 'editable': 'T', 'type': 'table', 'create': 'T', 'value': 'dr_jzgjcsjxx:JZGH AS ZZBH,XM AS ZZM', 'where': "DWH IN %(departments)s AND JZGH!='admin'"},
            {'table': 'dr_zlcgjbsjxx', 'field': 'ZZBH', 'title': '作者编号', 'editable': 'T', 'type': 'text', 'create': 'F', },
        ]

    @staticmethod
    def get_search_columns() -> []:
        return ['ZLCGMC']


class VIEW_KJZZXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_kjzzxx'
    __tablename__CH__ = '科技著作信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    ZZBH = Column('ZZBH', String(16), default='')  # 著作编号
    ZZMC = Column('ZZMC', String(16), default='')  # 著作名称
    DWH = Column('DWH', String(16), default='')  # 单位号
    CBRQ = Column('CBRQ', DateTime, default=now())  # 出版日期
    LZLBM = Column('LZLBM', String(16), default='')  # 论著类别码
    CBS = Column('CBS', String(16), default='')  # 出版社
    CBSJBM = Column('CBSJBM', String(16), default='')  # 出版社级别码
    CBH = Column('CBH', String(16), default='')  # 出版号
    ZZZS = Column('ZZZS', Integer, default=0)  # 著作字数
    ISBNH = Column('ISBNH', String(16), default='')  # ISBN号
    DYZZ = Column('DYZZ', String(16), default='')  # 第一作者
    DYZZBH = Column('DYZZBH', String(16), default='')  # 第一作者编号
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_kjzzxx AS
            SELECT
               dr_kjzz.id AS id,
               dr_kjzz.ZZBH AS ZZBH,
               dr_kjzz.ZZMC AS ZZMC,
               dr_kjzz.DWH AS DWH,
               dr_kjzz.CBRQ AS CBRQ,
               dr_kjzz.LZLBM AS LZLBM,
               dr_kjzz.CBS AS CBS,
               dr_kjzz.CBSJBM AS CBSJBM,
               dr_kjzz.CBH AS CBH,
               dr_kjzz.ZZZS AS ZZZS,
               dr_kjzz.ISBNH AS ISBNH,
               dr_kjzz.DYZZ AS DYZZ,
               dr_kjzz.DYZZBH AS DYZZBH,
               dr_kjzz.DYZZBH AS JZGH,              
               dr_kjzz.DWMC AS DWMC,
               dr_kjzz.CBRQ AS stamp,
               dr_kjzz.note AS note
            FROM dr_kjzzxx dr_kjzz
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_kjzzxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_kjzzxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_kjzzxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_kjzzxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_kjzzxx', 'field': 'ZZBH', 'title': '著作编号', 'editable': 'false', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjzzxx', 'field': 'ZZMC', 'title': '著作名称', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjzzxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_kjzzxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_kjzzxx', 'field': 'CBRQ', 'title': '出版日期', 'editable': 'False', 'type': 'date', 'create': 'True', },
            {'table': 'dr_kjzzxx', 'field': 'LZLBM', 'title': '论著类别码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_ky_lzlb:DM AS LZLBM,MC', 'where': ''},
            {'table': 'dr_kjzzxx', 'field': 'CBS', 'title': '出版社', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_ky_cbs:DM AS CBS,MC', 'where': ''},
            {'table': 'dr_kjzzxx', 'field': 'CBSJBM', 'title': '出版社级别码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_ky_cbsjb:DM AS CBSJBM,MC', 'where': ''},
            {'table': 'dr_kjzzxx', 'field': 'CBH', 'title': '出版号', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjzzxx', 'field': 'ZZZS', 'title': '著作字数', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjzzxx', 'field': 'ISBNH', 'title': 'ISBN号', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjzzxx', 'field': 'DYZZBH', 'title': '第一作者编号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_kjzzxx', 'field': 'DYZZ', 'title': '第一作者', 'editable': 'T', 'type': 'table', 'value': 'dr_jzgjcsjxx:JZGH AS DYZZBH,XM AS DYZZ', 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'T', },
        ]

    @staticmethod
    def get_search_columns() -> []:
        return ['ZZBH']


class VIEW_KJCGRYXX_ZZ(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_kjcgryxx_zz'
    __tablename__CH__ = '科技成果(著作)人员信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    RYH = Column('RYH', String(16), default='')  # 人员号
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    JSM = Column('JSM', String(16), default='')  # 角色码
    ZXZS = Column('ZXZS', Integer, default=0)  # 撰写字数
    PMZRS = Column('PMZRS', String(16), default='')  # 排名/总人数
    GXL = Column('GXL', String(16), default='')  # 贡献率
    XM = Column('XM', String(16), default='')  # 姓名
    DWH = Column('DWH', String(16), default='')  # 单位号
    SZDW = Column('SZDW', String(16), default='')  # 所在单位
    ZZBH = Column('ZZBH', String(16), default='')  # 著作编号
    KJCGRYBH = Column('KJCGRYBH', String(16), default='')  # 科技成果人员编号
    SMSX = Column('SMSX', String(16), default='')  # 署名顺序
    ZZMC = Column('ZZMC', String(16), default='')  # 著作名称
    CBRQ = Column('CBRQ', DateTime, default=now())  # 出版日期
    LZLBM = Column('LZLBM', String(16), default='')  # 论著类别码
    CBS = Column('CBS', String(16), default='')  # 出版社
    CBSJBM = Column('CBSJBM', String(16), default='')  # 出版社级别码
    ZZZS = Column('ZZZS', Integer, default=0)  # 著作字数
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_kjcgryxx_zz AS
            SELECT
               dr_kjcgryzz.id AS id,
               dr_kjcgryzz.RYH AS JZGH,
               dr_kjcgryzz.JSM AS JSM,
               dr_kjcgryzz.ZXZS AS ZXZS,
               dr_kjcgryzz.PMZRS AS PMZRS,
               dr_kjcgryzz.GXL AS GXL,
               dr_kjcgryzz.XM AS XM,
               dr_kjcgryzz.SZDW AS SZDW,
               dr_kjcgryzz.ZZBH AS ZZBH,
               dr_kjcgryzz.KJCGRYBH AS KJCGRYBH,
               dr_kjcgryzz.SMSX AS SMSX,
               dr_kjcgryzz.DWH AS DWH,
               dr_kjzz.ZZMC AS ZZMC,
               dr_kjzz.CBRQ AS CBRQ,
               dr_kjzz.LZLBM AS LZLBM,
               dr_kjzz.CBS AS CBS,
               dr_kjzz.CBSJBM AS CBSJBM,
               dr_kjzz.ZZZS AS ZZZS,
               dr_kjzz.DWMC AS DWMC,
               dr_kjzz.CBRQ AS stamp,
               dr_kjzz.note AS note
            FROM dr_kjcgryxx_zz dr_kjcgryzz
            LEFT JOIN dr_kjzzxx dr_kjzz on dr_kjcgryzz.ZZBH = dr_kjzz.ZZBH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_kjcgryxx_zz', 'dr_kjzzxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_kjcgryxx_zz']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_kjcgryxx_zz']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_kjcgryxx_zz', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_kjcgryxx_zz', 'field': 'RYH', 'title': '人员号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_kjcgryxx_zz', 'field': 'XM', 'title': '姓名', 'editable': 'True', 'type': 'table', 'value': 'dr_jzgjcsjxx:JZGH AS RYH,XM AS XM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'T', },
            {'table': 'dr_kjcgryxx_zz', 'field': 'JSM', 'title': '角色码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_ky_js:DM AS JSM,MC', 'where': ''},
            {'table': 'dr_kjcgryxx_zz', 'field': 'ZXZS', 'title': '撰写字数', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_zz', 'field': 'PMZRS', 'title': '排名/总人数', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_zz', 'field': 'GXL', 'title': '贡献率', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_zz', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_kjcgryxx_zz', 'field': 'SZDW', 'title': '所在单位', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_kjcgryxx_zz', 'field': 'ZZBH', 'title': '著作编号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_zz', 'field': 'KJCGRYBH', 'title': '科技成果人员编号', 'editable': 'False', 'type': 'text', 'create': 'True', },
            {'table': 'dr_kjcgryxx_zz', 'field': 'SMSX', 'title': '署名顺序', 'editable': 'False', 'type': 'text', 'create': 'True', },
        ]

    @staticmethod
    def get_search_columns() -> []:
        return ['ZZBH']


# zjx
class VIEW_JGXMXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_jgxmxx'
    __tablename__CH__ = '教改项目信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    DWH = Column('DWH', String(16), default='')  # 单位号
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    JZGXM = Column('JZGXM', String(16), default='')  # 教职工姓名
    GXL = Column('GXL', Float, default='')  # 贡献率
    ND = Column('ND', String(16), default='')  # 年度
    XMXH = Column('XMXH', String(16), default='')  # 项目序号
    XMBH = Column('XMBH', String(16), default='')  # 项目编号
    XMMC = Column('XMMC', String(16), default='')  # 项目名称
    XMFZRH = Column('XMFZRH', String(16), default='')  # 项目负责人号
    XM = Column('XM', String(16), default='')  # 姓名
    LXRQ = Column('LXRQ', DateTime, default='')  # 立项日期
    PZJF = Column('PZJF', String(16), default='')  # 批准经费
    XMJBM = Column('XMJBM', String(16), default='')  # 项目级别码
    JSLXM = Column('JSLXM', String(16), default='')  # 角色类型码
    SJLYM = Column('SJLYM', String(16), default='')  # 数据来源
    XMJB = Column('XMJB', String(16), default='')  # 项目级别
    CYRC = Column('CYRC', String(16), default='')  # 参与人次
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_jgxmxx AS
            SELECT
                dr_jg.id AS id,
                dr_jg.DWH AS DWH,
                dr_jg.JZGH AS JZGH,
                dr_jg.JZGXM AS JZGXM,
                dr_jg.GXL AS GXL,
                dr_jg.ND AS ND,
                dr_jg.XMXH AS XMXH,
                dr_jg.XMBH AS XMBH,
                dr_jg.XMMC AS XMMC,
                dr_jg.XMFZRH AS XMFZRH,
                dr_jg.XM AS XM,
                dr_jg.LXRQ AS LXRQ,
                dr_jg.PZJF AS PZJF,
                dr_jg.XMJBM AS XMJBM,
                dr_jg.JSLXM AS JSLXM,
                dr_jg.SJLYM AS SJLYM,
                dr_jg.XMJB AS XMJB,
                dr_jg.CYRC AS CYRC,
                dr_jg.stamp AS stamp,
                dr_jg.note AS note
            FROM dr_jgxmxx dr_jg
            LEFT JOIN dc_jgxmxx dc_jg ON dc_jg.JZGH=dr_jg.JZGH
            LEFT JOIN dr_zzjgjbsjxx dw ON dw.DWH=dr_jg.DWH
            LEFT JOIN dr_jzgjcsjxx jz ON jz.JZGH=dr_jg.JZGH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_jgxmxx', 'dr_zzjgjbsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_jgxmxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_jgxmxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_jgxmxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_jgxmxx', 'field': 'DWH', 'title': '单位名称', 'editable': 'T', 'type': 'inline', 'create': 'T', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_jgxmxx', 'field': 'JZGH', 'title': '教职工号', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_jgxmxx', 'field': 'JZGXM', 'title': '教职工姓名', 'editable': 'T', 'type': 'table', 'value': 'dr_jzgjcsjxx: JZGH AS JZGH, XM AS JZGXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'T', },
            {'table': 'dr_jgxmxx', 'field': 'ND', 'title': '年度', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jgxmxx', 'field': 'GXL', 'title': '贡献率', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jgxmxx', 'field': 'XMFZRH', 'title': '项目负责人号', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_jgxmxx', 'field': 'XM', 'title': '负责人姓名', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_jgxmxx', 'field': 'XMXH', 'title': '项目序号', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jgxmxx', 'field': 'XMBH', 'title': '项目编号', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jgxmxx', 'field': 'XMMC', 'title': '项目名称', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jgxmxx', 'field': 'LXRQ', 'title': '立项日期', 'editable': 'T', 'type': 'date', 'create': 'True', },
            {'table': 'dr_jgxmxx', 'field': 'PZJF', 'title': '批准经费', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jgxmxx', 'field': 'XMJBM', 'title': '项目级别码', 'editable': 'F', 'type': 'table', 'create': 'F', },
            {'table': 'dr_jgxmxx', 'field': 'XMJB', 'title': '项目级别', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'st_xx_jb:DM AS XMJBM,MC AS XMJB', 'where': ''},
            {'table': 'dr_jgxmxx', 'field': 'JSLXM', 'title': '角色类型码', 'editable': 'true', 'type': 'inline', 'create': 'T', 'value': 'st_ky_js:DM AS JSLXM,MC', 'where': ''},
            {'table': 'dr_jgxmxx', 'field': 'SJLYM', 'title': '数据来源', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jgxmxx', 'field': 'CYRC', 'title': '参与人次', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jgxmxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_jgxmxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> []:
        return ['XMBH']


class VIEW_JXCGJLSB(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_jxcgjlsb'
    __tablename__CH__ = '教学成果奖励申报'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    SBRH = Column('SBRH', String(16), default='')  # 申报人号
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    XM = Column('XM', String(16), default='')  # 姓名
    JXCGBH = Column('JXCGBH', String(16), default='')  # 教学成果编号
    JXCGLB = Column('JXCGLB', String(16), default='')  # 教学成果类别
    DWH = Column('DWH', String(16), default='')  # 单位号
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_jxcgjlsb AS
            SELECT 
                dr.id AS id,            
                dr.SBRH AS SBRH,            
                dr.SBRH AS JZGH, 
                dr.JXCGBH AS JXCGBH, 
                dr.JXCGLB AS JXCGLB, 
                jz.XM AS XM,
                jz.DWH AS DWH,
                jz.DWMC AS DWMC,   
                dr.stamp AS stamp,
                dr.note AS note
            FROM dr_jxcgjlsb dr
            LEFT JOIN view_jzgjcsjxx jz ON jz.JZGH=dr.SBRH
            WHERE 1=1
        """
            # jz.CSRQ AS stamp,
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_jxcgjlsb']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_jxcgjlsb']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_jxcgjlsb']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_jxcgjlsb', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },

            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {
                'table': 'dr_zzjgjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'False',
                'type': 'table', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s', 'create': 'True',
                'action': [{
                    'type': 'onclick',
                    'content': {'value': 'view_jzgjcsjxx:JZGH,XM', 'where': 'DWH IN :this', 'to': 'SBRH:JZGH,XM', },
                }],
            },
            {'table': 'dr_jxcgjlsb', 'field': 'SBRH', 'title': '申报人号', 'editable': 'False', 'type': 'inline', 'create': 'T', },
            {'table': 'dr_jzgjcsjxx', 'field': 'XM', 'title': '姓名', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_jxcgjlsb', 'field': 'JXCGBH', 'title': '教学成果编号', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_jxcgjlsb', 'field': 'JXCGLB', 'title': '教学成果类别', 'editable': 'T', 'type': 'inline','create': 'T', 'value': 'st_sb_jxcglb:DM AS JXCGLB,MC', 'where': ''},
            {'table': 'dr_jxcgjlsb', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_jxcgjlsb', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List:
        return ['JZGH', 'JXCGBH']


class VIEW_JXHJXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_jxhjxx'
    __tablename__CH__ = '教学获奖信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    FZRYH = Column('FZRYH', String(16), default='')  # 负责人员号
    FZRXM = Column('FZRXM', String(16), default='')  # 负责人姓名
    DWH = Column('DWH', String(16), default='')  # 单位号
    WCDW = Column('WCDW', String(16), default='')  # 完成单位
    JXCGBH = Column('JXCGBH', String(16), default='')  # 教学成果编号
    JXCGMC = Column('JXCGMC', DateTime, default='')  # 教学成果名称
    HJMC = Column('HJMC', String(16), default='')  # 获奖名称
    JLJBM = Column('JLJBM ', String(16), default='')  # 奖励级别码
    JLDJM = Column('JLDJM', String(16), default='')  # 奖励等级码
    JLLBM = Column('JLLBM', String(16), default='')  # 奖励类别码
    BJDW = Column('BJDW', String(16), default='')  # 颁奖单位
    BJNF = Column('BJNF', String(16), default='')  # 颁奖年份
    BJRQ = Column('BJRQ', String(16), default='')  # 颁奖日期
    ZYWCR = Column('ZYWCR', String(16), default='')  # 主要完成人
    WCRZS = Column('WCRZS', String(16), default='')  # 完成人总数
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_jxhjxx AS
            SELECT
               dr_kjxm.id AS id,
               dr_kjxm.FZRYH AS FZRYH,
               dr_kjxm.FZRXM AS FZRXM,
               dr_kjxm.DWH AS DWH,
               dr_kjxm.BJDW AS BJDW,
               dr_kjxm.JXCGBH AS JXCGBH,
               dr_kjxm.JXCGMC AS JXCGMC,
               dr_kjxm.HJMC AS HJMC,
               dr_kjxm.JLJBM AS JLJBM,
               dr_kjxm.JLDJM AS JLDJM,
               dr_kjxm.JLLBM AS JLLBM,
               dr_kjxm.BJNF AS BJNF,
               dr_kjxm.BJRQ AS BJRQ,
               dr_kjxm.ZYWCR AS ZYWCR,
               dr_kjxm.WCRZS AS WCRZS,
               dr_kjxm.BJRQ AS stamp,
               dr_kjxm.note AS note
            FROM dr_jxhjxx dr_kjxm
            LEFT JOIN dc_jxhjxx dc ON dr_kjxm.JXCGBH = dc.JXCGBH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_jxhjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_jxhjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_jxhjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_jxhjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_jxhjxx', 'field': 'JXCGMC', 'title': '教学成果名称', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jxhjxx', 'field': 'JXCGBH', 'title': '教学成果编号', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_jxhjxx', 'field': 'FZRYH', 'title': '负责人员号', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_jxhjxx', 'field': 'FZRXM', 'title': '负责人姓名', 'editable': 'T', 'type': 'table', 'value': 'dr_jzgjcsjxx:JZGH AS FZRYH,XM AS FZRXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'T', },
            {'table': 'dr_jxhjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'F', 'type': 'text', 'create': 'F', },
            {'table': 'dr_jxhjxx', 'field': 'BJDW', 'title': '颁奖单位', 'editable': 'F', 'type': 'table', 'create': 'T', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_jxhjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_jxhjxx', 'field': 'BJRQ', 'title': '颁奖日期', 'editable': 'T', 'type': 'date', 'create': 'T', },
            {'table': 'dr_jxhjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
            {'table': 'dr_jxhjxx', 'field': 'JLLBM', 'title': '奖励类别码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_jxcglbm:DM AS JLLBM,MC', 'where': ''},
            {'table': 'dr_jxhjxx', 'field': 'JLDJM', 'title': '奖励等级码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_jxcgdjm:DM AS JLDJM,MC', 'where': ''},
            {'table': 'dr_jxhjxx', 'field': 'JLJBM', 'title': '奖励级别码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_jldj:DM AS JLJBM,MC', 'where': ''},
        ]

    @staticmethod
    def get_search_columns() -> List:
        return ['FZRXM', 'JXCGMC', 'HJMC']


class VIEW_JXCGWCRXX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_jxcgwcrxx'
    __tablename__CH__ = '教学成果完成人信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    WCRH = Column('WCRH', String(16), default='')  # 完成人号
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    WCRXM = Column('WCRXM', String(16), default='')  # 完成人姓名
    WCRJSM = Column('WCRJSM', String(16), default='')  # 完成人角色码
    DWH = Column('DWH', String(16), default='')  # 单位号
    GXL = Column('GXL', Float, default=0.0)  # 贡献率
    WCDW = Column('WCDW', String(16), default='')  # 完成单位
    JXCGBH = Column('JXCGBH', String(16), default='')  # 教学成果编号
    JXCGMC = Column('JXCGMC', DateTime, default='')  # 教学成果名称
    HJMC = Column('HJMC', String(16), default='')  # 获奖名称
    JLJBM = Column('JLJBM', String(16), default='')  # 奖励级别码
    JLDJM = Column('JLDJM', String(16), default='')  # 奖励等级码
    JLLBM = Column('JLLBM', String(16), default='')  # 奖励类别码
    BJDW = Column('BJDW', String(16), default='')  # 颁奖单位
    BJNF = Column('BJNF', String(16), default='')  # 颁奖年份
    BJRQ = Column('BJRQ', String(16), default='')  # 颁奖日期
    ZYWCR = Column('ZYWCR', String(16), default='')  # 主要完成人
    WCRZS = Column('WCRZS', String(16), default='')  # 完成人总数
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_jxcgwcrxx AS
            SELECT
               dr_jxcg.id AS id,
               dr_jxcg.WCRH AS WCRH,
               dr_jxcg.WCRH AS JZGH,
               dr_jxcg.WCRXM AS WCRXM,
               dr_jxcg.WCRJSM AS WCRJSM,
               dr_jxcg.DWH AS DWH,
               dr_jxcg.WCDW AS WCDW,
               dr_jxcg.JXCGBH AS JXCGBH,
               dr_jxxx.JXCGMC AS JXCGMC,
               dr_jxxx.HJMC AS HJMC,
               dr_jxxx.JLJBM AS JLJBM,
               dr_jxxx.JLDJM AS JLDJM,
               dr_jxxx.JLLBM AS JLLBM,
               dr_jxcg.GXL AS GXL,
               dr_jxxx.BJDW AS BJDW,
               dr_jxxx.BJNF AS BJNF,
               dr_jxcg.BJRQ AS BJRQ,
               dr_jxxx.ZYWCR AS ZYWCR,
               dr_jxxx.WCRZS AS WCRZS,
               dr_jxcg.BJRQ AS stamp,
               dr_jxcg.note AS note
            FROM dr_jxcgwcrxx dr_jxcg
            LEFT JOIN dc_jxcgwcrxx dc_jxcg ON dr_jxcg.JXCGBH = dc_jxcg.JXCGBH
            LEFT JOIN dr_jxhjxx dr_jxxx ON dr_jxcg.JXCGBH= dr_jxxx.JXCGBH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_jxcgwcrxx', 'dr_jxhjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_jxcgwcrxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_jxcgwcrxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_jxcgwcrxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_jxcgwcrxx', 'field': 'JXCGBH', 'title': '教学成果编号', 'editable': 'F', 'type': 'text', 'create': 'F', },
            {'table': 'dr_jxcgwcrxx', 'field': 'JXCGMC', 'title': '教学成果名称', 'editable': 'T', 'type': 'table', 'create': 'True','value': 'dr_jxhjxx:JXCGBH,JXCGMC', 'where': '', },
            {'table': 'dr_jxcgwcrxx', 'field': 'DWH', 'title': '单位号', 'editable': 'F', 'type': 'text', 'create': 'F', },
            {'table': 'dr_jxcgwcrxx', 'field': 'WCDW', 'title': '完成单位', 'editable': 'T', 'type': 'table', 'create': 'T', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_jxcgwcrxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_jxcgwcrxx', 'field': 'BJRQ', 'title': '颁奖日期', 'editable': 'F', 'type': 'date', 'create': 'T', },
            {'table': 'dr_jxcgwcrxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
            {'table': 'dr_jxcgwcrxx', 'field': 'WCRH', 'title': '完成人号', 'editable': 'T', 'type': 'text', 'create': 'F', },
            {'table': 'dr_jxcgwcrxx', 'field': 'WCRXM', 'title': '完成人姓名', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_jzgjcsjxx:JZGH AS WCRH,XM AS WCRXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'"},
            {'table': 'dr_jxhjxx', 'field': 'JLLBM', 'title': '奖励类别码', 'editable': 'F', 'type': 'inline', 'create': 'F', 'value': 'st_jxcglbm:DM AS JLLBM,MC', 'where': ''},
            {'table': 'dr_jxhjxx', 'field': 'JLDJM', 'title': '奖励等级码', 'editable': 'F', 'type': 'inline', 'create': 'F', 'value': 'st_jxcgdjm:DM AS JLDJM,MC', 'where': ''},
            {'table': 'dr_jxhjxx', 'field': 'JLJBM', 'title': '奖励级别码', 'editable': 'F', 'type': 'inline', 'create': 'F', 'value': 'st_jldj:DM AS JLJBM,MC', 'where': ''},
            {'table': 'dr_jxcgwcrxx', 'field': 'GXL', 'title': '贡献率', 'editable': 'T', 'type': 'text', 'create': 'True', },
        ]

    @staticmethod
    def get_search_columns() -> List:
        return ['WCRXM', 'JXCGMC', 'HJMC']


class VIEW_ZDDXSKWKJHD(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_zddxskwkjhd'
    __tablename__CH__ = '指导大学生课外科技活动'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    XMBH = Column('XMBH', String(16), default='')  # 项目编号
    XMMC = Column('XMMC', String(16), default='')  # 项目名称
    XMZC = Column('XMZC', String(16), default='')  # 项目组次
    DWH = Column('DWH', String(16), default='')  # 单位号
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    FZRYH = Column('FZRYH', String(16), default='')  # 负责人员号
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    FZRXM = Column('FZRXM', String(16), default='')  # 负责人姓名
    XMJBM = Column('XMJBM', String(16), default='')  # 项目级别码
    XMRQ = Column('XMRQ', DateTime, default=now())  # 项目日期
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
                CREATE VIEW view_zddxskwkjhd AS
                SELECT
                   dr_kjxm.id AS id,
                   dr_kjxm.XMBH AS XMBH,
                   dr_kjxm.XMMC AS XMMC,
                   dr_kjxm.XMZC AS XMZC,
                   dr_kjxm.FZRYH AS FZRYH,
                   dr_kjxm.FZRYH AS JZGH,
                   dr_kjxm.FZRXM AS FZRXM,
                   dr_kjxm.DWH AS DWH,
                   dr_kjxm.DWMC AS DWMC,
                   dr_kjxm.XMJBM AS XMJBM,
                   dr_kjxm.XMRQ AS stamp,
                   dr_kjxm.XMRQ AS XMRQ,
                   dr_kjxm.note AS note
                FROM dr_dxskjxmjbsjxx dr_kjxm
                WHERE 1=1
            """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_dxskjxmjbsjxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_dxskjxmjbsjxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_dxskjxmjbsjxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_dxskjxmjbsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_dxskjxmjbsjxx', 'field': 'XMBH', 'title': '项目编号', 'editable': 'T', 'type': 'text', 'create': 'T', },
            {'table': 'dr_dxskjxmjbsjxx', 'field': 'XMMC', 'title': '项目名称', 'editable': 'T', 'type': 'text', 'create': 'True','value': '', 'where': '', },
            {'table': 'dr_dxskjxmjbsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'F', 'type': 'text', 'create': 'F', },
            {'table': 'dr_dxskjxmjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'T', 'type': 'table', 'create': 'T', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_dxskjxmjbsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_dxskjxmjbsjxx', 'field': 'XMRQ', 'title': '项目日期', 'editable': 'T', 'type': 'date', 'create': 'T', },
            {'table': 'dr_dxskjxmjbsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
            {'table': 'dr_dxskjxmjbsjxx', 'field': 'FZRYH', 'title': '负责人员号', 'editable': 'T', 'type': 'text', 'create': 'F', },
            {'table': 'dr_dxskjxmjbsjxx', 'field': 'FZRXM', 'title': '负责人姓名', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_jzgjcsjxx:JZGH AS FZRYH,XM AS FZRXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'"},
            {'table': 'dr_dxskjxmjbsjxx', 'field': 'XMJBM', 'title': '项目级别码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_xmbh:DM AS XMJBM,MC', 'where': ''},
            {'table': 'dr_dxskjxmjbsjxx', 'field': 'XMZC', 'title': '项目组次', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_xmzc:DM AS XMZC,MC', 'where': ''},
        ]

    @staticmethod
    def get_search_columns() -> List:
        return ['XMMC', 'FZRXM', ]


class VIEW_ZDYXLWJ(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_zdyxlwj'
    __tablename__CH__ = '指导学生获得优秀学位论文奖'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    LWBH = Column('LWBH', String(16), default='')  # 论文编号
    LWTM = Column('LWTM', String(16), default='')  # 论文题目
    LWLX = Column('LWLX', String(16), default='')  # 论文类型
    ZDRXM = Column('ZDRXM', String(16), default='')  # 指导人姓名
    ZDRH = Column('ZDRH', String(16), default='')  # 指导人号
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    DWH = Column('DWH', String(16), default='')  # 单位号
    LWHJJBM = Column('LWHJJBM', String(16), default='')  # 论文获奖级别码
    LWQSRQ = Column('GJJF', String(16), default='')  # 论文起始日期
    LWZZRQ = Column('LWZZRQ', String(16), default='')  # 论文终止日期
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_zdyxlwj AS
            SELECT
               dr_lwxx.id AS id,
               dr_lwxx.LWBH AS LWBH,
               dr_lwxx.LWTM AS LWTM,
               dr_lwxx.LWLX AS LWLX,
               dr_lwxx.ZDRXM AS ZDRXM,
               dr_lwxx.ZDRH AS ZDRH,
               dr_lwxx.ZDRH AS JZGH,
               dr_lwxx.DWMC AS DWMC,
               dr_lwxx.DWH AS DWH,
               dr_lwxx.LWHJJBM AS LWHJJBM,
               dr_lwxx.LWZZRQ AS LWZZRQ,
               dr_lwxx.LWZZRQ AS stamp,
               dr_lwxx.note AS note
            FROM dr_xwlwxx dr_lwxx
            LEFT JOIN dc_xwlwxx dc_lwxx ON dc_lwxx.LWBH = dr_lwxx.LWBH
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_xwlwxx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_xwlwxx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_xwlwxx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_xwlwxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_xwlwxx', 'field': 'LWBH', 'title': '论文编号', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xwlwxx', 'field': 'LWTM', 'title': '论文题目', 'editable': 'T', 'type': 'text', 'create': 'True', },
            {'table': 'dr_xwlwxx', 'field': 'LWLX', 'title': '论文类型', 'editable': 'T', 'type': 'inline', 'create': 'True','value': 'st_lwlx:DM AS LWLX,MC', 'where': ''},
            {'table': 'dr_xwlwxx', 'field': 'LWHJJBM', 'title': '论文获奖级别码', 'editable': 'T', 'type': 'inline', 'create': 'True', 'value': 'st_lwjbm:DM AS LWHJJBM,MC', 'where': ''},
            {'table': 'dr_xwlwxx', 'field': 'ZDRH', 'title': '指导人号', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_xwlwxx', 'field': 'ZDRXM', 'title': '指导人姓名', 'editable': 'T', 'type': 'table', 'value': 'dr_jzgjcsjxx:JZGH AS ZDRH,XM AS ZDRXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'T', },
            {'table': 'dr_xwlwxx', 'field': 'DWH', 'title': '单位号', 'editable': 'F', 'type': 'text', 'create': 'F', },
            {'table': 'dr_xwlwxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'F', 'type': 'table', 'create': 'T', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_xwlwxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_xwlwxx', 'field': 'LWZZRQ', 'title': '论文终止日期', 'editable': 'T', 'type': 'date', 'create': 'T', },
            {'table': 'dr_xwlwxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List:
        return ['LWTM', 'ZDRXM', ]


class VIEW_YJSDSPYGX(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_yjsdspygx'
    __tablename__CH__ = '研究生导师培养关系'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    XSXH = Column('XSXH', String(16), default='')  # 学生学号
    XSXM = Column('XSXM', String(16), default='')  # 学生姓名
    XSLBM = Column('XSLBM', String(16), default='')  # 学生类别码
    PYFSM = Column('PYFSM', String(16), default='')  # 培养方式码
    XSDQZTM = Column('XSDQZTM', String(16), default='')  # 学生当前状态码
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    XM = Column('XM', String(16), default='')  # 导师姓名
    DWH = Column('DWH', String(16), default='')  # 单位号
    SZDW = Column('SZDW', String(16), default='')  # 所在单位
    SFFDS = Column('SFFDS', String(16), default='')  # 是否为副导师
    FPXS = Column('FPXS', Float(16), default='')  # 工作量分配系数
    XXGXRQ = Column('XXGXRQ', DateTime, default='')  # 信息更新日期
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_yjsdspygx AS
            SELECT
               dr.id AS id,
               dr.XSXH AS XSXH,
               dr.XSXM AS XSXM,
               dr.XSLBM AS XSLBM,
               dr.PYFSM AS PYFSM,
               dr.XSDQZTM AS XSDQZTM,
               dr.JZGH AS JZGH,
               dr.XM AS XM,
               dr.DWH AS DWH,
               dr.SZDW AS SZDW,
               dr.SFFDS AS SFFDS,
               dr.FPXS AS FPXS,
               dr.XXGXRQ AS stamp,
               dr.note AS note
            FROM dr_yjsdspygx dr
            WHERE 1=1
        """
        return sql_v1

    @staticmethod
    def get_upload_tables() -> List[str]:
        return ['dr_yjsdspygx']

    @staticmethod
    def get_delete_tables() -> List[str]:
        return ['dr_yjsdspygx']

    @staticmethod
    def get_create_tables() -> List[str]:
        return ['dr_yjsdspygx']

    @staticmethod
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        return [
            {'table': 'dr_yjsdspygx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_yjsdspygx', 'field': 'XSXH', 'title': '学生学号', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_yjsdspygx', 'field': 'XSXM', 'title': '学生姓名', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_yjsdspygx', 'field': 'XSLBM', 'title': '学生类别码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_xs_xslb:DM AS XSLBM,MC', 'where': ''},
            {'table': 'dr_yjsdspygx', 'field': 'PYFSM', 'title': '培养方式码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_xs_pyfs:DM AS PYFSM,MC', 'where': ''},
            {'table': 'dr_yjsdspygx', 'field': 'XSDQZTM', 'title': '学生当前状态码', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_xs_xsdqzt:DM AS XSDQZTM,MC', 'where': ''},
            {'table': 'dr_yjsdspygx', 'field': 'JZGH', 'title': '教职工号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_yjsdspygx', 'field': 'XM', 'title': '导师姓名', 'editable': 'True', 'type': 'table', 'value': 'dr_jzgjcsjxx:JZGH,XM', 'where': "DWH IN %(departments)s AND JZGH!='admin'", 'create': 'T', },
            {'table': 'dr_yjsdspygx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'False', },
            {'table': 'dr_yjsdspygx', 'field': 'SZDW', 'title': '所在单位', 'editable': 'T', 'type': 'table', 'create': 'True', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_yjsdspygx', 'field': 'SFFDS', 'title': '是否为副导师', 'editable': 'True', 'type': 'inline', 'create': 'True', 'value': 'st_xs_dssf:DM AS SFFDS,MC', 'where': ''},
            {'table': 'dr_yjsdspygx', 'field': 'FPXS', 'title': '工作量分配系数', 'editable': 'True', 'type': 'text', 'create': 'True', },
            {'table': 'dr_yjsdspygx', 'field': 'XXGXRQ', 'title': '信息更新日期', 'editable': 'True', 'type': 'date', 'create': 'True', },
            {'table': 'dr_yjsdspygx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', 'create': 'False', },
            {'table': 'dr_yjsdspygx', 'field': 'note', 'title': '备注', 'editable': 'False', 'type': 'text', 'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> []:
        return ['JZGH']


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
