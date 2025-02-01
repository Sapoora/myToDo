from django.db import models
from django.contrib.auth.models import AbstractUser

class User (AbstractUser): ####

    def __str__(self):
        return self.username
    
    def add_item (self, item_text):
        Item.objects.create(username=self, item_text=item_text)


class Item (models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    item_text = models.CharField(max_length=300)
    is_done = models.BooleanField(default=0)
    pub_date = models.DateTimeField("date created", auto_now_add=True)

    def set_done(self):
        self.is_done = True
        self.save()
    
    def __str__(self):
        return self.item_text
    
    