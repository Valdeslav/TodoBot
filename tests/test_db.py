from datetime import datetime

from dateutil.tz import tzutc, tzlocal
import pytest

from task import Task
import db


def test_add_user(init_firebase):
	db.add_user(123456789, init_firebase)
	doc_ref = init_firebase.collection('users').document('123456789')
	assert doc_ref.get().to_dict() == {'id' : 123456789}


def test_add_task_firebase(make_task, make_dict, init_firebase):
	db.addTask_firebase(make_task, init_firebase)
	doc_ref = init_firebase.collection('123456789').document('task1')
	assert doc_ref.get().to_dict() == make_dict


def test_get_all_firebase(init_firebase, make_task_list):
	assert db.getAll_firebase(123456789, init_firebase) == make_task_list


def task_param(name='task1', user=123456789, is_done=False, description='description1', 
			   date=datetime(2020, 3, 5, 12, 30, 0)): 
	date = date.replace(tzinfo=tzutc())
	return Task(name, user, description, is_done, date, True)


@pytest.mark.parametrize("inp, outp", [('task1', task_param()), ('some task', False)])
def test_get_firebase(init_firebase, inp, outp):
	assert db.get_firebase(123456789, inp, init_firebase) == outp


@pytest.mark.parametrize("value", [(task_param(description='description2')), (task_param(date=datetime(2019, 4, 5, 0, 30, 0)))])
def test_update_firebase(init_firebase, value):
	db.update_firebase(123456789, value, init_firebase)
	doc_ref = init_firebase.collection('123456789').document('task1')
	assert Task.from_dict(doc_ref.get().to_dict()) == value


@pytest.mark.parametrize("inp, outp", [(task_param(), task_param(is_done=True))])
def test_done_firebase(init_firebase, inp, outp):
	init_firebase.collection('123456789').document('task1').set(inp.to_dict())
	db.done_firebase(123456789, 'task1',init_firebase)
	doc_ref = init_firebase.collection('123456789').document('task1')
	assert Task.from_dict(doc_ref.get().to_dict()) == outp


def test_delete_firebase(init_firebase):
	db.delete_firebase(123456789, 'task1', init_firebase)
	doc_ref = init_firebase.collection('123456789').document('task1')
	assert doc_ref.get().to_dict() == None