import os
from my_app import create_app, db, babel
import unittest
import tempfile


class CatalogTestCase(unittest.TestCase):

    def setUp(self):
        test_config = {}
        self.test_db_file = tempfile.mkstemp()[1]
        test_config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.test_db_file
        test_config['TESTING'] = True

        self.app = create_app(test_config)
        db.init_app(self.app)
        babel.init_app(self.app)
        
        with self.app.app_context():
            db.create_all()

        from my_app.catalog.views import catalog
        self.app.register_blueprint(catalog)

        self.client = self.app.test_client()

    def tearDown(self):
        os.remove(self.test_db_file)

    def test_home(self):
        rv = self.client.get('/')
        self.assertEqual(rv.status_code, 200)


if __name__ == '__main__':
    unittest.main()