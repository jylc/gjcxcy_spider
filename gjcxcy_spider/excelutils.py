# -- coding: UTF-8 --
import pandas as pd
from gjcxcy_spider.items import ProjectItem, ProjectMentor, ProjectMembers
from loguru import logger


def open_excel(filename):
    excel_file = pd.DataFrame(pd.read_excel(filename))
    return excel_file


def write_to_excel(excel_file, data, output, df_rows):
    if data is not None:
        try:
            # df_rows = excel_file.shape[0] + 1
            currentPage = data['currentPage']
            projectId = data['id']
            projectName = data['name']
            projectType = data['type']
            projectCategory = data['category']
            projectKeySupportAreas = data['keySupportAreas']
            projectSchool = data['school']
            projectRangeTime = data['rangeTime']
            projectSubject = data['subject']
            projectMajor = data['major']
            projectEstablishedTime = data['establishedTime']
            projectMembers = data['projectMembers']
            projectMentors = data['projectMentor']
            projectDetails = data['projectDetail']

            detailsInfo = [projectDetails['detail1'], projectDetails['detail2'], projectDetails['detail3'],
                           projectDetails['detail4'], projectDetails['detail5'], projectDetails['detail6']]
            mentorsInfo = []
            projectData = [projectId, projectName, projectType, projectCategory, projectKeySupportAreas, projectSchool,
                           projectRangeTime, projectSubject, projectMajor, projectEstablishedTime]
            for projectMentor in projectMentors:
                mentorsInfo.append(' ')
                mentorsInfo.append(projectMentor['name'])
                mentorsInfo.append(projectMentor['workplace'])
                mentorsInfo.append(projectMentor['position'])
                mentorsInfo.append(projectMentor['mentorType'])

            for i in range(len(projectMentors), 5):
                mentorsInfo.append(' ')
                mentorsInfo.append(' ')
                mentorsInfo.append(' ')
                mentorsInfo.append(' ')
                mentorsInfo.append(' ')

            for projectMember in projectMembers:
                memberBlank = ' '
                memberName = projectMember['name']
                memberGrade = projectMember['grade']
                memberId = projectMember['id']
                memberDepartment = projectMember['department']
                memberMajor = projectMember['major']
                memberTelephone = projectMember['telephone']
                memberEmail = projectMember['email']
                memberHost = projectMember['host']
                memberData = [memberBlank, memberName, memberGrade, memberId, memberDepartment, memberMajor,
                              memberTelephone,
                              memberEmail, memberHost]
                data_line = projectData + memberData + mentorsInfo + detailsInfo
                show_datas = data_line.copy()
                show_datas.insert(0, len(data_line))
                logger.info(show_datas)
                excel_file.loc[df_rows] = data_line
                df_rows += 1
            # excel_file.to_excel(output, index=False)
        except Exception as e:
            logger.error('error{},id={}', e, data['id'])
    return df_rows


if __name__ == '__main__':
    filename_ = "./output/frame.xlsx"
    open_excel(filename_)
