import time

import pytest
from fastapi.testclient import TestClient


from .main import app


import pandas as pd
import dataframe_image
import psutil

tests_time = []
cpu_time = []
mem_time = []

process = psutil.Process()
cpu_usage = process.cpu_percent(interval=0.1)

def metric_score(start_cpu,start_mem, start_time, process):
    now = time.time()
    mem_end = process.memory_info().rss / 1024 / 1024
    cpu_end = psutil.cpu_percent(interval=None)
    times = now - start_time
    cpu = cpu_end - start_cpu
    mem = mem_end - start_mem
    tests_time.append(times)
    cpu_time.append(cpu)
    mem_time.append(mem)


def test_create_post():
        client = TestClient(app)
        mem_usage = process.memory_info().rss / 1024 / 1024
        start = now = time.time()
        response = client.post(
            "/post/create_post",
            json={
                "title":"Test",
                "content":"Test"
            }
        )
        metric_score(cpu_usage, mem_usage, start, process)
        assert response.status_code == 200



def test_all_posts():
        client = TestClient(app)

        mem_usage = process.memory_info().rss / 1024 / 1024
        start = now = time.time()

        response = client.get("post/posts",)

        metric_score(cpu_usage, mem_usage, start, process)

        assert response.status_code == 200


def test_get_post():
        client = TestClient(app)

        response = client.post(
            "/post/create_post",
            json={
                "title": "Test",
                "content": "Test"
            }

        )
        assert response.status_code == 200
        created_response = response.json().get('id')
        print(created_response)
        mem_usage = process.memory_info().rss / 1024 / 1024
        start = now = time.time()
        get_response = client.get(
            f"/post/post_id/{created_response}",
        )
        metric_score(cpu_usage, mem_usage, start, process)
        print(get_response.text)
        assert get_response.status_code == 200


def test_update_post():
        client = TestClient(app)
        response = client.post(
            "/post/create_post",
            json={
                "title": "Test",
                "content": "Test"
            }
        )
        assert response.status_code == 200
        created_response = response.json().get('id')

        mem_usage = process.memory_info().rss / 1024 / 1024
        start = now = time.time()

        update_response = client.put(f"/post/update_post/{created_response}",
                                           json={
                                               "title": "Updated",
                                               "content": "Updated"
                                           }
                                           )

        metric_score(cpu_usage, mem_usage, start, process)

        assert update_response.status_code == 200


def test_delete_post():
        client = TestClient(app)
        response = client.post(
            "/post/create_post",
            json={
                "title": "Test",
                "content": "Test"
            }
        )
        assert response.status_code == 200
        created_response = response.json().get('id')


        mem_usage = process.memory_info().rss / 1024 / 1024
        start = now = time.time()

        get_response = client.delete(
            f"/post/delete_post/{created_response}",

        )

        metric_score(cpu_usage, mem_usage, start, process)

        df = pd.DataFrame({
            "Операция": ["Чтение (1)", "Чтение(все)", "Создание", "Изменение", "Удаление"],
            "Время": [tests_time[2], tests_time[1], tests_time[0], tests_time[3], tests_time[4]],
            "Память": [mem_time[2], mem_time[1], mem_time[0], mem_time[3], mem_time[4]],

        })

        dataframe_image.export(df, "table.png", table_conversion="matplotlib", dpi=300)
        assert get_response.status_code == 200

