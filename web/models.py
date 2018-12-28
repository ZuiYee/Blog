from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Article(models.Model):
    title = models.CharField(u'标题', max_length=100, null=True, blank=True)
    time = models.DateField(u'发表时间', max_length=100, null=True, blank=True)
    abstract = models.TextField(u'摘要', max_length=15, null=True, blank=True)
    content = models.TextField(u'内容', null=True, blank=True)
    type = models.CharField(u'文章类型', max_length=100, null=True, blank=True)
    img = ProcessedImageField(upload_to='icons', null=True, blank=True,
                              processors=[ResizeToFill(380, 243)],
                              format='JPEG',
                              options={'quality': 95},
                              )

    def __unicode__(self):
        return self.title
