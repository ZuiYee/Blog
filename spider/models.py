from django.db import models



class Score(models.Model):
    code = models.CharField(u'课程代码', max_length=50, null=True, blank=True)
    xh = models.CharField(u'学号', max_length=50, null=True, blank=True)
    name = models.CharField(u'姓名', max_length=50, null=True, blank=True)
    category = models.CharField(u'课程性质', max_length=50, null=True, blank=True)
    xf = models.CharField(u'学分', max_length=50, null=True, blank=True)
    daily_score = models.CharField(u'平时成绩', max_length=50, null=True, blank=True)
    test_score = models.CharField(u'考试成绩', max_length=50, null=True, blank=True)
    final_score = models.CharField(u'最终成绩', max_length=50, null=True, blank=True)
    source = models.CharField(u'学院名称', max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.code