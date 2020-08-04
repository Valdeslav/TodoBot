from datetime import datetime


class Task(object):
	def __init__(self, name="", user="", description=u'Описание отсутствует', is_done=False, date='', is_send_message=False):
		self.name = name
		self.user = user
		self.description = description
		self.is_done = is_done
		self.date = date
		self.is_send_message = is_send_message

	@staticmethod
	def from_dict(source):
		task = Task(source[u'name'], source[u'user'], source[u'description'], source[u'is_done'], source[u'date'], source[u'is_send_message'])
		return task

	def to_dict(self):
		dest = {
		u'name' : self.name,
		u'user' : self.user,
		u'description' : self.description,
		u'is_done' : self.is_done,
		u'date' : self.date,
		u'is_send_message' : self.is_send_message
		}

		return dest


	def set_done(self):
		self.is_done = True

	def to_str(self):
		value = self.name + ' - '
		if self.is_done == True:
			value += u'выполнена'
		else:
			value += u'не выполнена'
		value += u'\nвыполнить до: ' + datetime.strftime(self.date, '%d.%m.%Y/%H.%M') + u'\nОписание: ' + self.description
		return value

	def copy(self, task_to_copy):
		self.name = task_to_copy.name
		self.user = task_to_copy.user
		self.description = task_to_copy.description
		self.is_done = task_to_copy.is_done
		self.date = task_to_copy.date
		self.is_send_message = task_to_copy.is_send_message

	def __eq__(self, other):
		if isinstance(other, Task):
			return (self.name == other.name and
					self.user == other.user and
					self.description == other.description and
					self.is_done == other.is_done and
					self.date == other.date and
					self.is_send_message == other.is_send_message)
		return NotImplemented

