from django.db import models


class Template(models.Model):
    model = models.CharField(max_length=128)
    field_name = models.TextField()
    label = models.TextField()
    file = models.FileField(blank=True, null=True, upload_to='file_templates')
    
