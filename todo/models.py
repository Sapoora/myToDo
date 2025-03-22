from django.db import models
from django.contrib.auth.models import AbstractUser
from transitions import Machine
import random

class User (AbstractUser): 
    def __str__(self):
        return self.username
    
    def add_item (self, item_text):
        Item.objects.create(user=self, item_text=item_text)

class Item (models.Model):
    user = models.ForeignKey("todo.User", on_delete=models.CASCADE, related_name='items')
    item_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField("date created", auto_now_add=True)
    STATUS_CHOICES = [
        ('not done', 'Not Done'),
        ('in progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not done')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        state_names = [choice[0] for choice in Item.STATUS_CHOICES]        
        self.machine = Machine(model=self, states=state_names, initial='not done')
        self.machine.add_transition('start', 'not done', 'in progress')
        self.machine.add_transition('review', 'in progress', 'review')
        self.machine.add_transition('edit', 'review', 'in progress')
        self.machine.add_transition('end reveiw', 'review', 'done')
        self.machine.add_transition('reset', '*', 'not done')

    def set_done(self):
        self.is_done = True
        self.save()
    
    def __str__(self):
        return self.item_text
    
    