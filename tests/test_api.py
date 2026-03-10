import pytest
import json
import allure
from assertions import assert_status_code, assert_json_key ,assert_todo_equal

def load_todo_data():
    with open('tests/data.json','r',encoding='utf-8')as f:
        return json.load(f)
    
@allure.feature('待办事项API')

@allure.story('创建待办事项')
class TestCreateTodo:
    @allure.title('创建待办事项')
    def test_create_todo(self,todo_client):
        title = '测试待办事项'
        with allure.step(f'创建待办事项：{title}'):
            resp = todo_client.create(title)
        with allure.step('验证创建结果'):
            assert_status_code(resp,201)
            data = resp.json()
            assert_json_key(data,'id','title','completed')
            assert_todo_equal(data,title,False)

    @allure.title('数据驱动测试')
    @pytest.mark.parametrize('data',load_todo_data())
    def test_create_with_data(self,todo_client,data):
        title = data['title']
        expected_status = data['expected_status']
        with allure.step(f'创建待办事项：{title}'):
            resp = todo_client.create(title)
        with allure.step(f'验证状态码：{expected_status}'):
            assert_status_code(resp,expected_status)
        if expected_status == 201:
            assert resp.json()['title']==title

@allure.story("获取代办")
class TestGetTodo:
    @allure.title("获取所有待办事项")
    def test_get_todos(self,todo_client,clean_todos):
        todo_client.create("待办事项1")
        todo_client.create("待办事项2")
        resp = todo_client.get()
        assert_status_code(resp,200)
        data = resp.json()
        assert isinstance(data,list)
        assert len(data) == 2

    @allure.title("获取单个待办事项")
    def test_get_todo(self,todo_client,clean_todos):
        c_resp = todo_client.create("单个任务")
        todo_id = c_resp.json()['id']

        resp = todo_client.get_one(todo_id)
        assert_status_code(resp,200)
        assert_todo_equal(resp.json(),expected_title='单个任务')

    @allure.title("获取不存在的待办")
    def test_get_no_todo(self, todo_client):
        resp = todo_client.get_one(99999)
        assert_status_code(resp, 404)

@allure.story("更新待办")
class TestUpdateTodo:
    @allure.title("更新待办标题")
    def test_update_title_todo(self,todo_client,clean_todos):
        c_resp = todo_client.create("old")
        todo_id = c_resp.json()['id']

        resp = todo_client.update(todo_id,title='new')
        assert_status_code(resp,200)
        assert_todo_equal(resp.json(),expected_title='new')

    @allure.title("更新待办完成状态")
    def test_update_completed_todo(self,todo_client,clean_todos):
        c_resp = todo_client.create("任务")
        todo_id = c_resp.json()['id']

        resp = todo_client.update(todo_id,completed=True)
        assert_status_code(resp,200)
        assert_todo_equal(resp.json(),expected_completed=True)

    @allure.title("更新不存在待办")
    def test_update_no_todo(self,todo_client,clean_todos):
        resp = todo_client.update(9999)
        assert_status_code(resp,404)

@allure.story("删除待办")
class TestDeleteTodo:
    @allure.title("删除待办事项")
    def test_delete_todo(self,todo_client,clean_todos):
        c_resp = todo_client.create("待办事项")
        todo_id = c_resp.json()['id']
        resp = todo_client.delete(todo_id)
        assert_status_code(resp,204)
        g_resp = todo_client.get_one(todo_id)
        assert_status_code(g_resp,404)

    @allure.title("删除不存在的待办")
    def test_delete_no_todo(self, todo_client):
        resp = todo_client.delete(99999)
        assert_status_code(resp, 404)

