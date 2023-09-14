from django.db import models
from django.core.validators import validate_comma_separated_integer_list


class Job(models.Model):
    title = models.CharField(max_length=300)
    sysnam = models.CharField(max_length=300)
    org_name = models.CharField(max_length=300)
    person_kind = models.CharField(max_length=100)
    rank_from = models.PositiveIntegerField()
    rank_to = models.PositiveIntegerField()
    work_quality = models.CharField(max_length=4000)
    work_item = models.CharField(max_length=2000, null=True)
    work_addr = models.CharField(max_length=2000, null=True)
    is_resume_required = models.BooleanField(default=False)

    def __str__(self):
        statement = ' | '.join([
            str(self.id), 
            self.org_name,
            self.sysnam,
            self.title, 
            self.person_kind, 
            str(self.rank_from), 
            str(self.rank_to)
        ])
        return statement


class JobHistory(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        statement = ' | '.join([
            str(self.job.id), 
            str(self.date_from), 
            str(self.date_to) 
        ])
        return statement


class CurrentJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    sysnam = models.CharField(max_length=300)
    org_name = models.CharField(max_length=300)
    person_kind = models.CharField(max_length=100)
    rank_from = models.PositiveIntegerField()
    rank_to = models.PositiveIntegerField()
    num = models.PositiveIntegerField()
    gender = models.CharField(max_length=100)
    work_places_id = models.CharField(validators=[validate_comma_separated_integer_list], max_length=500)
    date_from = models.DateField()
    date_to = models.DateField()
    is_handicap = models.BooleanField()
    is_orig = models.BooleanField()
    is_local_orig = models.BooleanField()
    is_training = models.BooleanField()
    job_type = models.CharField(max_length=50)
    email = models.CharField(max_length=2000, null=True)
    work_quality = models.CharField(max_length=4000)
    work_item = models.CharField(max_length=2000, null=True) 
    work_addr = models.CharField(max_length=2000, null=True)
    contact = models.CharField(max_length=4000, null=True)
    url = models.CharField(max_length=200, null=True)
    view_url = models.CharField(max_length=400)
    isExpiring = models.BooleanField()
    history_count = models.PositiveSmallIntegerField()
    is_resume_required = models.BooleanField(default=False)

    def __str__(self):
        statement = ' | '.join([
            str(self.job.id), 
            self.org_name, 
            self.sysnam,
            self.title, 
            self.person_kind, 
            str(self.rank_from), 
            str(self.rank_to)
        ])
        return statement


class WorkPlace(models.Model):
    work_place_id = models.PositiveSmallIntegerField()
    work_place_name = models.CharField(max_length=30)

    def __str__(self):
        statement = ' | '.join([
            str(self.work_place_id), 
            self.work_place_name
        ])
        return statement


class UpdateRecord(models.Model):
    last_update_day = models.DateField()

    def __str__(self):
        return str(self.last_update_day)


class JobMessage(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    last_modified = models.DateTimeField(auto_now=True)
    password =  models.CharField(max_length=200)

    def __str__(self):
        msg = self.message[:50] + '..' if len(self.message) > 50 else self.message
        return str(self.job.id) + ' | ' + msg


class JobTrend(models.Model):
    sysnam = models.CharField(max_length=100)
    date = models.DateField()
    num = models.PositiveSmallIntegerField(default=0)
    HIGH = 1
    MIDDLE = 2
    LOW = 3
    LEVEL_CHOICES = (
        (HIGH, u'簡任'),
        (MIDDLE, u'薦任'),
        (LOW, u'委任')
    )
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=LOW)

    def __str__(self):
        statement = ' | '.join([
            self.sysnam, 
            str(self.date),
            str(self.num),
            str(self.level)
        ])
        return statement