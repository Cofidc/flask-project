from os import path
import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

class Todoclient:
    def __init__(self,base_url=None):
        self.base_url = base_url or Config.BASE_URL
        self.session = requests.Session()

    def _request(self,method,url,**kwargs):
        url = f"{self.base_url}/{url.lstrip('/')}"
        logger.info(f"发起{method}请求:{url}")
        if 'json' in kwargs:
            logger.debug(f"请求体：{kwargs['json']}")

        resp = self.session.request(method,url,timeout=Config.TIMEOUT,**kwargs)

        logger.info(f"响应状态码：{resp.status_code}")
        if resp.text:
            logger.debug(f"响应体：{resp.text}")
        return resp
    
    def get(self):
        return self._request('GET','todos')
    
    def create(self,title):
        return self._request('POST','todos',json={'title':title})
    
    def get_one(self,id):
        return self._request('GET',f'todos/{id}')
    
    def update(self,id,**kwargs):
        return self._request('PUT',f'todos/{id}',json=kwargs)

    def delete(self,id):
        return self._request('DELETE',f'todos/{id}')
    