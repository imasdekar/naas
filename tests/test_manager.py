from naas.types import t_notebook
from naas.manager import Manager
from shutil import copy2
import pytest
import uuid
import os

user_folder_name = 'test_user_folder'
proxy_url = 'proxy.naas.com'
test_file = 'demo_file.py'
token = 'test_token'
test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__))
, test_file)
os.environ["JUPYTERHUB_URL"] = 'test.naas.com'
os.environ["JUPYTERHUB_USER"] = 'TEST_USER'
os.environ["JUPYTERHUB_API_TOKEN"] = 'TESTAPIKEY'
os.environ["PUBLIC_PROXY_API"] = proxy_url

def test_init(tmp_path):
    path_srv_root = os.path.join(str(tmp_path), user_folder_name)
    os.environ["JUPYTER_SERVER_ROOT"] = path_srv_root
    manager = Manager()
    assert os.path.exists(os.path.join(path_srv_root, '.naas'))
    assert len(manager.get_naas()) == 0

def test_nb_path(tmp_path):
    path_srv_root = os.path.join(str(tmp_path), user_folder_name)
    os.environ["JUPYTER_SERVER_ROOT"] = path_srv_root
    # TODO need better test
    manager = Manager()
    assert manager.notebook_path() == None

def test_get_path(tmp_path):
    path_srv_root = os.path.join(str(tmp_path), user_folder_name)
    os.environ["JUPYTER_SERVER_ROOT"] = path_srv_root
    # TODO need better test
    manager = Manager()
    assert manager.get_path(test_file_path) == test_file_path


def test_copy_file(runner, tmp_path,requests_mock):
    path_srv_root = os.path.join(str(tmp_path), user_folder_name)
    os.environ["JUPYTER_SERVER_ROOT"] = path_srv_root
    os.environ["JUPYTERHUB_USER"] = 'joyvan'
    os.environ["JUPYTERHUB_URL"] = 'localhost:5000'
    os.environ["PUBLIC_PROXY_API"] = 'proxy:5000'

    new_path = os.path.join(path_srv_root, test_file)
    os.makedirs(os.path.dirname(new_path))
    copy2(test_file_path, new_path)
    manager = Manager()
    prod_path = manager.get_prod_path(test_file_path)
    obj = {"type": t_notebook, "path": new_path, "params": {}, "value": token}
    requests_mock.post(f'http://{os.environ["JUPYTERHUB_URL"]}/jobs', json=[obj])

    manager.add_prod(obj, True)
    assert os.path.exists(prod_path)
    manager.get_prod(new_path)
    dev_dir = os.path.dirname(new_path)
    dev_finename = os.path.basename(new_path)
    secure_path = os.path.join(dev_dir, f'prod_{dev_finename}')
    assert os.path.exists(secure_path)
    manager.del_prod(obj, True)
    assert os.path.exists(prod_path)
    
    

    # def __del_copy_file_in_prod(self, path):

    # def get_naas(self):
    
    # def get_value(self, path, obj_type):

    # def is_already_use(self, obj):

    # def get_prod(self, path):
                
    # def get_output(self, path):
        
    # def clear_output(self, path):
        
    # def list_history(self, path):
                
    # def get_history(self, path, histo):
                
    # def clear_history(self, path, histo=None):  

    # def add_prod(self, obj, silent):

    # def del_prod(self, obj, silent):

