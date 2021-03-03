# coding: utf-8
# 规则引擎使用，不需要移植到数据库；view模型改变后，需重新手工执行rule.py
# TODO: search tips
# TODO: view performance. possible to move view to table and sync between tables

from jx.sqlalchemy_env import *

# Example: DON'T change "cl_ass"
'''
cl_ass ApplyCode(Base):  # 类名
    """
        The class in module matches with database data source and inherits from SQLAlchemy Base.
        __tablename__: database table or view
        parameters: table column
        Please add "  # Name" notes to show in FE and match parameter with BE.
        前端定义规则时可以用注释中的表名和字段名。可以自定义，例如枚举类型：" 状态: {1: "是"， 0: "否"}"
    """

    __tablename__ = 'table_code'  # Test Table or View

    id = Column('id', Integer, primary_key=True)  # ID
    code = Column('code', String(128))  # CODE
    status = Column('status', Integer, default=1)  # 状态
    uid = Column('uid', String(128))  # UID

    def __init__(self, id, code, status, uid):
        """
        Use to match rule-engine default __init__ if no db connect. Useless and just so as this.
        :param id:
        :param code:
        :param status:
        :param uid:
        """
        self.id = id
        self.code = code
        self.status = status
        self.uid = uid

    @staticmethod
    def sql() -> str:
        sql_v1 = """
            CREATE VIEW view_name AS
            SELECT t1.*, t2.*
            FROM table1 t1
            LEFT JOIN table2 t2 ON t2.id=t1.table2_id
            WHERE 1=1
        """
        return sql_v1
'''

# DON'T touch below SQL which related to auto management
"""
    DROP VIEW view_sysuser;
    CREATE VIEW view_sysuser AS
    SELECT su.*, ro.role_name, jg.JZGH, jg.XM, jg.DWH, zz.DWMC
    FROM jx_sysuser su
    LEFT JOIN jx_role ro ON ro.id=su.role_id
    LEFT JOIN view_jzgjcsjxx jg ON jg.JZGH=su.payroll
    LEFT JOIN view_zzjgjbsjxx zz ON zz.DWH=jg.DWH;
"""


class VIEW_ZZJGJBSJXX(Base):  # 组织机构基本数据信息
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_zzjgjbsjxx'  # 组织机构基本数据信息

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
    SXRQ = Column('SXRQ', DateTime, default=now())  # 失效日期
    SFST = Column('SFST', String(128), default='')  # 是否实体
    JLNY = Column('JLNY', DateTime, default=now())  # 建立年月
    DWFZRH = Column('DWFZRH', String(128), default='')  # 单位负责人号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def sql() -> str:  # NOTE: run by rule.py to recreate data view
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
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['DWMC']

    @staticmethod
    def get_title_columns() -> List[dict]:
        # TODO: multi-sources to update dr data
        return [
            {'table': 'dr_zzjgjbsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'True', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWYWMC', 'title': '单位英文名称', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWJC', 'title': '单位简称', 'editable': 'True', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWYWJC', 'title': '单位英文简称', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWJP', 'title': '单位简拼', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWDZ', 'title': '单位地址', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'SZXQ', 'title': '所在校区', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'LSDWH', 'title': '隶属单位号', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWLBM', 'title': '单位类别码', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWBBM', 'title': '单位办别码', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWYXBS', 'title': '单位有效标识', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'SXRQ', 'title': '失效日期', 'editable': 'False', 'type': 'date', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'SFST', 'title': '是否实体', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'JLNY', 'title': '建立年月', 'editable': 'False', 'type': 'date', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWFZRH', 'title': '单位负责人号', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', },
        ]

    @staticmethod
    def get_managed_departments(_department_id) -> list:
        departments = [_department_id]
        try:
            dpmts_query = db.query(VIEW_ZZJGJBSJXX)
            dpmts_query = dpmts_query.filter(VIEW_ZZJGJBSJXX.LSDWH == str(_department_id))
            dpmts = dpmts_query.all()

            for dpmt in dpmts:
                departments.extend(VIEW_ZZJGJBSJXX.get_managed_departments(str(dpmt.DWH)))
        except:
            logger.error(sys_info())
            pass

        return list(set(departments))

    @staticmethod
    def get_parent_department(_department_id) -> str:
        try:
            dpmts_query = db.query(VIEW_ZZJGJBSJXX)
            dpmts_query = dpmts_query.filter(VIEW_ZZJGJBSJXX.DWH == str(_department_id))
            dpmts = dpmts_query.all()

            for dpmt in dpmts:
                return str(dpmt.LSDWH)
        except:
            logger.error(sys_info())

        return ''


class VIEW_BKSJXZXS(Base):  # 本科生教学总学时
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_bksjxzxs'  # 本科生教学总学时

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

    @staticmethod
    def get_managed_departments(_payroll) -> List[str]:
        try:
            users_query = db.query(VIEW_JZGJCSJXX)
            users_query = users_query.filter(VIEW_JZGJCSJXX.JZGH == str(_payroll))
            users = users_query.all()
            return VIEW_ZZJGJBSJXX.get_managed_departments(users[0].DWH)
        except:
            return []


class VIEW_JZGJCSJXX(Base):  # 教职工基础数据信息
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_jzgjcsjxx'  # 教职工基础数据信息

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JZGH = Column('JZGH', String(16), unique=True, default='')  # 教职工号
    DWH = Column('DWH', String(16), default='')  # 单位号
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
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_jzgjcsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'JZGH', 'title': '教职工号', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'True', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'XM', 'title': '姓名', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'YWXM', 'title': '英文姓名', 'editable': 'True', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'XMPY', 'title': '姓名拼音', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'CYM', 'title': '曾用名', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'XBM', 'title': '性别码', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'CSRQ', 'title': '出生日期', 'editable': 'False', 'type': 'date', },
            {'table': 'dr_jzgjcsjxx', 'field': 'CSDM', 'title': '出生地码', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'BZLBM', 'title': '编制类别码', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'JZGLBM', 'title': '教职工类别码', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'DQZTM', 'title': '当前状态码', 'editable': 'False', 'type': 'text', },
            {'table': 'dr_jzgjcsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date', },
            {'table': 'dr_jzgjcsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text', },
        ]

    @staticmethod
    def get_search_columns() -> List[str]:
        return ['XM']

    @staticmethod
    def get_managed_departments(_payroll) -> List[str]:
        try:
            users_query = db.query(VIEW_JZGJCSJXX)
            users_query = users_query.filter(VIEW_JZGJCSJXX.JZGH == str(_payroll))
            users = users_query.all()
            return VIEW_ZZJGJBSJXX.get_managed_departments(users[0].DWH)
        except:
            return []


