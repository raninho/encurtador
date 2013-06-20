import base64

from django.db import models
from django.contrib.auth.models import User


class Url(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=1000, verbose_name='Url', blank=False, null=False)
    momento_cadastro = models.DateField(auto_now=False, auto_now_add=True)
    usuario = models.ForeignKey(User, null=True)

    class Meta:
        db_table = 'urls'
        ordering = ['-id']

    def __unicode__(self):
        return self.url

    @property
    def token(self):
        return base64.b64encode(str(self.id))
