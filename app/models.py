from django.db import models

# Create your models here.


class Developer(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


class MavenRepoDependency(models.Model):
    group_id = models.TextField(max_length=512, db_index=True)
    artifact_id = models.TextField(max_length=256, db_index=True)
    latest = models.TextField(max_length=256)
    release = models.TextField(max_length=256)

    def __str__(self):
        return "Maven repo dependency: %s.%s:%s" % (self.group_id, self.artifact_id, self.latest)


class MavenProject(models.Model):
    developer = models.ForeignKey(Developer, blank=True)
    group_id = models.TextField(max_length=512, db_index=True)
    artifact_id = models.TextField(max_length=256, db_index=True)

    def __str__(self):
        return "Project: %s.%s" % (self.group_id, self.artifact_id)


class MavenProjectDependency(models.Model):
    project = models.ForeignKey(MavenProject)
    repo_version = models.ForeignKey(MavenRepoDependency, blank=True)
    group_id = models.TextField(max_length=512, db_index=True)
    artifact_id = models.TextField(max_length=256, db_index=True)
    version = models.TextField(max_length=256, blank=True)

    def __str__(self):
        return "Maven project dependency: %s.%s:%s" % (self.group_id, self.artifact_id, self.version)
