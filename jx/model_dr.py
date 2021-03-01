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
"""


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
