from django.db import models

# Create your models here.
class PlayList(models.Model):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		