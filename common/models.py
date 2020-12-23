import time
import binascii
import arrow
from django.db import models

from contacts.models import User

from common.templatetags.common_tags import (
    is_document_file_image, is_document_file_audio,
    is_document_file_video, is_document_file_pdf,
    is_document_file_code, is_document_file_text,
    is_document_file_sheet, is_document_file_zip
)
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


def document_path(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("docs", hash_, filename)


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    commented_on = models.DateTimeField(auto_now_add=True)
    commented_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='comments')

    user = models.ForeignKey(
        User, blank=True, null=True,
        related_name="user_comments",
        on_delete=models.CASCADE)

    task = models.ForeignKey('tasks.Task', blank=True, null=True,
                             related_name='tasks_comments', on_delete=models.CASCADE)


    def get_files(self):
        return Comment_Files.objects.filter(comment_id=self)

    @property
    def commented_on_arrow(self):
        return arrow.get(self.commented_on).humanize()


class Comment_Files(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now_add=True)
    comment_file = models.FileField(
        "File", upload_to="comment_files", default='')

    def get_file_name(self):
        if self.comment_file:
            return self.comment_file.path.split('/')[-1]

        return None


class Attachments(models.Model):
    created_by = models.ForeignKey(
        User, related_name='attachment_created_by',
        on_delete=models.SET_NULL, null=True)
    file_name = models.CharField(max_length=60)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    attachment = models.FileField(
        max_length=1001, upload_to='attachments/%Y/%m/')

    task = models.ForeignKey('tasks.Task', blank=True, null=True,
                             related_name='tasks_attachment', on_delete=models.CASCADE)

    travel = models.ForeignKey('hrm.StaffTravel', blank=True, null=True,
                                related_name='travel_attachment', on_delete=models.CASCADE)
    event = models.ForeignKey('events.Event', blank=True, null=True,
                              related_name='events_attachment', on_delete=models.CASCADE)

    def file_type(self):
        name_ext_list = self.attachment.url.split(".")
        if (len(name_ext_list) > 1):
            ext = name_ext_list[int(len(name_ext_list) - 1)]
            if is_document_file_audio(ext):
                return ("audio", "fa fa-file-audio")
            if is_document_file_video(ext):
                return ("video", "fa fa-file-video")
            if is_document_file_image(ext):
                return ("image", "fa fa-file-image")
            if is_document_file_pdf(ext):
                return ("pdf", "fa fa-file-pdf")
            if is_document_file_code(ext):
                return ("code", "fa fa-file-code")
            if is_document_file_text(ext):
                return ("text", "fa fa-file-alt")
            if is_document_file_sheet(ext):
                return ("sheet", "fa fa-file-excel")
            if is_document_file_zip(ext):
                return ("zip", "fa fa-file-archive")
            return ("file", "fa fa-file")
        return ("file", "fa fa-file")

    def get_file_type_display(self):
        if self.attachment:
            return self.file_type()[1]
        return None

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    def get_enrollment(self,pi_id):
        return self.enrolled_student.filter(pi__id=pi_id).last()


def document_path(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("docs", hash_, filename)


class Document(models.Model):

    DOCUMENT_STATUS_CHOICE = (
        ("active", "active"),
        ('inactive', 'inactive')
    )

    title = models.CharField(max_length=1000, blank=True, null=True)
    document_file = models.FileField(upload_to=document_path, max_length=5000)
    created_by = models.ForeignKey(
        User, related_name='documents',
        on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=DOCUMENT_STATUS_CHOICE, max_length=64, default='active')
    shared_to = models.ManyToManyField(User, related_name='document_shared_to')

    class Meta:
        ordering = ('-created_on',)

    def file_type(self):
        name_ext_list = self.document_file.url.split(".")
        if (len(name_ext_list) > 1):
            ext = name_ext_list[int(len(name_ext_list) - 1)]
            if is_document_file_audio(ext):
                return ("audio", "fa fa-file-audio")
            if is_document_file_video(ext):
                return ("video", "fa fa-file-video")
            if is_document_file_image(ext):
                return ("image", "fa fa-file-image")
            if is_document_file_pdf(ext):
                return ("pdf", "fa fa-file-pdf")
            if is_document_file_code(ext):
                return ("code", "fa fa-file-code")
            if is_document_file_text(ext):
                return ("text", "fa fa-file-alt")
            if is_document_file_sheet(ext):
                return ("sheet", "fa fa-file-excel")
            if is_document_file_zip(ext):
                return ("zip", "fa fa-file-archive")
            return ("file", "fa fa-file")
        return ("file", "fa fa-file")

    def __str__(self):
        return self.title

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()


def generate_key():
    return binascii.hexlify(os.urandom(8)).decode()
