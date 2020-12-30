import asyncio

stream_delay = 5 #sec
stream_retry_timeout = 30000 #milisec

async def project_tasks_generator(request, project_id, tasks_repo):
    latest_update = None
    while True:
        latest_change = tasks_repo.get_latest_project_tasks_change(project_id=project_id)
        if await request.is_disconnected():
            yield {
                'event': 'end',
                'data': ''
            }
            print('request disconnected')
            break
        if latest_change != latest_update:
            print('waiting')
        if latest_change != latest_update:
            yield {
                'event': 'update',
                'data': await tasks_repo.get_all_project_tasks(project_id=project_id),
                'retry': stream_retry_timeout
            }
            latest_update = latest_change
        await asyncio.sleep(stream_delay)