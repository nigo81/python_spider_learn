import json
import os

import requests

headers = {
    'Referer': 'http://kcb.sse.com.cn/disclosure/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
}
SAVE_PATH = './DATA'

CurrStatus = {
    '1': '已受理',
    '2': '已询问',
    '4': '提交注册',
    '5': '注册结果',
    '7': '中止',
    '8': '终止',
    '3': '通过',
    '6': '未通过',
}


def crawl_list(page):
    url = 'http://query.sse.com.cn/commonSoaQuery.do'
    params = {
        'isPagination': 'true',
        'sqlId': 'GP_GPZCZ_SHXXPL',
        'pageHelp.pageSize': 20,
        'fileType': '30,5,6',
        'PageHelp.pageNo': page,
        'pageHelp.beginPage': page,
        'pageHelp.endPage': page,
    }
    resp = requests.get(url=url, headers=headers, params=params)
    data = json.loads(resp.text)
    results = list()
    for item in data['result']:
        item['filePath'] = 'http://kcb.sse.com.cn' + item['filePath']
        results.append(item)
    pageCount = data['pageHelp']['pageCount']
    return results, pageCount


def crawl_list2(page):
    url = 'http://query.sse.com.cn/commonSoaQuery.do'
    params = {
        'isPagination': 'true',
        'sqlId': 'SH_XM_LB',
        'pageHelp.pageSize': 20,
        'fileType': '30,5,6',
        'PageHelp.pageNo': page,
        'pageHelp.beginPage': page,
        'pageHelp.endPage': page,
    }
    resp = requests.get(url=url, headers=headers, params=params)
    data = json.loads(resp.text)
    pageCount = data['pageHelp']['pageCount']
    return data['result'], pageCount


def download_pdf(url, save_path):
    for _ in range(3):
        try:
            fp = open(save_path, 'wb')
            resp = requests.get(url=url, headers=headers)
            fp.write(resp.content)
            fp.close()
            return True
        except Exception as e:
            print(e)
    raise OverflowError('Download Error')


def crawl_info(stockAuditNum):
    url = 'http://query.sse.com.cn/commonSoaQuery.do'
    params = {
        'isPagination': 'true',
        'sqlId': 'SH_XM_LB',
        'stockAuditNum': stockAuditNum
    }
    data = requests.get(url=url, headers=headers, params=params).json()
    result = {
        '注册地': '',
        '证监会行业': '',
        '发行人全称': data['result'][0]['stockAuditName'],
        '受理日期': data['result'][0]['auditApplyDate'][:8],
        '公司简称': data['result'][0]['stockIssuer'][0]['s_issueCompanyAbbrName'],
        '融资金额(亿元)': data['result'][0]['planIssueCapital'],
        '审核状态': CurrStatus[str(data['result'][0]['currStatus'])],
        '更新日期': data['result'][0]['updateDate'][:8],
        '保荐机构': '',
        '保荐代表人': '',
        '会计师事务所': '',
        '签字会计师': '',
        '律师事务所': '',
        '签字律师': '',
        '评估机构': '',
        '签字评估师': '',
    }
    for item in data['result'][0]['intermediary']:
        if item['i_intermediaryType'] == 1:
            result['保荐机构'] = item['i_intermediaryName']
            result['保荐代表人'] = '、'.join([i['i_p_personName'] for i in item['i_person'] if '保荐代表人' in i['i_p_jobTitle']])
        elif item['i_intermediaryType'] == 2:
            result['会计师事务所'] = item['i_intermediaryName']
            result['签字会计师'] = '、'.join([i['i_p_personName'] for i in item['i_person'] if '签字会计师' in i['i_p_jobTitle']])
        elif item['i_intermediaryType'] == 3:
            result['律师事务所'] = item['i_intermediaryName']
            result['签字律师'] = '、'.join([i['i_p_personName'] for i in item['i_person'] if '签字律师' in i['i_p_jobTitle']])
        elif item['i_intermediaryType'] == 4:
            result['评估机构'] = item['i_intermediaryName']
            result['签字评估师'] = '、'.join([i['i_p_personName'] for i in item['i_person'] if '签字评估师' in i['i_p_jobTitle']])
    return result


def start_download():
    page = 1
    pageCount = ''
    fp = open('Results.csv', 'w', encoding='gbk', errors='ignore')
    TITLE = ['stockAuditNum', 'publishDate', 'companyFullName', 'fileTitle']
    fp.write(','.join(TITLE) + '\n')
    while True:
        print(f'Current crawl page {page}, total {pageCount}')
        results, pageCount = crawl_list(page)
        for result in results:
            print(result['companyFullName'], result['fileTitle'])
            save_path = os.path.join(SAVE_PATH, '_'.join(
                [result['publishDate'], result['companyFullName'], result['fileTitle'] + '.pdf']))
            download_pdf(result['filePath'], save_path)
            fp.write(','.join([result[i] for i in TITLE]) + '\n')
        fp.flush()
        page += 1
        if page > pageCount:
            break
    fp.close()


def start_crwal():
    page = 1
    pageCount = ''
    fp = open('Info.csv', 'w', encoding='gbk', errors='ignore')
    TITLE = ['注册地', '证监会行业', '发行人全称', '受理日期', '公司简称', '融资金额(亿元)', '审核状态', '更新日期', '保荐机构', '保荐代表人', '会计师事务所', '签字会计师',
             '律师事务所', '签字律师', '评估机构', '签字评估师']
    fp.write(','.join(TITLE) + '\n')
    while True:
        print(f'Current crawl page {page}, total {pageCount}')
        results, pageCount = crawl_list2(page)
        for result in results:
            data = crawl_info(result['stockAuditNum'])
            data['注册地'] = result['stockIssuer'][0]['s_province']
            data['证监会行业'] = result['stockIssuer'][0]['s_csrcCodeDesc']
            fp.write(','.join([str(data[i]) for i in TITLE])+'\n')
        fp.flush()
        page += 1
        if page > pageCount:
            break
    fp.close()


if __name__ == '__main__':
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    start_download()
    start_crwal()
