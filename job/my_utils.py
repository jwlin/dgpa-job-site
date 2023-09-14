import re
import requests
import xml.etree.ElementTree as ET
import datetime
import ssl
import os
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.conf import settings


def get_jobs_from_xml(xml_path, is_path_local=False):
    resp = ''
    if is_path_local:
        resp = xml_path
    elif '?GETJOB=Y' in xml_path:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        resp = urlopen(xml_path, context=ctx)
    else:
        # first HTTP request without form data
        resp = requests.get(xml_path, verify=False)
        soup = BeautifulSoup(resp.text)
        # parse and retrieve 3 vital form values
        viewstate = soup.select("#__VIEWSTATE")[0]['value']
        eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']
        viewstategenerator = soup.select("#__VIEWSTATEGENERATOR")[0]['value']
        formData = {
            '__EVENTVALIDATION': eventvalidation,
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            'ctl00$ContentPlaceHolder1$btn_DownloadXML': '職缺 Open Data(XML)'
        }
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        resp = requests.post(xml_path, verify=False, stream=True, data=formData, headers=header)
        resp = resp.raw

    tree = ET.parse(resp)
    root = tree.getroot()
    unqualified_list = [] # 非公務人員
    with open(os.path.join(settings.BASE_DIR, 'job', 'filters', 'unqualified-list.txt'), encoding='utf-8') as fp:
        for line in fp:
            unqualified_list.append(line.strip())
    jobs = []
    for row in root.findall('ROW'):
        person_kind = row.find('PERSON_KIND').text
        if row.find('SYSNAM').text:
            sysnam = row.find('SYSNAM').text.replace(u'職系', '')
            sysnam = sysnam.replace(u'ㄧ', u'一')
        else:
            sysnam = None
        # 僅處理公務人員 (不在 unqualifiedList 中) 且 sysnam 非空
        if (person_kind not in unqualified_list) and (sysnam is not None):

            # 將多個工作地轉為 [ids, names]
            # 工作地為 98-連江, 88-澎湖, 89-金門, 20-基隆, 調整數值以便正確排序
            work_places = []
            work_places_ids = list(map(int, re.findall(r'\d+', row.find('WORK_PLACE_TYPE').text)))
            work_places_names = list(re.findall(r'[\u4E00-\u9fa5]+', row.find('WORK_PLACE_TYPE').text))
            for idx, w_id in enumerate(work_places_ids):
                if w_id in [88, 89]:
                    work_places_ids[idx] += 80
                elif w_id == 98:
                    work_places_ids[idx] = 101
                elif w_id == 20:
                    work_places_ids[idx] = 24
            work_places.append(work_places_ids)
            work_places.append(work_places_names)

            job = {
                'org_name': row.find('ORG_NAME').text,
                'person_kind': person_kind,
                'sysnam': sysnam,
                'rank': convertRank(row.find('RANK').text),
                'title': row.find('TITLE').text,
                'num': replaceChNum(row.find('NUMBER_OF').text),
                'gender': row.find('GENDER_TYPE').text,
                'work_places': work_places,
                'date_from': convertDate(row.find('DATE_FROM').text),
                'date_to': convertDate(row.find('DATE_TO').text),
                'is_handicap': convertBoolean(row.find('IS_HANDICAP').text),
                'is_orig': convertBoolean(row.find('IS_ORIGINAL').text),
                'is_local_orig': convertBoolean(row.find('IS_LOCAL_ORIGINAL').text),
                'is_training': convertBoolean(row.find('IS_TRANING').text),
                'type': row.find('TYPE').text,
                'email': row.find('VITAE_EMAIL').text,
                'work_quality': row.find('WORK_QUALITY').text,
                'work_item': row.find('WORK_ITEM').text,
                'work_addr': row.find('WORK_ADDRESS').text,
                'contact': row.find('CONTACT_METHOD').text,
                'url': row.find('URL_LINK').text,
                'view_url': row.find('VIEW_URL').text,
            }
            jobs.append(job)
    return jobs

