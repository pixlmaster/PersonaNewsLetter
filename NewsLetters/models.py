from django.db import models

from NewsLetters.consts import JSON_EMAIL_KEY, JSON_TOPIC_NAME_KEY


# Possible Topics of the NewsLetter
class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Subscriber Details identified by a unique email
class Subscriber(models.Model):
    email = models.EmailField()
    topic_name = models.CharField(max_length=100, blank=True)  # New field to store topic name
    # topic:Subscriber = 1:n
    # Cascading deletion of subscribers in case of deletion of a topic
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        # Ensures that each (email, topic) pair is unique
        unique_together = [JSON_EMAIL_KEY, JSON_TOPIC_NAME_KEY]

    # email, topic_name should be unique
    def __str__(self):
        return self.email + " " + self.topic.name


# Content of a SINGULAR newsLetter associated with a topic
class Content(models.Model):
    # topic:content = 1:n
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content_text = models.TextField()
    send_time = models.DateTimeField()

    def __str__(self):
        return f"{self.topic.name} - {self.send_time}"
