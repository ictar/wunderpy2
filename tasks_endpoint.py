'''
Encapsulates all tasks that can be run against the 'tasks' endpoint
'''
def get_tasks(client, list_id, completed=False):
    ''' Gets un/completed tasks for the given list ID '''
    params = { 
            wp_model.Task.list_id : str(list_id), 
            wp_model.Task.completed : completed 
            }
    response = client.authenticated_request(client.api.Endpoints.TASKS, params=params)
    return response.json()

def get_task(client, task_id):
    ''' Gets task information for the given ID '''
    endpoint = '/'.join([client.api.Endpoints.TASKS, str(task_id)])
    response = client.authenticated_request(endpoint)
    return response.json()

def create_task(client, list_id, title, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None):
    ''' 
    Creates a task in the given list 

    See https://developer.wunderlist.com/documentation/endpoints/task for detailed parameter information
    '''
    if len(title) > client.api.MAX_TASK_TITLE_LENGTH:
        raise ValueError("Title cannot be longer than {} characters".format(client.api.MAX_TASK_TITLE_LENGTH))
    if (recurrence_type is None and recurrence_count is not None) or (recurrence_type is not None and recurrence_count is None):
        raise ValueError("recurrence_type and recurrence_count are required are required together")
    data = {
            wp_model.Task.list_id : int(list_id) if list_id else None,
            wp_model.Task.title : title,
            wp_model.Task.assignee_id : int(assignee_id) if assignee_id else None,
            wp_model.Task.completed : completed,
            wp_model.Task.recurrence_type : recurrence_type,
            wp_model.Task.recurrence_count : int(recurrence_count) if recurrence_count else None,
            wp_model.Task.due_date : due_date,
            wp_model.Task.starred : starred,
            }
    data = { key: value for key, value in data.iteritems() if value is not None }
    response = client.authenticated_request(client.api.Endpoints.TASKS, 'POST', data=data)
    assert response.status_code == 201
    return response.json()

def update_task(client, task_id, revision, title=None, assignee_id=None, completed=None, recurrence_type=None, recurrence_count=None, due_date=None, starred=None, remove=None):
    '''
    Updates the task with the given ID

    See https://developer.wunderlist.com/documentation/endpoints/task for detailed parameter information
    '''
    if len(title) > client.api.MAX_TASK_TITLE_LENGTH:
        raise ValueError("Title cannot be longer than {} characters".format(client.api.MAX_TASK_TITLE_LENGTH))
    if (recurrence_type is None and recurrence_count is not None) or (recurrence_type is not None and recurrence_count is None):
        raise ValueError("recurrence_type and recurrence_count are required are required together")
    data = {
            wp_model.Task.title : title,
            wp_model.Task.assignee_id : int(assignee_id) if assignee_id else None,
            wp_model.Task.completed : completed,
            wp_model.Task.recurrence_type : recurrence_type,
            wp_model.Task.recurrence_count : int(recurrence_count) if recurrence_count else None,
            wp_model.Task.due_date : due_date,
            wp_model.Task.starred : starred,
            wp_model.Task.revision : int(revision),
            'remove' : remove,
            }
    data = { key: value for key, value in data.iteritems() if value is not None }
    endpoint = '/'.join([client.api.Endpoints.TASKS, str(task_id)])
    response = client.authenticated_request(endpoint, 'PATCH', data=data)
    return response.json()

def delete_task(client, task_id, revision):
    params = {
            wp_model.Task.revision : int(revision),
            }
    endpoint = '/'.join([client.api.Endpoints.TASKS, str(task_id)])
    client.authenticated_request(endpoint, 'DELETE', params=params)