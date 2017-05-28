from django.db import models
from django.db.models.aggregates import Func
from django.contrib.postgres.fields import JSONField
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from re import RegexFlag


class ObjectAtPath(Func):

    function = '#>'
    template = "%(expressions)s%(function)s'{%(path)s}'"
    arity = 1

    def __init__(self, expression, path, **extra):
        # if path is a list, convert it to a comma separated string
        if isinstance(path, (list, tuple)):
            path = ','.join(path)
        super().__init__(expression, path=path, **extra)


class LogFile(models.Model):

    log_file = models.FileField()


class Play(models.Model):
    """
    An Ansible play can represent the start/finish of a playbook or play. This model is 
    not yet complete, but represents enough structre for a proof of concept.
    """
    name = models.CharField(max_length=200)

    hostip = models.GenericIPAddressField(protocol="both", unpack_ipv4=True, default="0.0.0.0")

    hostname = models.CharField(max_length=250,
                                validators=[RegexValidator(regex=r"^[a-z0-9]([a-z0-9-\.]{0,61}[a-z0-9])?$",
                                                           flags=RegexFlag.IGNORECASE)],
                                default="nohost")

    data = JSONField()

    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User)


class Task(models.Model):
    """
    A task is an Ansible step in a playbook and this model can represent
    the start of a task or the results from a task. This model is 
    not yet complete, but represents enough structre for a proof of concept.
    """

    name = models.CharField(max_length=250)

    hostip = models.GenericIPAddressField(protocol="both", unpack_ipv4=True, default="0.0.0.0")

    hostname = models.CharField(max_length=250,
                                validators=[RegexValidator(regex=r"^[a-z0-9]([a-z0-9-\.]{0,61}[a-z0-9])?$",
                                                           flags=RegexFlag.IGNORECASE)],
                                default="nohost")

    data = JSONField()

    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User)


class Event(models.Model):
    """
    An Ansible event can represent internal actions that are not the result of a task
    or play. This model is not yet complete, but represents enough structre for a proof
    of concept.
    """

    name = models.CharField(max_length=200)

    hostip = models.GenericIPAddressField(protocol="both", unpack_ipv4=True, default="0.0.0.0")

    hostname = models.CharField(max_length=250,
                                validators=[RegexValidator(regex=r"^[a-z0-9]([a-z0-9-\.]{0,61}[a-z0-9])?$",
                                                           flags=RegexFlag.IGNORECASE)],
                                default="nohost")

    data = JSONField()

    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User)
