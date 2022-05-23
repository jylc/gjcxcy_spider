import re
import gjcxcy_spider.redisutils as ru
import gjcxcy_spider.excelutils as eu


# redis中数据导出到excel
def main():
    redis_pool = ru.connect_redis_pool()
    keys = redis_pool.keys()
    pipe = redis_pool.pipeline()
    key_list = []
    size = len(keys)
    for key in keys:
        key_list.append(key)
        pipe.get(key)

    value_list = pipe.execute()
    excel_file = eu.open_excel('./gjcxcy_spider/output/frame.xlsx')
    output_file_name = './gjcxcy_spider/output/statistics.xlsx'
    df_rows = excel_file.shape[0] + 1
    for (k, v) in zip(key_list, value_list):
        data = v.decode()
        projectItem = eval(data)
        df_rows = eu.write_to_excel(excel_file, projectItem, output=output_file_name, df_rows=df_rows)
        print(k)

    excel_file.to_excel(output_file_name, index=False)


if __name__ == '__main__':
    main()
