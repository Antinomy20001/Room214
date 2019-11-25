from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.timezone import now
import struct

class TitleType:
    STUDENT = 'STUDENT'
    TEACHAR = 'TEACHAR'

class Person(models.Model):
    name = models.CharField(max_length=200)
    title = models.TextField(default=TitleType.STUDENT)
    student_id = models.TextField(null=True)

    def to_json(self):
        data = {
            'name':self.name,
            'title':self.title,
        }
        if self.student_id is not None:
            data['student_id'] = self.student_id
        return data

    class Meta:
        db_table = 'Person'

class Face(models.Model):
    vector = models.BinaryField(max_length=4 * 512,blank=True,null=False)
    created_at = models.DateTimeField(auto_now=True)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, null=True)

    def to_json(self):
        data = {
            'vector': struct.unpack('f'*512,self.vector),
            'created_at': int(self.created_at.timestamp()),
            'label': self.person.pk
        }
        return data

    class Meta:
        db_table = 'Face'


class UserManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        return self.get(**{f"{self.model.USERNAME_FIELD}__iexact": username})

    def create_user(self, username, password=None):
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    @property
    def is_staff(self):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'User'
