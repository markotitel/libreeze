from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=512)

class ProjectDependency(models.Model):
    project = models.ForeignKey(Project)

class LatestDependency(models.Model):
    group_id = models.CharField(max_length=512)
    artifact_id = models.CharField(max_length=256)
    version = models.CharField(max_length=256).db_index
    index_together = [group_id, artifact_id]
    unique_together = (group_id, artifact_id, version)

