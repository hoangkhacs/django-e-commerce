from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager, Group
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number, password=None):
        if not email:
            raise ValueError('Vui lòng nhập địa chỉ email!')
        if not username:
            raise ValueError("Vui lòng nhập username!")
        if len(phone_number) != 10:
            raise ValueError("Só điện thoại không chính xác")
        #Tạo đối tượng mới
        user = self.model(
            email = self.normalize_email(email),
            phone_number = phone_number,
            username = username,
            first_name = first_name,
            last_name = last_name,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, phone_number, username, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractUser):
    username = models.CharField(max_length=200, unique=True,verbose_name="Username")
    last_name= models.CharField(max_length=200, verbose_name="Họ")
    first_name= models.CharField(max_length=200, verbose_name="Tên")
    email = models.EmailField(max_length=100, unique=True, verbose_name="email")
    phone_number = models.CharField(max_length=10, verbose_name="Số điện thoại")

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    last_login = models.DateTimeField(auto_now_add=True, verbose_name="Đăng nhập gần nhất")

    objects = MyAccountManager()

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    class Meta:
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Người dùng'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser
