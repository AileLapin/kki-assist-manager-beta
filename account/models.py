from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin)


class MyUserManager(BaseUserManager):
    def create_user(self, stu_num, password=None,
                    last_name=None, first_name=None, nickname=None):
        if not stu_num:
            raise ValueError("Users must have an student's number")

        user = self.model(stu_num=stu_num,
                          last_name=last_name,
                          first_name=first_name,
                          nickname=nickname)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, stu_num, password):
        user = self.create_user(stu_num, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'ユーザ'
        verbose_name_plural = 'ユーザ'

    stu_num = models.CharField(verbose_name='学籍番号',
                               unique=True, max_length=30, default="")
    last_name = models.CharField(verbose_name='苗字',
                                 max_length=30, default=None, null=True)
    first_name = models.CharField(verbose_name='名前',
                                  max_length=30, default=None, null=True)
    nickname = models.CharField(verbose_name='ニックネーム',
                                max_length=30, default=None, null=True)
    data_joind = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'stu_num'
    # REQUIRED_FIELDS = ['last_name', 'first_name']

    def __str__(self):
        return self.stu_num + ' : ' + str(self.last_name) + ' ' + str(self.first_name)
