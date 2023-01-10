from django.db import models

# Create your models here.
class Fruit(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    havest = models.CharField(max_length=20)
    content = models.CharField(max_length=512)
    price = models.IntegerField()
    calorie = models.IntegerField()
    create_at = models.DateTimeField()
    upload_at = models.DateTimeField()
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Fruit'


class Fruitorderbill(models.Model):
    id = models.BigAutoField(primary_key=True)
    fruit = models.ForeignKey(Fruit, models.DO_NOTHING)
    orderbill = models.ForeignKey('Orderbill', models.DO_NOTHING)
    count = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'FruitOrderBill'


class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    s3_image_url = models.CharField(max_length=512)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Image'


class Orderbill(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ForeignKey(Image, models.DO_NOTHING)
    date_of_purchase = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'OrderBill'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'