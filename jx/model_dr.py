# coding=utf-8
# 定义导入数据模型，与东大校标一致; 可自动运行建表，字段变化后需要手工写SQL调整

from jx.sqlalchemy_env import *


class DR_ZZJGJBSJXX(Base):  # 组织机构基本数据信息

    __tablename__ = 'dr_zzjgjbsjxx'  # 组织机构基本数据信息

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


class DR_PKSJXX(Base):  # 排课数据信息

    __tablename__ = 'dr_pksjxx'  # 排课数据信息
    __table_args__ = (UniqueConstraint(
        'JSGH', 'KCH', 'KKXND', 'KKXQM', 'SKBJH',
        name='_dr_pksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc'),
    )

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JSGH = Column('JSGH', String(16), default='')  # 教师工号
    KCH = Column('KCH', String(16), default='')  # 课程号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KKXND = Column('KKXND', String(16), default='')  # 开课学年度
    SKBJH = Column('SKBJH', String(16), default='')  # 上课班级号
    KKXQM = Column('KKXQM', String(16), default='')  # 开课学期码
    ZXXS = Column('ZXXS', String(16), default='')  # 总学时
    ZKJHXS = Column('ZKJHXS', String(16), default='')  # 助课计划学时
    JXMSJBM = Column('JXMSJBM', String(16), default='')  # 教学名师级别码
    WYKCTJM = Column('WYKCTJM', String(16), default='')  # 外语课程调节码
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
            '开课学期码': ['KKXQM'],
            '总学时': ['ZXXS'],
            '助课计划学时': ['ZKJHXS'],
            '教学名师级别码': ['JXMSJBM'],
            '外语课程调节码': ['WYKCTJM'],
            '质量系数': ['ZLXS'],
            '合班数': ['HBS '],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['JSGH', 'KCH', 'KKXND', 'KKXQM', 'SKBJH']


