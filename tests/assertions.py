def assert_status_code(resp,expected_code):
    assert resp.status_code == expected_code,\
        f"期望状态码{expected_code}，状态码为{resp.status_code}"
    
def assert_json_key(data,*keys):
    for key in keys:
        assert key in data,f"响应体中缺少键{key}"

def assert_todo_equal(todo,expected_title=None,expected_completed=None):
    if expected_title is not None:
        assert todo['title'] == expected_title,f"期望标题{expected_title}，实际标题{todo['title']}"
    if expected_completed is not None:
        assert todo['completed'] == expected_completed,f"期望完成状态{expected_completed}，实际完成状态{todo['completed']}"
