from django.db import models
from django.conf.urls import url
from django.conf import settings
import misaka

from django.urls import reverse

from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User,related_name='posts',on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=True)
    group = models.ForeignKey(Group,related_name='posts',null=True,blank=True,on_delete=models.DO_NOTHING)
    

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absoulte_url(self):
        return reverse('posts:single',kwargs={'username':self.username,'pk':self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user','message']
