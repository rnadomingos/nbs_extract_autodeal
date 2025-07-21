import unittest
from unittest.mock import patch
from app.infra.load_settings import env_settings
import os

class TestLoadSettings(unittest.TestCase):
   def test_ensure_load_settings_returns_correct_values_when_db_oracle(self):
         """ Ensure load settings returns correct values"""
         database = 'ORACLE'
         config = env_settings(database)
         
         mock_data = {
            'ORACLE_HOST': 'localhost',
            'ORACLE_USERNAME': 'admin',
            'ORACLE_PASSWORD': 'secret',
            'ORACLE_SERVICE': 'XE',
            'ORACLE_PORT': '1521',
            'ORACLE_DRIVER': 'oracle+cx_oracle',
            }
         
         with (
            patch("app.infra.load_settings.load_dotenv"),
            patch.dict(os.environ, mock_data)):
            resultado = config.load_settings()
      
         assert resultado == {
            "db_host": 'localhost',
            "db_user": 'admin',
            "db_pass": 'secret',
            "db_service": 'XE',
            "db_port": '1521',
            "db_driver": 'oracle+cx_oracle'
         }
   
   
   def test_ensure_load_settings_returns_correct_values_when_db_postgres(self):
         """ Ensure load settings returns correct values"""
         database = 'POSTGRES'
         config = env_settings(database)
         
         mock_data = {
            'POSTGRES_HOST': 'localhost',
            'POSTGRES_USERNAME': 'admin',
            'POSTGRES_PASSWORD': 'secret',
            'POSTGRES_SERVICE': 'XE',
            'POSTGRES_PORT': '1521',
            'POSTGRES_DRIVER': 'None',
            }
         
         with (
            patch("app.infra.load_settings.load_dotenv"),
            patch.dict(os.environ, mock_data)):
            resultado = config.load_settings()
      
         assert resultado == {
            "db_host": 'localhost',
            "db_user": 'admin',
            "db_pass": 'secret',
            "db_service": 'XE',
            "db_port": '1521',
            "db_driver": 'None',
         }

   def test_ensure_raises_when_database_is_wrong(self):
      with self.assertRaises(ValueError) as exc_info:
          env_settings('sqlserver')
      self.assertEqual(str(exc_info.exception), 'Invalid database type')
      