from django.db import models

class Project(models.Model):
    project_name = models.CharField(max_length=50, blank=True, null=True)
    item_type = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.project_name

class ItemType(models.Model):
    item_type = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.item_type
    class Meta:
        verbose_name = 'Device Type'

class Item(models.Model):
    project_name = models.CharField(max_length=50, blank=True, null=True)
    item_type = models.CharField(max_length=50, blank=True, null=True)
    project_description = models.TextField()
    name = models.CharField(max_length=40, blank=True, null=True)
    mac_img = models.ImageField(upload_to='images/')
    created_at = models.DateField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.project_name


class Device(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    mac = models.CharField(max_length=60, null=True, blank=True)
    img_path = models.ImageField(upload_to='images/',null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.mac
    

