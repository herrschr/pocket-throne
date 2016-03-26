__all__ = ('Notification')

from datetime import datetime

from pocketthrone.entities.enum import MessageImportancy, NotificationCategory

class Notification:
	_id = -1

	# properties defining unset type & category of this notification
	importancy = None
	category = None

	# title & message content
	title = "<untitled>"
	body = "<no content>"

	def __init__(self, _id, importancy=MessageImportancy.IMPORTANCY_UNSET, category=NotificationCategory.NOTI_UNSET, body=None, title=None):
		# set initial properties
		self._id = _id
		self.importancy = importancy
		self.category = category
		self.title = title
		self.content = content

	def get_importancy(self):
		'''returns the MessageImportancy of this Notification'''
		return self.importancy

	def set_importancy(self, value):
		'''sets MessageImportancy of this Notification'''
		self.importancy = value

	def get_category(self):
		'''returns the NotificationCategory of this Notification'''
		return self.category

	def set_category(self, value):
		'''sets NotificationCategory of this Notfication'''
		self.category = value

	def set_title_n_body(self, title, body):
		self.title = title
		self.body = body
