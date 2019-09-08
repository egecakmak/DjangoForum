from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Thread(models.Model):
    title = models.CharField(max_length=30)
    pub_date = models.DateTimeField()
    update_date = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Post(models.Model):
    post = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()

# class MessageContainer(models.Model):
#     title = models.CharField(max_length=20, null=True)
#     side_1 = models.ForeignKey(User, related_name="side_1", null=True, on_delete=models.CASCADE)
#     side_2 = models.ForeignKey(User, related_name="side_2", null=True, on_delete=models.CASCADE)
#
# class Message(models.Model):
#     recipient = models.ForeignKey(User, related_name="recipient", null=True, on_delete=models.CASCADE)
#     sender = models.ForeignKey(User, related_name="sender", null=True, on_delete=models.CASCADE)
#     text = models.TextField()
#     pub_date = models.DateTimeField()
#     message_container = models.ForeignKey(MessageContainer, null=True, on_delete=models.CASCADE)