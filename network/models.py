from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import ManyToOneRel
import django.utils.timezone

class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    post_txt = models.CharField(max_length=280)
    num_likes = models.IntegerField(default=0)
    liked = models.BooleanField(default=False)
    likers = models.ManyToManyField('User', blank=True)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)
 
    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.post,
            "post_txt": self.post_txt,
            "num_likes": self.num_likes,
            "liked": self.liked,
            "likers": [poster.post for poster in self.likers.all()],
            "timestamp": self.timestamp.strftime("%b %d %y, %I:%M %p")
        }
        
            
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    
#class Likes_list(models.Model):
#    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
#    liker = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
#    
#    def __str__(self) :
#        return f'{self.liker} likes: {self.liked_post}.'