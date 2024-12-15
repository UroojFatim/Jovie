from django.db import models

# Candidate Model
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    unique_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Question Model
class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField()
    marks = models.IntegerField()

    def __str__(self):
        return self.text

# Option Model
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.text} ({self.marks} marks)"

# Result Model
class Result(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    percentage = models.FloatField()
    suggestions = models.TextField()

    def __str__(self):
        return f"{self.candidate.name} - {self.percentage}%"
    
    
class Report(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    saved = models.BooleanField(default=False)  # Whether the report is saved

    def __str__(self):
        return f'Report for {self.candidate.name} - {self.result.percentage}%'
    
    
