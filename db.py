import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred=credentials.Certificate('todobotfirebase-firebase-adminsdk-npghl-cdadbeff71.json')
firebase_admin.initialize_app(cred)
db=firestore.client()
data={
	u'name': u'Minsk',
	u'state': u'none',
	u'country': u'Belarus'
}
db.collection(u'cities').document(u'Minsk').set(data)
