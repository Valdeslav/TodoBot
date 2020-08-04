from datetime import datetime, timezone

import pytest

from task import Task


def test_from_dict(make_dict, make_task):
	assert Task.from_dict(make_dict) == make_task


def test_to_dict(make_task, make_dict):
	assert make_task.to_dict() == make_dict


def test_to_str(make_task):
	assert make_task.to_str() == 'task1 - не выполнена\nвыполнить до: 05.03.2020/12.30\nОписание: description1'


def test_copy(make_task, make_task_to_copy):
	task=make_task
	task.copy(make_task_to_copy)
	assert task == make_task_to_copy

