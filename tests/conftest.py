from datetime import datetime

from dateutil.tz import tzutc, tzlocal
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pytest

from task import Task

@pytest.fixture
def make_dict():
	date = datetime(2020, 3, 5, 12, 30, 0) 
	date = date.replace(tzinfo=tzutc())
	return {
		u'name' : 'task1',
		u'user' : 123456789,
		u'description' : 'description1',
		u'is_done' : False,
		u'date' : date,
		u'is_send_message' : True
	}


@pytest.fixture
def make_task():
	date = datetime(2020, 3, 5, 12, 30, 0) 
	date = date.replace(tzinfo=tzutc())
	return Task('task1', 123456789, 'description1', False, date, True)


@pytest.fixture
def make_task_to_copy():
	date=datetime(2021, 3, 5, 12, 30, 0)
	date = date.replace(tzinfo=tzutc())
	return Task('copied task', 987654321, 'new description', True, date, False)


@pytest.fixture (scope = "module" ) 
def init_firebase():
	cred = credentials.Certificate('../todobotfirebase-firebase-adminsdk-npghl-cdadbeff71.json')
	firebase_admin.initialize_app(cred)
	db = firestore.client()
	return db


@pytest.fixture
def make_task_list():
	date = datetime(2020, 3, 5, 12, 30, 0) 
	date = date.replace(tzinfo=tzutc())
	return [Task('task1', 123456789, 'description1', False, date, True)]





