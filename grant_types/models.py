from django.db import models


class Granttype(models.Model):
    name = models.CharField(max_length=30)
    instructions = models.FileField()
    template = models.FileField()
    require_other_universities = models.BooleanField()
    require_collaborator_cvs = models.BooleanField()
    require_supporting_letters = models.BooleanField()
    require_project_budget = models.BooleanField()
    project_budget_template = models.FileField()
    review_form_template = models.FileField()

    def __str__(self):
        return self.name