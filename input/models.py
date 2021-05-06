from django.db import models

class Project(models.Model):
    project_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

class Item(models.Model):
    project_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    mac_img = models.ImageField(upload_to='images/')
    created_at = models.DateField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)


class macItem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    mac = models.CharField(max_length=60, null=True, blank=True)
    img_path = models.ImageField(upload_to='images/',null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    

