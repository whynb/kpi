# coding=utf-8
# 定义导入数据模型，与东大校标一致; 可自动运行建表，字段变化后需要手工写SQL调整

from jx.sqlalchemy_env import *

class DR_ZZJGJBSJXX(Base):
    __tablename__ = 'dr_zzjgjbsjxx'
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
    SXRQ = Column('SXRQ', DateTime, default=now())  # 失效日期
    SFST = Column('SFST', String(128), default='')  # 是否实体
    JLNY = Column('JLNY', DateTime, default=now())  # 建立年月
    DWFZRH = Column('DWFZRH', String(128), default='')  # 单位负责人号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '单位号': ['DWH'],
            '单位名称': ['DWMC'],
            '单位英文名称': ['DWYWMC'],
            '单位简称': ['DWJC'],
            '单位英文简称': ['DWYWJC'],
            '单位简拼': ['DWJP'],
            '单位地址': ['DWDZ'],
            '所在校区': ['SZXQ'],
            '隶属单位号': ['LSDWH'],
            '单位类别码': ['DWLBM'],
            '单位办别码': ['DWBBM'],
            '单位有效标识': ['DWYXBS'],
            '失效日期': ['SXRQ', 'DateTime'],
            '是否实体': ['SFST'],
            '建立年月': ['JLNY', 'DateTime'],
            '单位负责人号': ['DWFZRH'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['DWH']


class DR_BJSJXX(Base):
    '''
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
    '''

    __tablename__ = 'dr_bjsjxx'
    __tablename__CN__ = '班级数据信息'

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
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
            '班号': ['BH'],
            '班级': ['BJ'],
            '建班年月': ['JBNY', 'DateTime'],
            '入学年份': ['RXNF', 'DateTime'],
            '辅导员号': ['FDYH'],
            '班导师': ['BDS'],
            '所属学院': ['SSXY'],
            '所属专业': ['SSZY'],
            '学生类别': ['XSLB'],
            '启用标志': ['QYBZ'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['BH']


class DR_YJSPKSJXX(Base):  # 研究生排课数据信息

    __tablename__ = 'dr_yjspksjxx'  # 研究生排课数据信息
    __table_args__ = (UniqueConstraint(
        'JSGH', 'KCH', 'KKXND', 'KKXQM',
        name='_dr_yjspksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc'),
    )
    __tablename__CN__ = '研究生排课数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JSGH = Column('JSGH', String(16), default='')  # 教师工号
    KCH = Column('KCH', String(16), default='')  # 课程号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KKXND = Column('KKXND', String(16), default='')  # 开课学年度
    SKBJH = Column('SKBJH', String(16), default='')  # 上课班级号
    KKXQM = Column('KKXQM', DateTime, default=now())  # 开课学期码
    ZXXS = Column('ZXXS', String(16), default='')  # 总学时
    ZKJHXS = Column('ZKJHXS', String(16), default='')  # 助课计划学时
    SYZS = Column('SYZS', String(16), default='')  # 实验组数
    JXMSJBM = Column('JXMSJBM', String(16), default='')  # 教学名师级别码
    WYKCTJM = Column('WYKCTJM', String(16), default='')  # 外语课程调节码
    KCJBM = Column('KCJBM', String(16), default='')  # 课程级别码
    ZLXS = Column('ZLXS', String(16), default='')  # 质量系数
    HBS = Column('HBS', String(16), default='')  # 合班数
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '教师工号': ['JSGH'],
            '课程号': ['KCH'],
            '教师姓名': ['JSXM'],
            '开课学年度': ['KKXND'],
            '上课班级号': ['SKBJH'],
            '开课学期码': ['KKXQM', 'DateTime'],
            '总学时': ['ZXXS'],
            '助课计划学时': ['ZKJHXS'],
            '实验组数': ['SYZS'],
            '教学名师级别码': ['JXMSJBM'],
            '外语课程调节码': ['WYKCTJM'],
            '课程级别码': ['KCJBM'],
            '质量系数': ['ZLXS'],
            '合班数': ['HBS'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['JSGH', 'KCH', 'KKXND', 'KKXQM',]


class DR_PKSJXX(Base):  # 排课数据信息

    __tablename__ = 'dr_pksjxx'  # 排课数据信息
    __table_args__ = (UniqueConstraint(
        'JSGH', 'KCH', 'KKXND', 'KKXQM', 'SKBJH',
        name='_dr_pksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc'),
    )
    __tablename__CN__ = '排课数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JSGH = Column('JSGH', String(16), default='')  # 教师工号
    KCH = Column('KCH', String(16), default='')  # 课程号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KKXND = Column('KKXND', String(16), default='')  # 开课学年度
    SKBJH = Column('SKBJH', String(16), default='')  # 上课班级号
    KKXQM = Column('KKXQM', DateTime, default=now())  # 开课学期码
    ZXXS = Column('ZXXS', String(16), default='')  # 总学时
    ZKJHXS = Column('ZKJHXS', String(16), default='')  # 助课计划学时
    SYZS = Column('SYZS', String(16), default='')  # 实验组数
    JXMSJBM = Column('JXMSJBM', String(16), default='')  # 教学名师级别码
    WYKCTJM = Column('WYKCTJM', String(16), default='')  # 外语课程调节码
    KCJBM = Column('KCJBM', String(16), default='')  # 课程级别码
    ZLXS = Column('ZLXS', Float(16), default='')  # 质量系数
    HBS = Column('HBS', Float(16), default='')  # 合班数
    DWH = Column('DWH', String(16), default='')  # 单位号
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '教师工号': ['JSGH'],
            '课程号': ['KCH'],
            '教师姓名': ['JSXM'],
            '开课学年度': ['KKXND'],
            '上课班级号': ['SKBJH'],
            '开课学期码': ['KKXQM', 'DateTime'],
            '总学时': ['ZXXS'],
            '助课计划学时': ['ZKJHXS'],
            '实验组数': ['SYZS'],
            '教学名师级别码': ['JXMSJBM'],
            '外语课程调节码': ['WYKCTJM'],
            '课程级别码': ['KCJBM'],
            '质量系数': ['ZLXS', 'Float'],
            '合班数': ['HBS', 'Float'],
            '单位号': ['DWH'],
            '单位名称': ['DWMC'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['JSGH', 'KCH', 'KKXND', 'KKXQM', 'SKBJH']


class DR_PKZKSJXX(Base):  # 排课助课数据信息

    __tablename__ = 'dr_pkzksjxx'  # 排课助课数据信息
    __table_args__ = (UniqueConstraint(
        'JSGH', 'KCH', 'KKXND', 'KKXQM', 'SKBJH',
        name='_dr_pkzksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc'),
    )
    __tablename__CN__ = '排课助课数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JSGH = Column('JSGH', String(16), default='')  # 教师工号
    KCH = Column('KCH', String(16), default='')  # 课程号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KKXND = Column('KKXND', String(16), default='')  # 开课学年度
    SKBJH = Column('SKBJH', String(16), default='')  # 上课班级号
    KKXQM = Column('KKXQM', DateTime, default=now())  # 开课学期码
    ZXXS = Column('ZXXS', String(16), default='')  # 总学时
    ZKJHXS = Column('ZKJHXS', Float(16), default='')  # 助课计划学时
    SYZS = Column('SYZS', String(16), default='')  # 实验组数
    JXMSJBM = Column('JXMSJBM', String(16), default='')  # 教学名师级别码
    WYKCTJM = Column('WYKCTJM', String(16), default='')  # 外语课程调节码
    KCJBM = Column('KCJBM', String(16), default='')  # 课程级别码
    ZLXS = Column('ZLXS', String(16), default='')  # 质量系数
    HBS = Column('HBS', Float(16), default='')  # 合班数
    DWH = Column('DWH', String(16), default='')  # 单位号
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '教师工号': ['JSGH'],
            '课程号': ['KCH'],
            '教师姓名': ['JSXM'],
            '开课学年度': ['KKXND'],
            '上课班级号': ['SKBJH'],
            '开课学期码': ['KKXQM', 'DateTime'],
            '总学时': ['ZXXS'],
            '助课计划学时': ['ZKJHXS', 'Float'],
            '实验组数': ['SYZS'],
            '教学名师级别码': ['JXMSJBM'],
            '外语课程调节码': ['WYKCTJM'],
            '课程级别码': ['KCJBM'],
            '质量系数': ['ZLXS'],
            '合班数': ['HBS', 'Float'],
            '单位号': ['DWH'],
            '单位名称': ['DWMC'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['JSGH', 'KCH', 'KKXND', 'KKXQM', 'SKBJH']


class DR_SYPKSJXX(Base):  # 实验排课数据信息

    __tablename__ = 'dr_sypksjxx'  # 实验排课数据信息
    __table_args__ = (UniqueConstraint(
        'JSGH', 'KCH', 'KKXND', 'KKXQM',
        name='_dr_sypksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc'),
    )

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JSGH = Column('JSGH', String(16), default='')  # 教师工号
    KCH = Column('KCH', String(16), default='')  # 课程号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KKXND = Column('KKXND', String(16), default='')  # 开课学年度
    SKBJH = Column('SKBJH', String(16), default='')  # 上课班级号
    KKXQM = Column('KKXQM', DateTime, default=now())  # 开课学期码
    ZXXS = Column('ZXXS', String(16), default='')  # 总学时
    KCJBM = Column('KCJBM', String(16), default='')  # 课程级别码
    SYZS = Column('SYZS', Float(16), default='')  # 实验组数
    ZLXS = Column('ZLXS', String(16), default='')  # 质量系数
    HBS = Column('HBS', String(16), default='')  # 合班数
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '教师工号': ['JSGH'],
            '课程号': ['KCH'],
            '教师姓名': ['JSXM'],
            '开课学年度': ['KKXND'],
            '上课班级号': ['SKBJH'],
            '开课学期码': ['KKXQM', 'DateTime'],
            '总学时': ['ZXXS'],
            '课程级别码': ['KCJBM'],
            '实验组数': ['SYZS'],
            '质量系数': ['ZLXS'],
            '合班数': ['HBS'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['JSGH', 'KCH', 'KKXND', 'KKXQM', ]


class DR_SSPKSJXX(Base):  # 实习排课数据信息

    __tablename__ = 'dr_sspksjxx'  # 实习排课数据信息
    __table_args__ = (UniqueConstraint(
        'JSGH', 'KCH', 'KKXND', 'KKXQM',
        name='_dr_sspksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc'),
    )

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JSGH = Column('JSGH', String(16), default='')  # 教师工号
    KCH = Column('KCH', String(16), default='')  # 课程号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KKXND = Column('KKXND', String(16), default='')  # 开课学年度
    SKBJH = Column('SKBJH', String(16), default='')  # 上课班级号
    KKXQM = Column('KKXQM', DateTime, default=now())  # 开课学期码
    ZXXS = Column('ZXXS', String(16), default='')  # 总学时
    SXZS = Column('SXZS', Float(16), default='')  # 实习周数
    ZLXS = Column('ZLXS', String(16), default='')  # 质量系数
    HBS = Column('HBS', Float(16), default='')  # 合班数
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '教师工号': ['JSGH'],
            '课程号': ['KCH'],
            '教师姓名': ['JSXM'],
            '开课学年度': ['KKXND'],
            '上课班级号': ['SKBJH'],
            '开课学期码': ['KKXQM', 'DateTime'],
            '总学时': ['ZXXS'],
            '质量系数': ['ZLXS'],
            '合班数': ['HBS', 'Float'],
            '实习周数': ['SXZS', 'Float'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['JSGH', 'KCH', 'KKXND', 'KKXQM']


class DR_KCSJSJXX(Base):  # 课程设计数据信息

    __tablename__ = 'dr_kcsjsjxx'  # 课程设计数据信息
    __table_args__ = (UniqueConstraint(
        'JSGH', 'KCH', 'KKXND', 'KKXQM',
        name='_dr_kcsjsjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc'),
    )

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JSGH = Column('JSGH', String(16), default='')  # 教师工号
    KCH = Column('KCH', String(16), default='')  # 课程号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KKXND = Column('KKXND', String(16), default='')  # 开课学年度
    SKBJH = Column('SKBJH', String(16), default='')  # 上课班级号
    KKXQM = Column('KKXQM', DateTime, default=now())  # 开课学期码
    ZXXS = Column('ZXXS', String(16), default='')  # 总学时
    ZLXS = Column('ZLXS', String(16), default='')  # 质量系数
    SXZS = Column('SXZS', Float(16), default='')  # 课程设计周数
    HBS = Column('HBS', Float(16), default='')  # 合班数
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '教师工号': ['JSGH'],
            '课程号': ['KCH'],
            '教师姓名': ['JSXM'],
            '开课学年度': ['KKXND'],
            '上课班级号': ['SKBJH'],
            '开课学期码': ['KKXQM', 'DateTime'],
            '总学时': ['ZXXS'],
            '质量系数': ['ZLXS'],
            '合班数': ['HBS', 'Float'],
            '课程设计周数': ['SXZS', 'Float'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['JSGH', 'KCH', 'KKXND', 'KKXQM']


class DR_KCSJXX(Base):
    __tablename__ = 'dr_kcsjxx'
    __tablename__CH__ = '课程数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    KCH = Column('KCH', String(16), unique=True, default='')  # 课程号
    KCMC = Column('KCMC', String(16), default='')  # 课程名称
    ZXS = Column('ZXS', String(16), default='')  # 总学时
    LLXS = Column('LLXS', Float(16), default='')  # 理论学时
    SYXS = Column('SYXS', Float(16), default='')  # 实验学时
    SJXS = Column('SJXS', String(16), default='')  # 实践学时
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '教职工号': ['JZGH'],
            '课程号': ['KCH'],
            '课程名称': ['KCMC'],
            '总学时': ['ZXS'],
            '理论学时': ['LLXS', 'Float'],
            '实验学时': ['SYXS', 'Float'],
            '实践学时': ['SJXS'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['KCH']


class DR_XNXQXX(Base):
    __tablename__ = 'dr_xnxqxx'
    __tablename__CH__ = '学年学期信息'
    __table_args__ = (UniqueConstraint(
        'XNDM', 'XQDM', 'XQQSSJ',
        name='_dr_sypksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc'),
    )

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    XQMC = Column('XQMC', String(16), default='')  # 学期名称
    XQQSSJ = Column('XQQSSJ', DateTime, unique=True, default=now())  # 学期起始时间
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
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '学期名称': ['XQMC'],
            '教职工号': ['JZGH'],
            '学年学期名': ['XNXQM'],
            '学年代码': ['XNDM'],
            '学期代码': ['XQDM'],
            '学年名称': ['XNMC'],
            '起始上课周': ['QSSKZ'],
            '终止上课周': ['ZZSKZ'],
            '学期类型代码': ['XQLXDM'],
            '学期类型名称': ['XQLXMC'],
            '是否当前学期': ['SFDQXQ'],
            '学期起始时间': ['XQQSSJ', 'DateTime'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['XNDM', 'XQDM', 'XQQSSJ',]


class DR_BKS_JPKC(Base):
    __tablename__ = 'dr_bks_jpkc'
    __tablename__CH__ = '本科精品课程'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    KCH = Column('KCH', String(16), unique=True, default='')  # 课程号
    KCMC = Column('KCMC', String(16), default='')  # 课程名称
    KCJBM = Column('KCJBM', String(16), default='')  # 课程级别码
    FZRGH = Column('FZRGH', String(16), default='')  # 负责人工号
    FZRXM = Column('FZRXM', String(16), default='')  # 负责人姓名
    DWH = Column('DWH', String(16), default='')  # 单位号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '课程号': ['KCH'],
            '课程名称': ['KCMC'],
            '课程级别码': ['KCJBM'],
            '负责人工号': ['FZRGH'],
            '负责人姓名': ['FZRXM'],
            '单位号': ['DWH'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['KCH']


class DR_KSAPXX(Base):
    '''
KSRQ     考试日期 C  教务处、研究生院
KSSC     考试时长 N  教务处、研究生院
KSFSLXM  考试方式类型码 C(1) JX_KSFS 考试方式代码 教务处、研究生院
KCH      课程号 C  教务处、研究生院
JKRGH    监考人工号 C(8)  教务处、研究生院
KSJSH    考试教室号 C  教务处、研究生院
JKRXM    监考人姓名 C  教务处、研究生院
KSRS     考试人数 N  教务处、研究生院
    '''

    __tablename__ = 'dr_ksapxx'
    __tablename__CN__ = '考试安排信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    KSRQ = Column('KSRQ', DateTime, default=now())  # 考试日期
    KSSC = Column('KSSC', Float(16), default='')  # 考试时长
    KSFSLXM = Column('KSFSLXM', String(16), default='')  # 考试方式类型码
    KCH = Column('KCH', String(16), default='')  # 课程号
    JKRGH = Column('JKRGH', String(16), default='')  # 监考人工号
    KSJSH = Column('KSJSH', String(16), default='')  # 考试教室号
    JKRXM = Column('JKRXM', String(16), default='')  # 监考人姓名
    KSRS = Column('KSRS', String(16), default='')  # 考试人数
    SSXY = Column('SSXY', String(16), default='')  # 本次考试所属学院
    JSSSXY = Column('JSSSXY', String(16), default='')  # 教师所属学院

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
            '考试日期': ['KSRQ', 'DateTime'],
            '考试时长': ['KSSC', 'Flaot'],
            '考试方式类型码': ['KSFSLXM'],
            '课程号': ['KCH'],
            '监考人工号': ['JKRGH'],
            '考试教室号': ['KSJSH'],
            '监考人姓名': ['JKRXM'],
            '考试人数': ['KSRS'],
            '本次考试所属学院': ['SSXY'],
            '教师所属学院': ['JSSSXY'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['KCH','KSRQ','KSJSH','SSXY']


class DR_XWLWXX(Base):
    '''
LWTM 论文题目 C  教务处、研究生院
LWQSRQ 论文起始日期 C  教务处、研究生院
LWZZRQ 论文终止日期 C  教务处、研究生院
XH 学号 C(8)  教务处、研究生院
    '''

    __tablename__ = 'dr_xwlwxx'
    __tablename__CN__ = '学位论文信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    LWTM = Column('LWTM', String(16), default='')  # 论文题目
    LWQSRQ = Column('LWQSRQ', DateTime, default=now())  # 论文起始日期
    LWZZRQ = Column('LWZZRQ', DateTime, default=now())  # 论文终止日期
    XH = Column('XH', String(16), default='')  # 学号
    XSXM = Column('XSXM', String(16), default='')  # 学生姓名
    XSSSXY = Column('XSSSXY', String(16), default='')  # 所属学院

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
            '论文题目': ['LWTM'],
            '论文起始日期': ['LWQSRQ', 'DateTime'],
            '论文终止日期': ['LWZZRQ', 'DateTime'],
            '学号': ['XH'],
            '学生姓名': ['XSXM'],
            '所属学院': ['XSSSXY'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['LWTM','XH']


class DR_ZDBYLWSJXX(Base):  # 指导毕业论文数据信息

    __tablename__ = 'dr_zdbylwsjxx'  # 指导毕业论文数据信息
    __tablename__CN__ = '指导毕业论文数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注
    JZGH = Column('JZGH', String(16), default='')  # 教师工号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    ZDZS = Column('ZDZS', Float(16), default='')  # 指导周数
    XQ = Column('XQ', DateTime, default=now())  # 指导学期
    ZDPTXSS = Column('ZDPTXSS', Float(16), default='')  # 指导普通学生数
    ZDSYXSS = Column('ZDSYXSS', Float(16), default='')  # 指导双语学生数
    JXMSJBM = Column('JXMSJBM', String(16), default='')  # 教学名师级别码

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
            '教师工号': ['JZGH'],
            '教师姓名': ['JSXM'],
            '指导周数': ['ZDZS', 'Float'],
            '指导普通学生数': ['ZDPTXSS', 'Float'],
            '指导双语学生数': ['ZDSYXSS', 'Float'],
            '教学名师级别码': ['JXMSJBM'],
            '指导学期': ['XQ', 'DateTime'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['JZGH','JXMSJBM']


class DR_JZGJCSJXX(Base):
    __tablename__ = 'dr_jzgjcsjxx'
    __tablename__CH__ = '教职工基础数据信息'

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
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '教职工号': ['JZGH'],
            '单位号': ['DWH'],
            '姓名': ['XM'],
            '英文姓名': ['YWXM'],
            '姓名拼音': ['XMPY'],
            '曾用名': ['CYM'],
            '性别码': ['XBM'],
            '出生日期': ['CSRQ', 'DateTime'],
            '出生地码': ['CSDM'],
            '编制类别码': ['BZLBM'],
            '教职工类别码': ['JZGLBM'],
            '当前状态码': ['DQZTM'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['JZGH']


class DR_XMJFXX(Base):
    __tablename__ = 'dr_xmjfxx'
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
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '计划经费总额': ['JHJFZE', 'Float'],
            '项目经费来源码': ['XMJFLYM'],
            '拨入日期': ['BRRQ', 'DateTime'],
            '拨款数': ['BKS', 'Float'],
            '支出日期': ['ZCRQ', 'DateTime'],
            '拨付协作单位经费': ['BFXZDWJF'],
            '项目凭证编号': ['XMPZBH'],
            '经办人姓名': ['JBRXM'],
            '项目编号': ['XMBH'],
            '支出款数': ['ZZKS', 'Float'],
            '教职工号': ['JZGH'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['XMBH']


# yangchen
class DR_HJCGJBSJXX(Base):
    __tablename__ = 'dr_hjcgjbsjxx'
    __tablename__CH__ = '获奖成果基本数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    HJCGBH = Column('HJCGBH', String(16), unique=True, default='')  # 获奖成果编号
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
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '获奖成果编号': ['HJCGBH'],
            '获奖成果名称': ['HJCGMC'],
            '项目来源码': ['XMLYM'],
            '单位号': ['DWH'],
            '获奖日期': ['HJRQ', 'DateTime'],
            '成果获奖类别码': ['CGHJLBM'],
            '科技奖类别': ['KJJLB'],
            '奖励等级码': ['JLDJM'],
            '获奖级别码': ['HJJBM'],
            '学科领域': ['XKLYM'],
            '颁奖单位': ['BJDW'],
            '所属项目编号': ['SSXMBH'],
            '单位排名': ['DWPM'],
            '学科门类(科技)码': ['XKMLKJM'],
            '负责人员号': ['FZRYH'],
            '负责人姓名': ['FZRXM'],
            '一级学科': ['YJXK'],
            '单位名称': ['DWMC'],
            '研究所名称': ['YJSMC'],
            '成果形式': ['CGXS'],
            '获奖名称': ['HJMC'],
            '获奖编号': ['HJBH'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['HJCGBH', 'HJCGMC']


#yangchen
class DR_KJCGRYXX_JL(Base):
    __tablename__ = 'dr_kjcgryxx_jl'
    __tablename__CH__ = '科技成果(获奖成果)人员信息'
    __table_args__ = (UniqueConstraint('RYH', 'HJCGBH', name='_dr_kjcgryxx_jl_ryh_hjcgbh_uc'),)

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    RYH = Column('RYH', String(16), default='')  # 人员号
    JSM = Column('JSM', String(16), default='')  # 角色码
    ZXZS = Column('ZXZS', String(16), default='')  # 撰写字数
    PMZRS = Column('PMZRS', String(16), default='')  # 排名/总人数
    GXL = Column('GXL', Float, default=0.0)  # 贡献率
    XM = Column('XM', String(16), default='')  # 姓名
    SZDW = Column('SZDW', String(16), default='')  # 所在单位
    RYLX = Column('RYLX', String(16), default='')  # 人员类型
    HJCGBH = Column('HJCGBH', String(16), default='')  # 获奖成果编号
    KJCGRYBH = Column('KJCGRYBH', String(16), default='')  # 科技成果人员编号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '人员号': ['RYH'],
            '角色码': ['JSM'],
            '撰写字数': ['ZXZS'],
            '排名/总人数': ['PMZRS'],
            '贡献率': ['GXL'],
            '姓名': ['XM'],
            '所在单位': ['SZDW'],
            '人员类型': ['RYLX'],
            '获奖成果编号': ['HJCGBH'],
            '科技成果人员编号': ['KJCGRYBH'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['RYH', 'HJCGBH']


#zouyang
class DR_KJQKLWJBSJXX(Base):
    __tablename__ = 'dr_kjqklwjbsjxx'
    __tablename__CH__ = '科技期刊论文基本数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    LWBH= Column('LWBH', String(16), default='')  # 论文编号
    LWMC = Column('LWMC', String(128),default='')  # 论文名称
    DWH = Column('DWH', String(16), default='')  # 单位号
    LWLXM = Column('LWLXM', String(16), default='')  # 论文类型码
    LZLBM = Column('LZLBM', String(16), default='')  # 论著类别码
    XKLYM = Column('XKLYM', String(16), default='')  # 学科领域
    XKMLKJM = Column('XKMLKJM', String(16), default='')  # 学科门类(科技)码
    XMLYM = Column('XMLYM', String(16), default='')  # 项目来源码
    ZGYZM = Column('ZGYZM', String(16), default='')  # 中国语种码
    YZM = Column('YZM', String(16), default='')  # 语种码
    SSXMBH = Column('SSXMBH', String(16), default='')  # 所属项目编号
    SSJSLY = Column('SSJSLY', String(16), default='')  # 所属技术领域
    LZSLQKM = Column('LZSLQKM', String(16), default='')  # 论著收录情况码
    QTSLQK = Column('QTSLQK', String(16), default='')  # 其他收录情况
    DYZZ = Column('DYZZ', String(16), default='')  # 第一作者
    DYZZBH = Column('DYZZBH', String(16), default='')  # 第一作者编号
    XXSM = Column('XXSM', String(16), default='')  # 学校署名
    YJXK = Column('YJXK', String(16), default='')  # 一级学科
    CYRY = Column('CYRY', String(128), default='')  # 参与人员
    TXZZ= Column('TXZZ', String(16), default='')  # 通讯作者
    JSQK = Column('JSQK', String(128),  default='')  # 检索情况
    JQY = Column('JQY', String(128),  default='')  # 卷期页
    WDWZZPX = Column('WDWZZPX', String(16), default='')  # 外单位作者排序
    BZXYBJZDSYS = Column('BZXYBJZDSYS', String(16), default='') # 标注学院部级重点实验室
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '论文编号': ['LWBH'],
            '论文名称': ['LWMC'],
            '单位号': ['DWH'],
            '论文类型码': ['LWLXM'],
            '论著类别码': ['LZLBM'],
            '学科领域': ['XKLYM'],
            '学科门类(科技)码': ['XKMLKJM'],
            '项目来源码': ['XMLYM'],
            '中国语种码': ['ZGYZM'],
            '语种码': ['YZM'],
            '所属项目编号': ['SSXMBH'],
            '所属技术领域': ['SSJSLY'],
            '论著收录情况码': ['LZSLQKM'],
            '其他收录情况': ['QTSLQK'],
            '第一作者': ['DYZZ'],
            '第一作者编号': ['DYZZBH'],
            '学校署名': ['XXSM'],
            '一级学科': ['YJXK'],
            '参与人员': ['CYRY'],
            '通讯作者': ['TXZZ'],
            '检索情况': ['JSQK'],
            '卷期页': ['JQY'],
            '外单位作者排序': ['WDWZZPX'],
            '标注学院部级重点实验室': ['BZXYBJZDSYS'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['LWBH']


#zouyang
class DR_KJLWFBXX(Base):
    __tablename__ = 'dr_kjlwfbxx'
    __tablename__CH__ = '科技论文发表信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    KWMC = Column('KWMC', String(16), default='')  # 刊物名称
    LWBH = Column('LWBH', String(16), default='')  # 论文编号
    FBRQ = Column('FBRQ', DateTime, default=now())  # 发表日期
    JH = Column('JH', String(16), default='')  # 卷号
    QH = Column('QH', String(16), default='')  # 期号
    LRSJ = Column('LRSJ', DateTime, default=now())  # 录入时间
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '刊物名称': ['KWMC'],
            '论文编号': ['LWBH'],
            '发表日期': ['FBRQ', 'DateTime'],
            '卷号': ['JH'],
            '期号': ['QH'],
            '录入时间': ['LRSJ ', 'DateTime'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['LWBH']


#zouyang
class DR_KJCGRYXX_LW(Base):  # 科技成果(论文)人员信息

    __tablename__ = 'dr_kjcgryxx_lw'  # 科技成果(论文)人员信息

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    RYH = Column('RYH', String(16), default='')  # 人员号
    JSM = Column('JSM', String(16), default='')  # 角色码
    ZXZS= Column('ZXZS', String(16), default='')  # 撰写字数
    PMZRS= Column('PMZRS', String(16), default='')  # 排名/总人数
    GXL = Column('GXL', Float, default=0.0)  # 贡献率
    XM= Column('XM', String(16), default='')  # 姓名
    SZDW = Column('SZDW', String(16), default='')  # 所在单位
    RYLX = Column('RYLX', String(16), default='')  # 人员类型
    LWBH = Column('LWBH', String(16), default='')  # 论文编号
    KJCGRYBH = Column('KJCGRYBH', String(16), default='')  # 科技成果人员编号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '人员号': ['RYH'],
            '角色码': ['JSM'],
            '撰写字数': ['ZXZS'],
            '排名/总人数': ['PMZRS'],
            '贡献率': ['GXL'],
            '姓名': ['XM'],
            '所在单位': ['SZDW'],
            '人员类型': ['RYLX'],
            '论文编号': ['LWBH'],
            '科技成果人员编号': ['KJCGRYBH'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['LWBH']


#zouyang
class DR_KJLWSLQK(Base):  # 科技论文收录情况

    __tablename__ = 'dr_kjlwslqk'  # 科技论文收录情况

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    LWBH = Column('LWBH', String(16), default='')  # 论文编号
    SLLX = Column('SLLX', String(16), default='')  # 收录类型
    SLBH = Column('SLBH', String(16), default='')  # 收录编号
    SLSJ = Column('SLSJ', String(16), default='')  # 收录时间
    SLQH = Column('SLQH', String(16), default='')  # 收录区号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '论文编号': ['LWBH'],
            '收录类型': ['SLLX'],
            '收录编号': ['SLBH'],
            '收录时间': ['SLSJ'],
            '收录区号': ['SLQH'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['LWBH']


#yangchen
class DR_ZLCGJBSJXX(Base):
    __tablename__ = 'dr_zlcgjbsjxx'
    __tablename__CH__ = '专利成果基本数据信息'
    __table_args__ = (UniqueConstraint('ZLCGBH', 'SQBH', name='_dr_zlcgjbsjxx_zlcgbh_sqbh_uc'),)

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
    ZLZZRQ = Column('ZLZZRQ', DateTime(16), default=now())  # 专利终止日期
    XKMLKJM = Column('XKMLKJM', String(16), default='')  # 学科门类(科技)码
    ZLSQRQ = Column('ZLSQRQ', String(16), default='')  # 专利申请日期
    ZZM = Column('ZZM', String(16), default='')  # 作者名
    ZZBH = Column('ZZBH', String(16), default='')  # 作者编号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '专利成果编号': ['ZLCGBH'],
            '专利成果名称': ['ZLCGMC'],
            '单位号': ['DWH'],
            '申请编号': ['SQBH'],
            '学科领域': ['XKLYM'],
            '专利类型码': ['ZLLXM'],
            '批准日期': ['PZRQ', 'DateTime'],
            '批准形式码': ['PZXSM'],
            '专利证书编号': ['ZLZSBH'],
            '法律状态码': ['FLZTM'],
            '交纳专利年费日期': ['JNZLNFRQ'],
            '交纳金额': ['JNJE'],
            '所属项目编号': ['SSXMBH'],
            '国籍/地区码': ['GJDQM'],
            '国际专利主分类号': ['GJZLZFLH'],
            'PCT 或专利国家/地区码': ['PCTHZLGJDQM'],
            '授权公告号': ['SQGGH'],
            '授权公告日期': ['SQGGRQ', 'DateTime'],
            '申请名称': ['SQMC'],
            '专利代理机构': ['ZLDLJG'],
            '专利代理人': ['ZLDLR'],
            '专利权人': ['ZLQR'],
            '专利终止日期': ['ZLZZRQ'],
            '学科门类(科技)码': ['XKMLKJM'],
            '专利申请日期': ['ZLSQRQ', 'DateTime'],
            '作者名': ['ZZM'],
            '作者编号': ['ZZBH'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['ZLCGBH', 'SQBH']


#yangchen
class DR_ZLCSXX(Base):
    __tablename__ = 'dr_zlcsxx'
    __tablename__CH__ = '专利出售信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False) # ID
    CSRQ = Column('CSRQ', DateTime, default=now())  # 出售日期
    CSJE = Column('CSJE', Float, default=0.0)  # 出售金额
    SSDW = Column('SSDW', String(16), default='')  # 受售单位
    GJDQM = Column('GJDQM', String(16), default='')  # 国籍/地区码
    BNSJSR = Column('BNSJSR', Float, default=0.0)  # 本年实际收入
    XKMLKJM = Column('XKMLKJM', String(16), default='')  # 学科门类(科技)码
    ZLCGBH = Column('ZLCGBH', String(16), default='')  # 专利成果编号
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '出售日期': ['CSRQ', 'DateTime'],
            '出售金额': ['CSJE'],
            '受售单位': ['SSDW'],
            '国籍/地区码': ['GJDQM'],
            '本年实际收入': ['BNSJSR'],
            '学科门类(科技)码': ['XKMLKJM'],
            '专利成果编号': ['ZLCGBH', 'DateTime'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['ZLCGBH']


#yangchen
class DR_KJCGRYXX_ZL(Base):
    __tablename__ = 'dr_kjcgryxx_zl'
    __tablename__CH__ = '科技成果(专利)人员信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    RYH = Column('RYH', String(16), default='')  # 人员号
    JSM = Column('JSM', String(16), default='')  # 角色码
    ZXZS = Column('ZXZS', String(16), default='')  # 撰写字数
    PMZRS = Column('PMZRS', String(16), default='')  # 排名/总人数
    GXL = Column('GXL', Float, default=0.0)  # 贡献率
    XM = Column('XM', String(16), default='')  # 姓名
    SZDW = Column('SZDW', String(16), default='')  # 所在单位
    RYLX = Column('RYLX', String(16), default='')  # 人员类型
    ZLCGBH = Column('ZLCGBH', String(16), default='')  # 专利成果编号
    KJCGRYBH = Column('KJCGRYBH', String(16), default='')  # 科技成果人员编号
    SMSX = Column('SMSX', String(16), default='')  # 署名顺序
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '人员号': ['RYH'],
            '角色码': ['JSM'],
            '撰写字数': ['ZXZS'],
            '排名/总人数': ['PMZRS'],
            '贡献率': ['GXL'],
            '姓名': ['XM'],
            '所在单位': ['SZDW'],
            '人员类型': ['RYLX'],
            '专利成果编号': ['ZLCGBH'],
            '科技成果人员编号': ['KJCGRYBH'],
            '署名顺序': ['SMSX'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['ZLCGBH']


# fanmingreviveagain 项目人员信息表
class DR_XMRYXX(Base):
    __tablename__ = 'dr_xmryxx'
    __tablename__CH__ = '项目人员信息'
    __table_args__ = (
        UniqueConstraint('XMBH', 'RYH', name='_dr_xmryxx_xmbh_ryh_uc'),
        {'extend_existing': True},
    )

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    RYH = Column('RYH', String(16), default='')  # 人员号
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
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '人员号': ['RYH'],
            '工作量': ['GZL', 'Float'],
            '每年工作月数': ['MNGZYS', 'Float'],
            '角色码': ['JSM'],
            '人员类型': ['RYLX'],
            '署名顺序': ['SMSX'],
            '项目编号': ['XMBH'],
            '学科门类(科技)码': ['XKMLKJM'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['XMBH', 'RYH']
# fanmingdieatlast


class DR_JCJBSJXX(Base):
    __tablename__ = 'dr_jcjbsjxx'
    __tablename__CH__ = '教材基本数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    CBH = Column('CBH', String(16), default='')  # 出版号
    JCMC = Column('JCMC', String(16), default='')  # 教材名称
    BC = Column('BC', String(16), default='')  # 版次
    DWH = Column('DWH', String(16), default='')  # 单位号
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    CBS = Column('CBS', String(16), default='')  # 出版社
    BZZZS = Column('BZZZS', String(16), default='')  # 编著者总数
    CBRQ = Column('CBRQ', DateTime, default=now())  # 出版日期
    JCBH = Column('JCBH', String(16), default='')  # 教材编号
    JCLB = Column('JCLB', String(16), default='')  # 教材类别
    JCZS = Column('JCZS', String(16), default='')  # 教材字数
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注


    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '出版号': ['CBH'],
            '教材名称': ['JCMC'],
            '版次': ['BC'],
            '单位号': ['DWH'],
            '单位名称': ['DWMC'],
            '出版社': ['CBS'],
            '编著者总数': ['BZZZS'],
            '出版日期': ['CBRQ', 'DateTime'],
            '教材编号': ['JCBH'],
            '教材类别': ['JCLB'],
            '教材字数': ['JCZS'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['JCBH']


class DR_HJJCXX(Base):
    __tablename__ = 'dr_hjjcxx'
    __tablename__CH__ = '获奖教材信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    HJJCBH = Column('HJJCBH', String(16), default='')  # 获奖教材编号
    HJXM = Column('HJXM', String(16), default='')  # 获奖项目
    HJJC = Column('HJJC', String(16), default='')  # 获奖届次
    HJRQ = Column('HJRQ', DateTime, default=now())  # 获奖日期
    HJMC = Column('HJMC', String(16), default='')  # 获奖名称
    JLJBM = Column('JLJBM', String(16), default='')  # 奖励级别码
    JLDJM = Column('JLDJM', String(16), default='')  # 奖励等级码
    BJDW = Column('BJDW', String(16), default='')  # 颁奖单位
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '获奖教材编号': ['HJJCBH'],
            '获奖项目': ['HJXM'],
            '获奖届次': ['HJJC'],
            '获奖日期': ['HJRQ', 'DateTime'],
            '获奖名称': ['HJMC'],
            '奖励级别码': ['JLJBM'],
            '奖励等级码': ['JLDJM'],
            '颁奖单位': ['BJDW'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['HJJCBH']

    class DR_BZXX(Base):
        __tablename__ = 'dr_bzxx'
        __tablename__CH__ = '教材编者信息'

        id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
        BZZH = Column('BZZH', String(16), default='')  # 编著者号
        BZZXM = Column('BZZXM', String(16), default='')  # 编著者姓名
        BZZJSM = Column('BZZJSM', String(16), default='')  # 编著者角色码
        BZZDW = Column('BZZDW', String(16), default='')  # 编著者单位
        JCBH = Column('JCBH', String(16), default='')  # 教材编号
        stamp = Column('stamp', DateTime, default=now())  # 时间戳
        note = Column('note', String(1024), default='')  # 备注

        @staticmethod
        def get_column_label() -> dict:
            return {
                'ID': ['id'],
                '编著者号': ['BZZH'],
                '编著者姓名': ['BZZXM'],
                '编著者角色码': ['BZZJSM'],
                '编著者单位': ['BZZDW'],
                '教材编号': ['JCBH'],
                '时间戳': ['stamp', 'DateTime'],
                '备注': ['note'],
            }

        @staticmethod
        def get_unique_condition() -> []:
            return ['JCBH']

class DR_KJZZXX(Base):
    __tablename__ = 'dr_kjzzxx'
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
    DWMC = Column('DWMC', String(16), default='')  # 单位名称
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '著作编号': ['ZZBH'],
            '著作名称': ['ZZMC'],
            '单位号': ['DWH'],
            '出版日期': ['CBRQ', 'DateTime'],
            '论著类别码': ['LZLBM'],
            '出版社': ['CBS'],
            '出版社级别码': ['CBSJBM'],
            '出版号': ['CBH'],
            '著作字数': ['ZZZS'],
            'ISBN号': ['ISBNH'],
            '第一作者': ['DYZZ'],
            '第一作者编号': ['DYZZBH'],
            '单位名称': ['DWMC'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['ZZBH']

class DR_KJCGRYXX_ZZ(Base):
    __tablename__ = 'dr_kjcgryxx_zz'
    __tablename__CH__ = '科技成果(著作)人员信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    RYH = Column('RYH', String(16), default='')  # 人员号
    JSM = Column('JSM', String(16), default='')  # 角色码
    ZXZS = Column('ZXZS', Integer, default=0)  # 撰写字数
    PMZRS = Column('PMZRS', String(16), default='')  # 排名/总人数
    GXL = Column('GXL', String(16), default='')  # 贡献率
    XM = Column('XM', String(16), default='')  # 姓名
    DWH = Column('DWH', String(16), default='')  # 单位号
    SZDW = Column('SZDW', String(16), default='')  # 所在单位
    ZZBH = Column('ZZBH', Integer, default=0)  # 著作编号
    KJCGRYBH = Column('KJCGRYBH', String(16), default='')  # 科技成果人员编号
    SMSX = Column('SMSX', Integer, default=0)  # 署名顺序
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '人员号': ['RYH'],
            '角色码': ['JSM'],
            '撰写字数': ['ZXZS'],
            '排名/总人数': ['PMZRS'],
            '贡献率': ['GXL'],
            '姓名': ['XM'],
            '单位号': ['DWH'],
            '所在单位': ['SZDW'],
            '著作编号': ['ZZBH'],
            '科技成果人员编号': ['KJCGRYBH'],
            '署名顺序': ['SMSX'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['ZZBH']


class DR_XJJBSJXX(Base):
    __tablename__ = 'dr_xjjbsjxx'
    __tablename__CH__ = '学籍基本数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    RXNY = Column('RXNY', String(16), default='')  # 入学年月
    XSLBM = Column('XSLBM', String(16), default='')  # 学生类别码
    SZBH = Column('SZBH', String(16), default='')  # 所在班号
    SZNJ = Column('SZNJ', String(16), default='')  # 所在年级
    YXSH = Column('YXSH', String(16), default='')  # 院系所号
    DWH = Column('DWH', String(16), default='')  # 单位号
    SZDW = Column('SZDW', String(16), default='')  # 所在单位
    ZYM = Column('ZYM', String(16), default='')  # 专业码
    XKMLM = Column('XKMLM', String(16), default='')  # 学科门类码
    PYFSM = Column('PYFSM', String(16), default='')  # 培养方式码
    YJFX = Column('YJFX', String(16), default='')  # 研究方向
    DSXM = Column('DSXM', String(16), default='')  # 导师姓名
    DSH = Column('DSH', String(16), default='')  # 导师号
    HDXLFSM = Column('HDXLFSM', String(16), default='')  # 获得学历方式码
    SFXFZ = Column('SFXFZ', String(16), default='')  # 是否学分制
    PYCCM = Column('PYCCM', String(16), default='')  # 培养层次码
    LDFS = Column('LDFS', String(16), default='')  # 连读方式
    XSDQZTM = Column('XSDQZTM', String(16), default='')  # 学生当前状态码
    XH = Column('XH', String(16), default='')  # 学号
    XZ = Column('XZ', String(16), default='')  # 学制
    XJBH = Column('XJBH', String(16), default='')  # 学籍编号
    XXGXRQ = Column('XXGXRQ', DateTime, default=now())  # 信息更新日期
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '入学年月': ['RXNY'],
            '学生类别码': ['XSLBM'],
            '所在班号': ['SZBH'],
            '所在年级': ['SZNJ'],
            '院系所号': ['YXSH'],
            '单位号': ['DWH'],
            '所在单位': ['SZDW'],
            '专业码': ['ZYM'],
            '学科门类码': ['XKMLM'],
            '培养方式码': ['PYFSM'],
            '研究方向': ['YJFX'],
            '导师姓名': ['DSXM'],
            '导师号': ['DSH'],
            '获得学历方式码': ['HDXLFSM'],
            '是否学分制': ['SFXFZ'],
            '培养层次码': ['PYCCM'],
            '连读方式': ['LDFS'],
            '学生当前状态码': ['XSDQZTM'],
            '学号': ['XH'],
            '学制': ['XZ'],
            '学籍编号': ['XJBH'],
            '信息更新日期': ['XXGXRQ', 'DateTime'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['XH']

class DR_YJSDSXX(Base):
    __tablename__ = 'dr_yjsdsxx'
    __tablename__CH__ = '研究生导师信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JZGH = Column('JZGH', String(16), default='')  # 教职工号
    DSLBM = Column('DSLBM', String(16), default='')  # 导师类别码
    RDSNY = Column('RDSNY', String(16), default='')  # 任导师年月
    XWSYDWM = Column('XWSYDWM', String(16), default='')  # 学位授予单位码
    DWMC = Column('DWMC', String(16), default='')  # 人事归属单位名称
    WYZJ = Column('WYZJ', String(16), default='')  # 唯一主键
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '教职工号': ['JZGH'],
            '导师类别码': ['DSLBM'],
            '任导师年月': ['RDSNY'],
            '学位授予单位码': ['XWSYDWM'],
            '人事归属单位名称': ['DWMC'],
            '唯一主键': ['WYZJ'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['JZGH']



class DR_JGXMXX(Base):
    __tablename__ = 'dr_jgxmxx'
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
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '单位号': ['DWH'],
            '教职工号': ['JZGH'],
            '教职工姓名': ['JZGXM'],
            '贡献率': ['GXL'],
            '年度': ['ND'],
            '项目序号': ['XMXH'],
            '项目编号': ['XMBH'],
            '项目名称': ['XMMC'],
            '项目负责人号': ['XMFZRH'],
            '姓名': ['XM'],
            '立项日期': ['LXRQ', 'DateTime'],
            '批准经费': ['PZJF'],
            '项目级别码': ['XMJBM'],
            '角色类型码': ['JSLXM'],
            '数据来源': ['SJLYM'],
            '项目级别': ['XMJB'],
            '参与人次': ['CYRC'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['XMBH']


class_dict = {key: var for key, var in locals().items() if isinstance(var, type)}


if __name__ == '__main__':

    try:
        Base.metadata.create_all(engine)
    except Error as e:
        print(e)

    exit(0)
