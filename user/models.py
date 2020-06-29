from django.db import models

from djangoBackend.util.smallTools import ModelUnit

class User(models.Model):
    userId = models.AutoField(db_column='user_id', primary_key=True)
    userName = models.CharField(db_column='user_name', unique=True, max_length=50)
    password = models.CharField(db_column='password', max_length=16)
    nickname = models.CharField(db_column='nickname', max_length=100)
    gender = models.IntegerField(db_column='gender', default=1)
    birthday = models.DateField(db_column='birthday', blank=True, null=True)
    email = models.CharField(db_column='email', unique=True, max_length=30)
    loginTime = models.DateTimeField(db_column='login_time', blank=True, null=True)
    registerTime = models.DateTimeField(db_column='register_time', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'

class ChatMessage(models.Model):
    chatMessageId = models.AutoField(db_column='chat_message_id', primary_key=True)
    content = models.TextField(db_column='content')
    status = models.IntegerField(db_column='status')
    time = models.DateTimeField(db_column='time')
    sendId = models.ForeignKey(db_column='send_id', to=User, to_field=ModelUnit.getOneField(User.userId), related_name='send_id_fk', on_delete=models.CASCADE)
    receiveId = models.ForeignKey(db_column='receive_id', to=User, to_field=ModelUnit.getOneField(User.userId), related_name='receive_id_fk', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'chat_message'