class VIEW_XMJFXX(Base):  # 项目经费信息
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_xmjfxx'  # 项目经费信息

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID

    JHJFZE = Column('JHJFZE', Float, unique=True, default=0.0)  # 计划经费总额
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

    # NOTE1: NOT from dr and dc, FROM other tables or views
    # NOTE2: used to filter out data
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
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note']

    @staticmethod
    def get_title_columns() -> List[str]:
        # NOTE: enum data: 'type': 'enum', 'value': ['未启用', '已启用'],
        # NOTE: static data from db: 'type': 'static', 'value': 'jx_usertype:id:usertype_name', 'where': ''
        # NOTE: SQL data from db: 'type': 'table', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'
        return [
            {'table': 'dr_xmjfxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text',
             'create': 'False', },
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text',
             'create': 'False', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'False', 'type': 'table',
             'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s', 'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'JZGH', 'title': '教职工号', 'editable': 'False', 'type': 'text',
             'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'JHJFZE', 'title': '计划经费总额', 'editable': 'True', 'type': 'float',
             'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'XMJFLYM', 'title': '项目经费来源码', 'editable': 'False', 'type': 'text',
             'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'BRRQ', 'title': '拨入日期', 'editable': 'False', 'type': 'date',
             'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'BKS', 'title': '拨款数', 'editable': 'True', 'type': 'float',
             'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'ZCRQ', 'title': '支出日期', 'editable': 'True', 'type': 'date',
             'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'BFXZDWJF', 'title': '拨付协作单位经费', 'editable': 'True', 'type': 'float',
             'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'XMPZBH', 'title': '项目凭证编号', 'editable': 'True', 'type': 'text',
             'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'JBRXM', 'title': '经办人姓名', 'editable': 'False', 'type': 'text',
             'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'XMBH', 'title': '项目编号', 'editable': 'False', 'type': 'text',
             'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'ZZKS', 'title': '支出款数', 'editable': 'True', 'type': 'float',
             'create': 'True', },
            {'table': 'dr_xmjfxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date',
             'create': 'False', },
            {'table': 'dr_xmjfxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text',
             'create': 'False', },
        ]

    @staticmethod
    def get_search_columns() -> List:
        return ['JZGH', 'DWH', 'DWMC', 'XMBH', 'JBRXM']