# replace Chinese Number with digital one
def replaceChNum(s):
    pattern1 = [u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九',u'十']
    pattern2 = [u'壹',u'貳',u'參',u'肆',u'伍',u'陸',u'柒',u'捌',u'玖',u'拾']
    pattern3 = [u'１',u'２',u'３',u'４',u'５',u'６',u'７',u'８',u'９',u'１０']
    replacement = ['1','2','3','4','5','6','7','8','9','10']
    for i in range(0,10):
        s = s.replace(pattern1[i], replacement[i])
        s = s.replace(pattern2[i], replacement[i])
        s = s.replace(pattern3[i], replacement[i])
    s = s.replace(u'乙', '1')
    # delete extra 0. ex. 104 -> 14
    s = re.sub('(10[0-9])',lambda m: m.group(0).replace('10', '1'), s)
    return s

# convert RANK field to a rank obj.
# ex. "委任第五職等或薦任第六職等至第七職等" -> rank{from: 5, to: 7};
def convertRank(s):
    if s == None:
        return {'from': 0, 'to': 0}

    s = replaceChNum(s)
    ranks = list(map(int, re.findall(r'\d+', s)))

    if len(ranks) == 0:
        return {'from': 0, 'to': 0}

    ranks.sort()
    return {'from': ranks[0], 'to': ranks[-1]}

def convertDate(s):
    y = int(s[0:3])+1911
    m = int(s[3:5])
    d = int(s[5:7])
    date = datetime.date(y, m, d)
    return date

def convertBoolean(s):
    if (s is not None) and (s == 'Y'):
        return True
    else:
        return False

# judge if a sysnam belongs to tech or admin type.
# admin: return 0. tech: return 1
def judge_type(sysnam):
    adminlist = []
    with open(os.path.join(settings.BASE_DIR, 'job','filters', 'adminlist.txt'), encoding='utf-8') as fp:
        for line in fp:
            adminlist.append(line.strip())

    for keyword in adminlist:
        if keyword in sysnam:
            return 0
    return 1

def filter(sysnam):
    sysnam_exclude = []
    with open(os.path.join(settings.BASE_DIR, 'job', 'filters', 'sysnam-filter-exclude.txt'), encoding='utf-8') as fp:
        for line in fp:
            sysnam_exclude.append(line.strip())

    sysnam_list = [[],[]]
    with open(os.path.join(settings.BASE_DIR, 'job', 'filters', 'sysnam-filter-ad.txt'), encoding='utf-8') as fp:
        for line in fp:
            sysnam_list[0].append(line.strip())
    with open(os.path.join(settings.BASE_DIR, 'job', 'filters', 'sysnam-filter-tech.txt'), encoding='utf-8') as fp:
        for line in fp:
            sysnam_list[1].append(line.strip())
    
    for word in sysnam_exclude:
        if word in sysnam:
            return False

    for sublist in sysnam_list:
        for word in sublist:
            if word in sysnam:
                return True
    return False


def split_sysnam(sysnam):
    # ex. sysnam = u'具教育行政（含文化行政、新聞、博物館管理、圖書資訊管理、史料編纂）任用資格 :'
    if sysnam[0] == u'具':
        sysnam = sysnam[1:]
    sysnam = re.sub(u'[（）()：: 「」]', '', sysnam)
    discards = [u'任用資格', u'預估缺', u'秘書室', u'6204', u'技術類']
    for discard in discards:
        sysnam = sysnam.replace(discard, '')
    splitters = [u'、', u'或', u'及', u'/', u'含', ',']
    # first pass
    sysnam_list = list()
    for splitter in splitters:
        if splitter in sysnam:
            sysnam_list = sysnam.split(splitter)
            break
    # second pass
    new_sysnam_list = list()
    if sysnam_list:
        checked = False
        for splitter in splitters:
            if checked:
                break
            new_sysnam_list = list()
            for nam in sysnam_list:
                if splitter in nam:
                    new_sysnam_list += nam.split(splitter)
                    checked = True
                else:
                    new_sysnam_list.append(nam)
    if new_sysnam_list:
        return new_sysnam_list
    elif sysnam_list:
        return sysnam_list
    else:
        return [sysnam]


def isResumeRequired(url, is_path_local=False):
    if not url:
        return False
    
    if is_path_local:
        with open(url, "r", encoding="utf-8") as f:
            resp = f.read()
    else:
        resp = requests.get(url, verify=False)
        if resp.status_code != 200:
            return False
        else:
            resp = resp.text
    
    if '<span id="txt_UseResume"' in resp:
        return True
    else:
        return False


def get_latest_xml_file(folder_path):
    xml_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.xml')]    
    if not xml_files:
        return None    
    latest_xml_file = max(xml_files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))    
    return os.path.join(folder_path, latest_xml_file)


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dgpaproject.settings'
    jobs = get_jobs_from_xml(os.path.join(settings.BASE_DIR, "data/job.230827.xml"), is_path_local=True)
    print(jobs[0])
    print(len(jobs))