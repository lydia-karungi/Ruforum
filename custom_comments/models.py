from django.db import models

from django_comments.models import Comment 


class Ruforumcomment(models.Model):
    COMMENT_TYPES = (
        ('general', 'General'),
        ('administrative', 'Administrative'),
        ('technical', 'Technical'),
    )
    comment_ptr = models.OneToOneField(Comment, models.DO_NOTHING, primary_key=True)
    comment_type = models.CharField(max_length=32, blank=True, null=True, choices=COMMENT_TYPES)
