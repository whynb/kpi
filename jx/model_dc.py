# coding=utf-8
# 定义导入数据模型，与东大校标一致; 可自动运行建表，字段变化后需要手工写SQL调整

from jx.sqlalchemy_env import *


class DC_ZZJGJBSJXX(Base):
    __tablename__ = 'dc_zzjgjbsjxx'
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


class DC_PKSJXX(Base):
    __tablename__ = 'dc_pksjxx'
    __tablename__CH__ = '排课数据信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    JSGH = Column('JSGH', String(16), unique=True, default='')  # 教师工号
    KCH = Column('KCH', String(16), default='')  # 课程号
    JSXM = Column('JSXM', String(16), default='')  # 教师姓名
    KKXND = Column('KKXND', String(16), default='')  # 开课学年度
    SKBJH = Column('SKBJH', String(16), default='')  # 上课班级号
    KKXQM = Column('KKXQM', String(16), default='')  # 开课学期码
    ZXXS = Column('ZXXS', String(16), default='')  # 总学时
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
            '教学名师级别码': ['JXMSJBM'],
            '外语课程调节码': ['WYKCTJM'],
            '质量系数': ['ZLXS'],
            '合班数': ['HBS '],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['JSGH']


class DC_KCSJXX(Base):
    __tablename__ = 'dc_kcsjxx'
    __tablename__CH__ = '课程数据信息'

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


class DC_XNXQXX(Base):
    __tablename__ = 'dc_xnxqxx'
    __tablename__CH__ = '学年学期信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    XQMC = Column('XQMC', String(16), unique=True, default='')  # 学期名称
    XNXQM = Column('XNXQM', String(16), default='')  # 学年学期名
    XNDM = Column('XNDM', String(16), default='')  # 学年代码
    XQDM = Column('XQDM', String(16), default='')  # 学期代码
    XNMC = Column('XNMC', String(16), default='')  # 学年名称
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
            '学期类型代码': ['XQLXDM'],
            '学期类型名称': ['XQLXMC'],
            '是否当前学期': ['SFDQXQ'],
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List[str]:
        return ['XNXQM']


class DC_BKS_JPKC(Base):
    __tablename__ = 'dc_bks_jpkc'
    __tablename__CH__ = '本科精品课程'

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


class DC_JZGJCSJXX(Base):
    __tablename__ = 'dc_jzgjcsjxx'
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


class DC_XMJFXX(Base):
    __tablename__ = 'dc_xmjfxx'
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
class DC_HJCGJBSJXX(Base):
    __tablename__ = 'dc_hjcgjbsjxx'
    __tablename__CH__ = '获奖成果基本数据信息'

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
        return ['HJCGBH', 'HJCGMC']


class DC_KJCGRYXX_JL(Base):
    __tablename__ = 'dc_kjcgryxx_jl'
    __tablename__CH__ = '科技成果(获奖成果)人员信息'

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
        return ['RYH']

#zouyang
class DC_KJQKLWJBSJXX(Base):
    __tablename__ = 'dc_kjqklwjbsjxx'
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
            '时间戳': ['stamp', 'DateTime'],
            '备注': ['note'],
        }

    @staticmethod
    def get_unique_condition() -> List:
        return ['LWBH']

#zouyang
class DC_KJLWFBXX(Base):
    __tablename__ = 'dc_kjlwfbxx'
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
    def get_unique_condition() -> List:
        return ['LWBH']

#zouyang
class DC_KJCGRYXX_LW(Base):  # 科技成果(论文)人员信息

    __tablename__ = 'dc_kjcgryxx_lw'  # 科技成果(论文)人员信息

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
    RYH = Column('RYH', String(16), default='')  # 人员号
    JSM = Column('JSM', String(16), default='')  # 角色码
    ZXZS= Column('ZXZS', String(16), default='')  # 撰写字数
    PMZRS= Column('PMZRS', String(16), default='')  # 排名/总人数
    GXL = Column('GXL', String(16), default='')  # 贡献率
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
class DC_KJLWSLQK(Base):  # 科技论文收录情况

    __tablename__ = 'dc_kjlwslqk'  # 科技论文收录情况

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


# yangchen
class DC_ZLCGJBSJXX(Base):
    __tablename__ = 'dc_zlcgjbsjxx'
    __tablename__CH__ = '专利成果基本数据信息'
    __table_args__ = (UniqueConstraint('ZLCGBH', 'SQBH', name='_dc_zlcgjbsjxx_zlcgbh_sqbh_uc'),)

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


# yangchen
class DC_ZLCSXX(Base):
    __tablename__ = 'dc_zlcsxx'
    __tablename__CH__ = '专利出售信息'

    id = Column('id', Integer, autoincrement=True, primary_key=True, nullable=False)  # ID
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


# yangchen
class DC_KJCGRYXX_ZL(Base):
    __tablename__ = 'dc_kjcgryxx_zl'
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


class_dict = {key: var for key, var in locals().items() if isinstance(var, type)}


if __name__ == '__main__':

    try:
        Base.metadata.create_all(engine)
    except Error as e:
        print(e)

    exit(0)
