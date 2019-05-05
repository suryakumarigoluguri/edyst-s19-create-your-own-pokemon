import unittest
import os
import json
from app import db,app

 
TEST_DB = 'test.sqlite'

class TestsPokemon(unittest.TestCase):

    @classmethod
    def setUpClass(self): 
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
    
    @classmethod 
    def tearDownClass(self): 
        db.drop_all()

    
    def test_add_pokemon(self):
        print("---------Testing of pokemon post operation----------")
        pk_data={ "pokemon": {"name": "bulbasaur","sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                                    "cardColours": {"fg": "#eeeeee","bg": "#3e3e3e","desc": "#111111" }}}
        
        expected_data={ "pokemon": {"id": 1,"name": "bulbasaur","sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                                    "cardColours": {"fg": "#eeeeee","bg": "#3e3e3e","desc": "#111111" }}}
        actual_data=self.app.post("http://127.0.0.1:8006/api/pokemon/", data = json.dumps(pk_data), content_type='application/json')
        self.assertEqual(expected_data,json.loads(actual_data.data))
        print("---------Testing of pokemon post is success----------")

    def test_get_pokemon(self):
        print("---------Testing of pokemon get operation----------")
        expected_data={ "pokemon": {"id": 1,"name": "bulbasaur","sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                                    "cardColours": {"fg": "#eeeeee","bg": "#3e3e3e","desc": "#111111" }}}
        actual_data=self.app.get("http://127.0.0.1:8006/api/pokemon/1")
        self.assertEqual(expected_data,json.loads(actual_data.data))
        print("---------Testing of pokemon get is success----------")

    def test_update_pokemon(self):
        print("---------Testing of pokemon patch operation----------")
        pk_data={ "pokemon": {"name": "bulbasaur_new_name","sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                                    "cardColours": {"fg": "#eeeeee","bg": "#3e3e3e","desc": "#111111" }}}
        
        expected_data={ "pokemon": {"id": 1,"name": "bulbasaur_new_name","sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                                    "cardColours": {"fg": "#eeeeee","bg": "#3e3e3e","desc": "#111111" }}}
        actual_data=self.app.patch("http://127.0.0.1:8006/api/pokemon/1", data = json.dumps(pk_data), content_type='application/json')
        self.assertEqual(expected_data,json.loads(actual_data.data))
        print("---------Testing of pokemon patch is success----------")

    def test_zdelete_pokemon(self):
        print("---------Testing of pokemon delete operation----------")
        expected_data={ "pokemon": {"id": 1,"name": "bulbasaur_new_name","sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                                    "cardColours": {"fg": "#eeeeee","bg": "#3e3e3e","desc": "#111111" }}}
        actual_data=self.app.get("http://127.0.0.1:8006/api/pokemon/1")
        self.assertEqual(expected_data,json.loads(actual_data.data))
        print("---------Testing of pokemon delete is success----------")


if __name__ == '__main__':
    unittest.main()