class VIEW_HJCGJBSJXX(Base):  # 获奖成果基本数据信息
    __tablename__ = 'view_hjcgjbsjxx'  # 获奖成果基本数据信息
    __table_args__ = {'extend_existing': True}

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
    FZRXM = Column('FZRXM', String(16), default='')  # 负责人姓名
    YJXK = Column('YJXK', String(16), default='')  # 一级学科
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    YJSMC = Column('YJSMC', String(16), default='')  # 研究所名称
    CGXS = Column('CGXS', String(16), default='')  # 成果形式
    HJMC = Column('HJMC', String(16), default='')  # 获奖名称
    HJBH = Column('HJBH', String(16), default='')  # 获奖编号
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
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
    def get_hide_columns() -> List[str]:
        return ['id', 'stamp', 'note', 'RYH']

    @staticmethod
    def get_title_columns() -> List[str]:
        # NOTE: enum data: 'type': 'enum', 'value': ['未启用', '已启用'],
        # NOTE: static data from db: 'type': 'static', 'value': 'jx_usertype,id,usertype_name', 'where': ''
        # NOTE: SQL data from db: 'type': 'table', 'value': 'dr_zzjgjbsjxx,DWH,DWMC', 'where': 'DWH IN %(departments)s'
        return [
            {'table': 'dr_hjcgjbsjxx', 'field': 'id', 'title': 'ID', 'editable': 'False', 'type': 'text',
             'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'HJCGBH', 'title': '获奖成果编号', 'editable': 'T', 'type': 'text',
             'create': 'True', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'HJCGMC', 'title': '获奖成果名称', 'editable': 'T', 'type': 'text',
             'create': 'True', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'RYH', 'title': '人员号', 'editable': 'False', 'type': 'text',
             'create': 'F', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'FZRYH', 'title': '负责人员号', 'editable': 'False', 'type': 'text',
             'create': 'F', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'FZRXM', 'title': '负责人姓名', 'editable': 'T', 'type': 'table',
             'value': 'dr_jzgjcsjxx:JZGH AS FZRYH,XM AS FZRXM', 'where': "DWH IN %(departments)s AND JZGH!='admin'",
             'create': 'T', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'F', 'type': 'text',
             'create': 'false', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'T', 'type': 'table',
             'create': 'True', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s'},
            {'table': 'dr_hjcgjbsjxx', 'field': 'YJSMC', 'title': '研究所名称', 'editable': 'T', 'type': 'text',
             'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'HJRQ', 'title': '获奖日期', 'editable': 'true', 'type': 'date',
             'create': 'True', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'CGHJLBM', 'title': '成果获奖类别码', 'editable': 'True', 'type': 'inline',
             'create': 'F', 'value': 'st_ky_cghjlb:DM AS CGHJLBM,MC', 'where': ''},
            {'table': 'dr_hjcgjbsjxx', 'field': 'KJJLB', 'title': '科技奖类别', 'editable': 'False', 'type': 'text',
             'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'JLDJM', 'title': '奖励等级码', 'editable': 'true', 'type': 'inline',
             'create': 'T', 'value': 'st_jldj:DM as JLDJM,MC', 'where': ''},
            {'table': 'dr_hjcgjbsjxx', 'field': 'HJJBM', 'title': '获奖级别码', 'editable': 'False', 'type': 'text',
             'create': 'False', },  # need value
            {'table': 'dr_hjcgjbsjxx', 'field': 'BJDW', 'title': '颁奖单位', 'editable': 'T', 'type': 'text',
             'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'SSXMBH', 'title': '所属项目编号', 'editable': 'T', 'type': 'text',
             'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'DWPM', 'title': '单位排名', 'editable': 'T', 'type': 'text',
             'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'CGXS', 'title': '成果形式', 'editable': 'T', 'type': 'text',
             'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'stamp', 'title': '时间戳', 'editable': 'False', 'type': 'date',
             'create': 'False', },
            {'table': 'dr_hjcgjbsjxx', 'field': 'note', 'title': '备注', 'editable': 'True', 'type': 'text',
             'create': 'False', },
        ]


class VIEW_KJCGRYXX_JL(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'view_kjcgryxx_jl'  # 获奖成果基本数据信息

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    RYH = Column('RYH', String(16), unique=True, default='')  # 人员号
    JSM = Column('JSM', String(16), default='')  # 角色码
    ZXZS = Column('ZXZS', String(16), default='')  # 撰写字数
    PMZRS = Column('PMZRS', String(16), default='')  # 排名/总人数
    GXL = Column('GXL', Float, default=0.0)  # 贡献率
    XM = Column('XM', String(16), default='')  # 姓名
    SZDW = Column('SZDW', String(16), default='')  # 所在单位
    RYLX = Column('RYLX', String(16), default='')  # 人员类型
    HJCGBH = Column('HJCGBH', String(16), default='')  # 获奖成果编号
    KJCGRYBH = Column('KJCGRYBH', String(16), default='')  # 科技成果人员编号


def get_class_attribute(file='./module.py'):
    """
        Return all classes' name, table, table name, columns, etc.
        This data dictionary should be done as a URL and can be used by FE while editing rules.
        Below json is only an example, which can be customized while realization.
    :return: [
        {
            'class': 'ApplyCode',  # from class ApplyCode name
            'classname': '类名',  # from class name to show in FE
            'table': 'view_code',  # from class ApplyCode -> __tablename__ value
            'tablename': 'Test Table or View',  # from class ApplyCode -> __tablename__ note
            'columns': [
                {
                    'name': 'id',  # table column
                    'label': 'ID',  # column label to show in FE
                    'type': 'Integer',  # column type
                    'value': {}  # value set
                }
            ]
        }
    ]
    """

    import re
    json = []
    one_class = {}

    with open(file, 'r') as f:
        for line in f.readlines():
            ls = line.strip()

            try:
                m_class = re.match(r'class (.*)\(Base\): {2}# (.*)', ls)
                if m_class:
                    one_class.clear()
                    one_class['class'] = m_class.group(1)
                    one_class['classname'] = m_class.group(2)
                    continue

                m_table = re.match(r'__tablename__ = \'(.*)\' {2}# (.*)', ls)
                if m_table:
                    one_class['table'] = m_table.group(1)
                    one_class['tablename'] = m_table.group(2)
                    one_class['columns'] = []
                    continue

                # TODO: class/classname is useful. field definition can be replaced by class.get_title_columns()
                m_column = re.match(r'(.*) = Column\(\'(.*)\', (.*), (.*)\) {2}# (.*)', ls)
                if m_column:
                    one_class['columns'].append(
                        {
                            'name': m_column.group(2),
                            'label': m_column.group(5),
                            'type': m_column.group(3),
                            'value': {}  # TODO
                        }
                    )
                    continue

                m_column = re.match(r'(.*) = Column\(\'(.*)\', (.*)\) {2}# (.*)', ls)
                if m_column:
                    one_class['columns'].append(
                        {
                            'name': m_column.group(2),
                            'label': m_column.group(4),
                            'type': m_column.group(3),
                            'value': {}  # TODO
                        }
                    )
                    continue

                m_init = re.match(r'def __init__(.*)', ls)
                if m_init:
                    json.append(one_class)
                    continue

            except Exception:
                logger.error(sys_info())
                continue

    return json


def generate_class_view(file='./module.py'):
    """
    Generate view for rule_engine to run after module.py changed.
    :param file:
    :return:
    """
    import re
    try:
        module = __import__('jx.module', fromlist=(["module"]))
    except ImportError:
        module = __import__('module')

    with open(file, 'r') as f:
        for line in f.readlines():
            m_class = re.match(r'class (.*)\(Base\): {2}# (.*)', line.strip())
            if m_class:
                v_class = getattr(module, m_class.group(1))
                try:
                    print("DROP VIEW " + v_class.__tablename__)
                    cursor.execute("DROP VIEW " + v_class.__tablename__)
                except OperationalError as e:
                    print(e)
                except Exception as e:
                    print(e)

                print(v_class.sql())
                cursor.execute(v_class.sql())
    return


if __name__ == '__main__':
    # TODO: get all classes in this module to drop/create view
    generate_class_view()
    print(get_class_attribute())
    exit(0)

    # try:
    #     cursor.execute("DROP VIEW " + VIEW_ZZJGJBSJXX.__tablename__)
    # except OperationalError as e:
    #     pass
    # except Exception as e:
    #     pass
    #
    # cursor.execute(VIEW_ZZJGJBSJXX.sql())

    exit(0)

    # try:
    #     Base.metadata.create_all(engine)
    #     obj = VIEW_ZZJGJBSJXX(DWH='1223', JLNY='2020-01-01')
    #     db.add(obj)
    #     db.commit()
    # except IntegrityError as e:
    #     print(e.orig)
    #
    # except:
    #     print(sys_info())
    #
    exit(0)
