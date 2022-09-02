import uuid
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Contributor(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Work(BaseModel):
    iswc = models.CharField(primary_key=True, max_length=16)
    title = models.CharField(max_length=255)
    contributors = models.ManyToManyField(to=Contributor, related_name="works")

    def __str__(self):
        return self.title
