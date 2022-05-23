# -*-coding:utf8-*-
import os.path
import sys
from abc import ABC

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

from loguru import logger
from gjcxcy_spider.items import ProjectItem, ProjectMembers, ProjectMentor, ProjectDetail

HEADERS = {
    'X-MicrosoftAjax': 'Delta=true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
}
URL = 'http://exitrealty.com/agent_list.aspx?firstName=&lastName=&country=USA&state=NY'


class ProjectSpider(CrawlSpider, ABC):
    name = "gjcxcy_spider"
    allow_domains = ['http://gjcxcy.bjtu.edu.cn/']
    start_urls = [
        'http://gjcxcy.bjtu.edu.cn/NewLXItemListForStudent.aspx?year=2021',
        'http://gjcxcy.bjtu.edu.cn/NewLXItemListForStudentDetail.aspx?ItemNo=863943&year=2021&type=student&IsLXItem=0']
    base_url = 'http://gjcxcy.bjtu.edu.cn/NewLXItemListForStudentDetail.aspx?ItemNo={}&year={}&type=student&IsLXItem=0'

    min_page = 1
    max_page = 1284

    year = 2021

    def __init__(self, *a, **kw):
        super(ProjectSpider, self).__init__(*a, **kw)

    def start_requests(self):
        url = self.start_urls[0]
        return [Request(url, callback=self.parse_pagination, errback=self.parse_error,
                        dont_filter=True, headers=HEADERS)]

    def parse_error(self, response):
        logger.error('craw {} failed'.format(response))

    def parse_pagination(self, response):
        """
        表单分页
        :param response:
        :return:
        """
        selector = Selector(response)
        # 表单翻页请求
        viewstate = selector.xpath("//input[@id='__VIEWSTATE']/@value").extract().pop()
        eventvalidation = selector.xpath("//input[@id='__EVENTVALIDATION']/@value").extract().pop()
        for i in range(self.min_page, self.max_page):
            data = {
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': '7CF496E6',
                '__EVENTTARGET': 'ctl00$ContentMain$AspNetPager1',
                '__EVENTARGUMENT': str(i),
                '__EVENTVALIDATION': eventvalidation,
                'ctl00$ContentMain$txtItemCode': '',
                'ctl00$ContentMain$txtItemName': '',
                'ctl00$ContentMain$SelYears': str(2021),
                'ctl00$ContentMain$txtFristUserName': '',
                'ctl00$ContentMain$txtFristUserAccount': '',
                'ctl00$ContentMain$txtSchoolName': '',
                'ctl00$ContentMain$txtTeacherName': '',
                'ctl00$ContentMain$SelItemLevel': '',
                'ctl00$ContentMain$SelItemType': '',
                'ctl00$ContentMain$txtSchoolCode': '',
                'ctl00$ContentMain$txtSubjectTwo': '',
                'ctl00$ContentMain$AspNetPager1_input': str(2)
            }
            # 去重
            current_ = FormRequest(self.start_urls[0], formdata=data, callback=self.parse_pagination_table,
                                   dont_filter=True, headers=HEADERS, method='POST',
                                   meta={'current_page': i})
            yield current_

    def parse_pagination_table(self, response):
        selector = Selector(response)
        positions = selector.xpath(
            '//table[@class="table c-table table-hover table_vertical-middle"]//tr/@id').extract()
        # logger.info(positions)
        for position in positions:
            current_position = position.replace('goto_tr_', '')
            url = self.base_url.format(current_position, self.year)
            # logger.info(url)
            yield Request(url=url, callback=self.parse_project_item, headers=HEADERS,
                          meta=response.meta)

    def parse_project_item(self, response):
        """
        解析项目
        :param response:
        :return:
        """
        selector = Selector(response)
        project_items_info = selector.xpath('//div[@class="form-group form-group-line"]')
        project_item = ProjectItem()
        project_item['currentPage'] = response.meta['current_page']
        for i in range(0, len(project_items_info)):
            label = project_items_info[i].xpath('./label/label/text()').extract_first()
            item = project_items_info[i].xpath('./div/text()').extract_first()
            item = item.strip()
            if label == '项目编号':
                project_item['id'] = item
            if label == '项目名称':
                project_item['name'] = item
            if label == '项目类型':
                project_item['type'] = item
            if label == '项目类别':
                project_item['category'] = item
            if label == '重点支持领域':
                project_item['keySupportAreas'] = item
            if label == '所属学校':
                project_item['school'] = item
            if label == '项目实施时间':
                project_item['rangeTime'] = item
            if label == '所属学科门类':
                project_item['subject'] = item
            if label == '所属专业大类':
                project_item['major'] = item
            if label == '立项时间':
                project_item['establishedTime'] = item

        project_numbers_info = selector.xpath('//div[@class="form-group"]')
        project_member = ProjectMembers
        project_mentor = ProjectMentor

        for i in range(0, len(project_numbers_info)):
            label = project_numbers_info[i].xpath('./label/label/text()').extract()
            for j in range(0, len(label)):
                if label[j] == "项目成员":
                    project_member = self.get_project_member(project_numbers_info[i])
                if label[j] == "指导教师":
                    project_mentor = self.get_project_mentor(project_numbers_info[i])

        project_details = selector.xpath('//table[@class="table table-bordered  infotable"]')
        project_item['projectDetail'] = self.get_project_details(project_details)
        project_item['projectMembers'] = project_member
        project_item['projectMentor'] = project_mentor
        yield project_item

    def get_project_member(self, selector):
        table_header = selector.xpath('.//table//tr')
        members_info = []
        for i in range(1, len(table_header)):
            table_ = table_header[i].xpath('.//td/text()').extract()
            member_info = ProjectMembers()
            member_info['name'] = table_[0].strip()
            member_info['grade'] = table_[1].strip()
            member_info['id'] = table_[2].strip()
            member_info['department'] = table_[3].strip()
            member_info['major'] = table_[4].strip()
            member_info['telephone'] = table_[5].strip()
            member_info['email'] = table_[6].strip()
            member_info['host'] = table_[7].strip()
            members_info.append(member_info)
        return members_info

    def get_project_mentor(self, selector):
        table_header = selector.xpath('.//table//tr')
        mentors_info = []
        for i in range(1, len(table_header)):
            table_ = table_header[i].xpath('.//td').extract()
            mentor_info = ProjectMentor()
            mentor_info['name'] = table_[0].strip().strip('<td>').strip('</td>')
            mentor_info['workplace'] = table_[1].strip().strip('<td>').strip('</td>')
            mentor_info['position'] = table_[2].strip().strip('<td>').strip('</td>')
            mentor_info['mentorType'] = table_[3].strip().strip('<td>').strip('</td>')
            mentors_info.append(mentor_info)
        return mentors_info

    def get_project_details(self, selector):
        projectDetail = ProjectDetail()
        projectDetail['detail1'] = ''
        projectDetail['detail2'] = ''
        projectDetail['detail3'] = ''
        projectDetail['detail4'] = ''
        projectDetail['detail5'] = ''
        projectDetail['detail6'] = ''
        details = selector.xpath('.//tr')
        for detail in details:
            if detail.xpath('./td[@class="labbelbg"]/text()').extract_first() == '负责人曾经参与科研的情况：':
                tmp = detail.xpath('./td//text()').extract()
                tmp = ' '.join(tmp)
                projectDetail['detail1'] = tmp.replace('\r\n', ' ')
            if detail.xpath('./td[@class="labbelbg"]/text()').extract_first() == '指导教师承担科研课题情况：':
                tmp = detail.xpath('./td//text()').extract()
                tmp = ' '.join(tmp)
                projectDetail['detail2'] = tmp.replace('\r\n', ' ')
            if detail.xpath('./td[@class="labbelbg"]/text()').extract_first() == '指导教师对本项目的支持情况：':
                tmp = detail.xpath('./td//text()').extract()
                tmp = ' '.join(tmp)
                projectDetail['detail3'] = tmp.replace('\r\n', ' ')
            if detail.xpath('./td[@class="labbelbg"]/text()').extract_first() == '项目简介：':
                tmp = detail.xpath('./td//text()').extract()
                tmp = ' '.join(tmp)
                projectDetail['detail4'] = tmp.replace('\r\n', ' ')
            if detail.xpath('./td[@class="labbelbg"]/text()').extract_first() == '企业导师担任的职务及科研情况：':
                tmp = detail.xpath('./td//text()').extract()
                tmp = ' '.join(tmp)
                projectDetail['detail5'] = tmp.replace('\r\n', ' ')
            if detail.xpath('./td[@class="labbelbg"]/text()').extract_first() == '指导教师、企业导师支持情况：':
                tmp = detail.xpath('./td//text()').extract()
                tmp = ' '.join(tmp)
                projectDetail['detail6'] = tmp.replace('\r\n', ' ')
        return projectDetail
