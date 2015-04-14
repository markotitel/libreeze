from django.db import models

# Create your models here.


class Developer(models.Model):
    email = models.EmailField(unique=True)
    email_verification_code = models.CharField(max_length=64, db_index=True, unique=True)
    email_verification_timestamp = models.DateTimeField(blank=True)
    email_verified = models.BooleanField(default=False)
    send_emails = models.BooleanField(default=True)
    unsubscribe_code = models.CharField(max_length=64, db_index=True)

    def __str__(self):
        return self.email


class RepoDependency(models.Model):
    namespace = models.CharField(max_length=512, db_index=True)
    name = models.CharField(max_length=256, db_index=True)
    latest = models.CharField(max_length=256)
    release = models.CharField(max_length=256)

    def key(self):
        return "%s.%s" % (self.namespace, self.name)

    def __str__(self):
        return "%s.%s:%s" % (self.namespace, self.name, self.latest)


class Project(models.Model):
    developer = models.ForeignKey(Developer, blank=True)
    namespace = models.CharField(max_length=512, db_index=True)
    name = models.CharField(max_length=256, db_index=True)
    version = models.CharField(max_length=256, db_index=True)
    send_updates = models.BooleanField(default=True)
    unsubscribe_code = models.CharField(max_length=64, db_index=True)

    def __str__(self):
        return "%s:%s" % (self.namespace, self.name)


class ProjectDependency(models.Model):
    project = models.ForeignKey(Project)
    repo_dependency = models.ForeignKey(RepoDependency, blank=True, null=True)
    namespace = models.CharField(max_length=512, db_index=True)
    name = models.CharField(max_length=256, db_index=True)
    version = models.CharField(max_length=256, blank=True)

    def key(self):
        return "%s.%s" % (self.namespace, self.name)

    def __str__(self):
        return "%s.%s:%s" % (self.namespace, self.name, self.version)
