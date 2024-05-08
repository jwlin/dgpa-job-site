import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'dgpaproject.settings'
django.setup()

from datetime import datetime, timedelta, date
from django.conf import settings
import re 
from django.db.models import Sum
from job.models import *
from job import my_utils


# xml_url = 'https://web3.dgpa.gov.tw/WANT03FRONT/AP/WANTF00003.aspx?GETJOB=Y'

# ensure data in CurrentJob is up to date
twDate = (datetime.utcnow() + timedelta(hours=8)).date()
yesterday = twDate + timedelta(days=-1)
ur = UpdateRecord.objects.all()[0]

#if (twDate != ur.last_update_day) or (not CurrentJob.objects.all()): # data is old or last update failed
# jobs = my_utils.get_jobs_from_xml(xml_url)    
latest_xml = my_utils.get_latest_xml_file(os.environ.get("XML_FOLDER"))
if latest_xml:
    jobs = my_utils.get_jobs_from_xml(latest_xml, is_path_local=True)
    CurrentJob.objects.all().delete()
    JobTrend.objects.filter(date=yesterday).delete()
    for job in jobs:
        # filter unqualified sysnam
        sysname = job['sysnam']
        if not my_utils.filter(sysname):
            continue

        if job['work_addr'] and len(job['work_addr']) > 2000:
            continue

        if not job['person_kind']:
            continue

        c_job = CurrentJob()
        c_job.title = job['title']
        c_job.sysnam = sysname
        c_job.org_name = job['org_name']
        c_job.person_kind = job['person_kind']
        c_job.rank_from = int(job['rank']['from'])
        c_job.rank_to = int(job['rank']['to'])
        c_job.work_quality = job['work_quality'] if job['work_quality'] else 'no data'
        c_job.work_item = job['work_item']
        c_job.work_addr = job['work_addr'] if job['work_addr'] else 'no data'
        
        # get the unique job_id of this job
        c_job.job, created = Job.objects.get_or_create(
            title = c_job.title,
            sysnam = c_job.sysnam,
            org_name = c_job.org_name,
            person_kind = c_job.person_kind,
            rank_from = c_job.rank_from,
            rank_to = c_job.rank_to,
            work_quality = c_job.work_quality,
            work_item = c_job.work_item,
            work_addr = c_job.work_addr
        )
        if created:
            new_job = Job.objects.get(id=c_job.job.id)
            # new_job.is_resume_required = my_utils.isResumeRequired(job['view_url'].replace('http://', 'https://'))
            new_job.is_resume_required = False
            new_job.save()
        
        searchObj = re.search( r'(\d+)', job['num'], re.M|re.I)
        if searchObj:
            c_job.num = int(searchObj.group())
        else:
            c_job.num = 0
            
        c_job.gender = job['gender']
        c_job.work_places_id = job['work_places'][0]
        c_job.date_from = job['date_from']
        c_job.date_to = job['date_to']
        c_job.is_handicap = job['is_handicap']
        c_job.is_orig = job['is_orig']
        c_job.is_local_orig = job['is_local_orig']
        c_job.is_training = job['is_training']
        c_job.job_type = job['type']
        c_job.email = job['email']
        c_job.work_quality = job['work_quality'] if job['work_quality'] else 'no data'
        c_job.contact = job['contact']
        c_job.url = job['url']
        c_job.view_url = job['view_url'].replace('http://', 'https://')
        c_job.is_resume_required = Job.objects.get(id=c_job.job.id).is_resume_required
                
        if ( c_job.date_to <= (twDate + timedelta(days=2)) ):
            c_job.isExpiring = True
        else:
            c_job.isExpiring = False

        job_his, created = JobHistory.objects.get_or_create(
            job = c_job.job,
            date_from = c_job.date_from,
            date_to = c_job.date_to
        )
            
        c_job.history_count = JobHistory.objects.filter(job = c_job.job).count()
        c_job.save()

    # accumulate job trends
    level = [3, 2, 1]
    level_rank = [0, 6, 10, 14]
    for i in range(3):
        yesterdayJobs = CurrentJob.objects.filter(date_from=yesterday, rank_to__gte=level_rank[i], rank_to__lt=level_rank[i+1]).values('sysnam').annotate(num=Sum('num')).order_by('-num')
        for yjob in yesterdayJobs:
            jt = JobTrend(sysnam=yjob['sysnam'], date=yesterday, num=yjob['num'], level=level[i])
            jt.save()
    
    ur.last_update_day = twDate
    ur.save()
