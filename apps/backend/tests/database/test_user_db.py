
import unittest
import firebase_admin
from firebase_admin import credentials, db, firestore

from src.database.db_utils import get_path


class TestFirebaseDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cred = credentials.Certificate(get_path('key.json'))
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db

    @classmethod
    def tearDownClass(cls):
        
        firebase_admin.delete_app(firebase_admin.get_app())

    def test_write_to_database(self):
        
        ref = db.reference('/')

        
        ref.child('users').child('user1').set({
            'username': 'test_user',
            'email': 'test@example.com'
        })

        
        snapshot = ref.child('users').child('user1').get()

        
        self.assertEqual(snapshot['username'], 'test_user')
        self.assertEqual(snapshot['email'], 'test@example.com')

    def test_delete_from_database(self):
        
        ref = db.reference('/')

        
        ref.child('users').child('user1').delete()

        
        snapshot = ref.child('users').child('user1').get()

        
        self.assertIsNone(snapshot)


if __name__ == '__main__':
    unittest.main()
