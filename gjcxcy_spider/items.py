# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class GjcxcySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProjectItem(scrapy.Item):
    """项目属性
       Attributes:
        id 项目编号
        name 项目名称
        type 项目类型
        category 项目类别
        keySupportAreas 重点支持领域
        school 所属大学
        rangeTime 项目实施时间
        subject 所属学科门类
        major 所属专业大类
        establishedTime 立项时间
        projectMembers 项目成员
        projectMentor 指导教师
       """
    currentPage = Field()
    id = Field()
    name = Field()
    type = Field()
    category = Field()
    keySupportAreas = Field()
    school = Field()
    rangeTime = Field()
    subject = Field()
    major = Field()
    establishedTime = Field()
    projectMembers = Field()
    projectMentor = Field()
    projectDetail = Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProjectMembers(scrapy.Item):
    """项目成员
     Attributes:
        name 姓名
        grade 年级
        id 学号
        department 所在院系
        major 专业
        telephone 联系电话
        email E-mail
        host 是否主持人
    """
    name = Field()
    grade = Field()
    id = Field()
    department = Field()
    major = Field()
    telephone = Field()
    email = Field()
    host = Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProjectMentor(scrapy.Item):
    """指导教师
         Attributes:
            name 姓名
            workplace 单位
            position 专业技术职务
            mentorType 指导教师类型
     """
    name = Field()
    workplace = Field()
    position = Field()
    mentorType = Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProjectDetail(scrapy.Item):
    """项目信息
            Attributes:
               detail1 负责人曾经参与科研的情况
               detail2 指导教师承担科研课题情况
               detail3 指导教师对本项目的支持情况
               detail4 项目简介
               detail5 企业导师担任的职务及科研情况
               detail6 指导教师、企业导师支持情况
        """
    detail1 = Field()
    detail2 = Field()
    detail3 = Field()
    detail4 = Field()
    detail5 = Field()
    detail6 = Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
