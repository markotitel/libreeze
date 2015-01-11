from django.db import models

# Create your models here.

class Developer(models.Model):
    email = models.EmailField()

class Project(models.Model):
    POM = 'pm'
    BOWER = 'bw'
    SBT = 'sb'
    GRADLE = 'gr'
    PROJECT_TYPE_CHOICES = (
        (POM, 'Java Maven'),
        (BOWER, 'Javascript Bower'),
        (SBT, 'Scala Build Tool'),
        (GRADLE, 'Gradle')
    )
    owner = models.ForeignKey(Developer)
    name = models.TextField(max_length=512)
    type = models.CharField(max_length=2, choices=PROJECT_TYPE_CHOICES, default=POM)

class LatestDependency(models.Model):
    key = models.TextField(max_length=1024, unique=True, db_index=True)
    version = models.TextField(max_length=256, db_index=True)

class ProjectDependency(models.Model):
    project = models.ForeignKey(Project)
    latest = models.ForeignKey(LatestDependency)
    version = models.TextField(max_length=256, blank=True)