class DR_KCSJXX(Base):  # 课程数据信息

    __tablename__ = 'dr_kcsjxx'  # 课程数据信息

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    KCH = Column('KCH', String(16), unique=True, default='')  # 课程号
    KCMC = Column('KCMC', String(16), default='')  # 课程名称
    ZXS = Column('ZXS', String(16), default='')  # 总学时
    LLXS = Column('LLXS', String(16), default='')  # 理论学时
    SYXS = Column('SYXS', String(16), default='')  # 实验学时
    SJXS = Column('SJXS', String(16), default='')  # 实践学时
    stamp = Column('stamp', DateTime, default=now())  # 时间戳
    note = Column('note', String(1024), default='')  # 备注

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '课程号': ['KCH'],
            '课程名称': ['KCMC'],
            '总学时': ['ZXS'],
            '理论学时': ['LLXS'],
            '实验学时': ['SYXS'],
            '实践学时': ['SJXS'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['KCH']


class DR_XNXQXX(Base):  # 学年学期信息

    __tablename__ = 'dr_xnxqxx'  # 学年学期信息

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    XQMC = Column('XQMC', String(16), unique=True, default='')  # 学期名称
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
            '学年学期名': ['XNXQM'],
            '学年代码': ['XNDM'],
            '学期代码': ['XQDM'],
            '学年名称': ['XNMC'],
            '起始上课周': ['QSSKZ'],
            '终止上课周': ['ZZSKZ'],
            '学期类型代码': ['XQLXDM'],
            '学期类型名称': ['XQLXMC'],
            '是否当前学期': ['SFDQXQ'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['XNXQM']


class DR_BKS_JPKC(Base):  # 本科精品课程

    __tablename__ = 'dr_bks_jpkc'  # 本科精品课程

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    KCH = Column('KCH', String(16), unique=True, default='')  # 课程号
    KCMC = Column('KCMC', String(16), default='')  # 课程名称
    KCJBM = Column('KCJBM', String(16), default='')  # 课程级别码
    FZRGH = Column('FZRGH', String(16), default='')  # 负责人工号
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
            '单位号': ['DWH'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['KCH']


class DR_JZGJCSJXX(Base):  # 教职工基础数据信息

    __tablename__ = 'dr_jzgjcsjxx'  # 教职工基础数据信息

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


class DR_XMJFXX(Base):  # 项目经费信息

    __tablename__ = 'dr_xmjfxx'  # 项目经费信息

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


"""
ALTER TABLE DR_ZZJGJBSJXX ADD stamp TIMESTAMP(6);
ALTER TABLE DR_JZGJCSJXX ADD stamp TIMESTAMP(6);
ALTER TABLE DR_XMJFXX ADD stamp TIMESTAMP(6);
ALTER TABLE DR_PKSJXX ADD stamp TIMESTAMP(6);
ALTER TABLE DR_KCSJXX ADD stamp TIMESTAMP(6);
ALTER TABLE DR_XNXQXX ADD stamp TIMESTAMP(6);
ALTER TABLE DR_BKS_JPKC ADD stamp TIMESTAMP(6);
"""


# yangchen
class DR_HJCGJBSJXX(Base):  # 获奖成果基本数据信息

    __tablename__ = 'dr_hjcgjbsjxx'  # 获奖成果基本数据信息

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    HJCGBH = Column('HJCGBH', String(16), unique=True, default='')  # 获奖成果编号
    HJCGMC = Column('HJCGMC', String(16), unique=True, default='')  # 获奖成果名称
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
        # TODO: individual unique condition OR combined
        return ['HJCGBH', 'HJCGMC']


class DR_KJCGRYXX_JL(Base):
    __tablename__ = 'dr_kjcgryxx_jl'  # 科技成果(获奖成果)人员信息

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
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['RYH']


class DR_KJQKLWJBSJXX(Base):  # 科技期刊论文基本数据信息

    __tablename__ = 'dr_kjqklwjbsjxx'  # 科技期刊论文基本数据信息

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    LWBH= Column('LWBH', String(16), default='')  # 论文编号
    LWMC = Column('LWMC', String(128), unique=True, default='')  # 论文名称
    LWLXM= Column('LWLXM', String(16), default='')  # 论文类型码
    DYZZ= Column('DYZZ', String(16), default='')  # 第一作者
    CYRY = Column('CYRY', String(128), unique=True, default='')  # 参与人员
    TXZZ= Column('TXZZ', String(16), default='')  # 通讯作者
    JSQK = Column('JSQK', String(128), unique=True, default='')  # 检索情况
    JQY = Column('JQY', String(128), unique=True, default='')  # 卷期页
    WDWZZPX = Column('WDWZZPX', String(16), default='')  # 外单位作者排序
    BZXYBJZDSYS = Column('BZXYBJZDSYS', String(16), default='') # 标注学院部级重点实验室

    @staticmethod
    def get_column_label() -> dict:
        return {
            'ID': ['id'],
            '论文编号': ['LWBH'],
            '论文名称': ['LWMC'],
            '论文类型码': ['LWLXM'],
            '第一作者': ['DYZZ'],
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


class DR_KJLWFBXX(Base):  # 科技论文发表信息

    __tablename__ = 'dr_kjlwfbxx'  # 科技论文发表信息

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    KWMC = Column('KWMC', String(16), default='')  # 刊物名称
    LWBH = Column('LWBH', String(16), default='')  # 论文编号
    FBRQ = Column('FBRQ', DateTime, default=now())  # 发表日期
    JH= Column('JH', String(16), default='')  # 卷号
    QH = Column('QH', String(16), default='')  # 期号
    LRSJ = Column('LRSJ', DateTime, default=now())  # 录入时间


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
        }

    @staticmethod
    def get_unique_condition() -> []:
        return ['LWBH']

if __name__ == '__main__':
    try:
        Base.metadata.create_all(engine)
        # obj = DR_ZZJGJBSJXX(DWH='1234', JLNY='19200121')
        # db.add(obj)
        # db.commit()
    except IntegrityError as e:
        print(e)

    except:
        print(sys_info())

    exit(0)
