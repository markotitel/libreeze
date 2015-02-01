from django.db import models

# Create your models here.

class Developer(models.Model):
    email = models.EmailField()
    def __str__(self):
        return self.email

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
    owner = models.ForeignKey(Developer, blank=True)
    name = models.TextField(max_length=512)
    type = models.CharField(max_length=2, choices=PROJECT_TYPE_CHOICES, default=POM)

    def __str__(self):
        return self.name + ' ' + self.type

class MavenDependency(models.Model):
    group_id = models.TextField(max_length=512, db_index=True)
    artifact_id = models.TextField(max_length=256, db_index=True)
    latest = models.TextField(max_length=256)
    release = models.TextField(max_length=256)

    def __str__(self):
        return self.name + ' ' + self.version

# class MavenProjectDependency(models.Model):
#     project = models.ForeignKey(Project, blank=True)
#     repo_version = models.ForeignKey(MavenDependency, blank=True)
#     group_id = models.TextField(max_length=512, db_index=True)
#     artifact_id = models.TextField(max_lenghth=256, db_index=True)
#     version = models.TextField(max_length=256, blank=True)

