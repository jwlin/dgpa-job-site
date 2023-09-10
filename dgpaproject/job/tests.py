from django.test import TestCase
from .my_utils import split_sysnam, isResumeRequired, replaceChNum

class MyUtilTest(TestCase):
    def test_split_sysnam(self):
        dataset = [
            '具教育行政（含文化行政、新聞、博物館管理、圖書資訊管理、史料編纂）任用資格:',
            '原子能、電力工程、電子工程、機械工程、衛生技術、環保技術:',
            '土木工程及水利工程:',
            '交通技術',
            '電力工程或電子工程或機械工程：',
            '資訊處理 :',
            '警察官或消防行政 :',
            '土木工程/建築工程',
            '「一般行政」 :',
            '業務類（一般行政） :',
        ]
        ans = [
            ['教育行政', '文化行政', '新聞', '博物館管理', '圖書資訊管理', '史料編纂'],
            ['原子能', '電力工程', '電子工程', '機械工程', '衛生技術', '環保技術'],
            ['土木工程', '水利工程'],
            ['交通技術'],
            ['電力工程', '電子工程', '機械工程'],
            ['資訊處理'],
            ['警察官', '消防行政'],
            ['土木工程', '建築工程',],
            ['一般行政'],
            ['業務類一般行政']
        ]
        for i in range(len(dataset)):
            ss = split_sysnam(dataset[i])
            for j in range(len(ss)):
                self.assertEqual(ans[i][j], ss[j])
    
    # def test_isResumeRequired(self):
    #     self.assertFalse(isResumeRequired('http://web3.dgpa.gov.tw/want03front/ap/wantf00001_1.aspx?work_id=1050500240'))
    #     self.assertTrue(isResumeRequired('http://web3.dgpa.gov.tw/want03front/ap/wantf00001_1.aspx?work_id=1050300230'))
        

    def test_replaceChNum(self):
        s = '名額１符合下列各款資格者 １、曾經銓敘審定合格實授委任第3職等以上之公務人員【２、未曾受懲戒或行政處分，品行端'
        oracle = '名額1符合下列各款資格者 1、曾經銓敘審定合格實授委任第3職等以上之公務人員【2、未曾受懲戒或行政處分，品行端'
        self.assertEqual(replaceChNum(s), oracle)