from django.db import models

# Create your models here.


class Developer(models.Model):
    email = models.EmailField(unique=True)
    email_verification_code = models.CharField(max_length=64, db_index=True, unique=True)
    email_verification_timestamp = models.DateTimeField(blank=True)
    email_verified = models.BooleanField(default=False)
    send_emails = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class MavenRepoDependency(models.Model):
    group_id = models.CharField(max_length=512, db_index=True)
    artifact_id = models.CharField(max_length=256, db_index=True)
    latest = models.CharField(max_length=256)
    release = models.CharField(max_length=256)

    def __str__(self):
        return "%s.%s:%s" % (self.group_id, self.artifact_id, self.latest)


class MavenProject(models.Model):
    developer = models.ForeignKey(Developer, blank=True)
    group_id = models.CharField(max_length=512, db_index=True)
    artifact_id = models.CharField(max_length=256, db_index=True)
    version = models.CharField(max_length=256, db_index=True)
    send_updates = models.BooleanField(default=True)
    unsubscribe_code = models.CharField(max_length=64, db_index=True)

    def __str__(self):
        return "%s:%s" % (self.group_id, self.artifact_id)


class MavenProjectDependency(models.Model):
    project = models.ForeignKey(MavenProject)
    repo_dependency = models.ForeignKey(MavenRepoDependency, blank=True, null=True)
    group_id = models.CharField(max_length=512, db_index=True)
    artifact_id = models.CharField(max_length=256, db_index=True)
    version = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return "%s.%s:%s" % (self.group_id, self.artifact_id, self.version)
