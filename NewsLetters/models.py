from django.db import models


# Possible Topics of the NewsLetter
class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Subscriber Details identified by a unique email
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    # # topic:Subscriber = 1:n
    # Cascading deletion of subscribers in case of deletion of a topic
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.email


# Content of a SINGULAR newsLetter associated with a topic
class Content(models.Model):
    # topic:content = 1:n
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content_text = models.TextField()
    send_time = models.DateTimeField()

    def __str__(self):
        return f"{self.topic.name} - {self.send_time}"
