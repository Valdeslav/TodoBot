import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from task import Task

def init_firebase(token):
	cred=credentials.Certificate(token)
	firebase_admin.initialize_app(cred)
	db=firestore.client()
	return db

def add_user(user, db):
	db.collection(u'users').document(str(user)).set({'id' : user})

def addTask_firebase(data, db):
	db.collection(str(data.user)).document(data.name).set(data.to_dict())

def getAll_firebase(user, db):
	tasks=db.collection(str(user)).stream()
	return tasks

def get_firebase(user, name, db):
	doc_ref=db.collection(str(user)).document(name)
	doc=doc_ref.get()
	if doc.exists:
		task=Task.from_dict(doc.to_dict())
		return task
	else:
		return False

def update_firebase(user, task, db):
	doc_ref=db.collection(str(user)).document(task.name)
	doc_ref.update({u'description' : task.description,
					u'date' : task.date})

def delete_firebase(user, name, db):
	db.collection(str(user)).document(name).delete()

def done_firebase(user, name, db):
	doc_ref=db.collection(str(user)).document(name)
	doc_ref.update({u'is_done' : True})

def get_users(db):
	docs=db.collection(u'users').stream()
	return docs