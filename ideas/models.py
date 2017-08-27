from django.db import models

# Create your models here.
class Idea(models.Model):
    label = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField()

    def __str__(self):
        return self.label

class Inspiration(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    label = models.CharField(max_length=200)
    category = models.CharField(
        max_length=200,
        blank=True
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.label

class Concept(models.Model):
    category = models.CharField(max_length=200)
    label = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.label
