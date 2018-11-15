

from django.db import models
from django.contrib.auth.models import User

import os

# #extend User model to have things like profile photos etc.
# class HotPotUser(models.Model):
# 	user = models.OneToOneField(User, on_delete = models.CASCADE)

# single room entry represent: one specific user enters one room
# get all current user of room (pk = A):
# 	user = SingleRoomEntry.objects.filter(room_pk = A, has_left = False).user_set.all()

# get the rooms own by this user
#	rooms = Room.objects.filter(owner = request.user)

def getDefaultUser():
	return 1;

class Room(models.Model):
	owner = models.ForeignKey(User, on_delete = models.CASCADE, blank = True);
	name =  models.CharField(max_length = 42,default = 'myRoom')
	create_date = models.DateTimeField(auto_now = True)
	# listeners = models.ManyToManyField(HotPotUser, related_name='+')
	cover_pic = models.ImageField(upload_to ='room-photo', blank = True,
			 	default = 'room-photo/logo.png',
							)
	description = models.TextField(max_length = 420, blank = True,
						)

	thumbs_up = models.IntegerField(default = 0)

	def __str__(self):
		return self.name
	
class RoomHistory(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	join_date = models.DateTimeField(auto_now = True)
	has_left = models.BooleanField(default=False)
	visited_room = models.ForeignKey(Room, on_delete = models.CASCADE)

	@staticmethod
	def getCurrentListeners(room, time = "1970-01-01T00:00+00:00"):
		return RoomHistory.objects.filter(room = room, has_left = False, join_date__gt = time).user_set.all()

	@staticmethod
	def getVistedRooms(user,time = "1970-01-01T00:00+00:00" ):
		history = RoomHistory.objects.filter(user = user, join_date__gt = time)
		rooms = []
		for i in history:
			rooms.append(i.visited_room)

	def leaveRoom(self):
		self.has_left = True
		return self.has_left

	def __str__(self):
		return self.user.username

