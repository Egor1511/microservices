import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tasks.models import Task
from tasks.serializers import TaskSerializer
from tasks.tests.factories import TaskFactory

@pytest.mark.django_db
class TestTaskAPI:

    def setup_method(self):
        self.client = APIClient()
        self.task1 = TaskFactory.create(completed=False)
        self.task2 = TaskFactory.create(completed=True)
        self.list_url = '/api/tasks/'
        self.detail_url = '/api/tasks/{}/'

    def test_list_tasks(self):
        response = self.client.get(self.list_url)
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    def test_retrieve_task(self):
        url = self.detail_url.format(self.task1.pk)
        response = self.client.get(url)
        serializer = TaskSerializer(self.task1)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    def test_create_task(self):
        data = {
            'title': 'Новая задача',
            'description': 'Описание новой задачи',
            'completed': False
        }
        response = self.client.post(self.list_url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.count() == 3
        assert Task.objects.get(pk=response.data['id']).title == data['title']

    def test_update_task(self):
        data = {
            'title': 'Обновленная задача',
            'description': 'Обновленное описание',
            'completed': True
        }
        url = self.detail_url.format(self.task1.pk)
        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.task1.refresh_from_db()
        assert self.task1.title == data['title']
        assert self.task1.completed == data['completed']

    def test_partial_update_task(self):
        data = {'completed': True}
        url = self.detail_url.format(self.task1.pk)
        response = self.client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.task1.refresh_from_db()
        assert self.task1.completed is True

    def test_delete_task(self):
        url = self.detail_url.format(self.task1.pk)
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Task.objects.count() == 1

    def test_retrieve_nonexistent_task(self):
        url = self.detail_url.format(999)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_invalid_create_task(self):
        data = {'description': 'Без заголовка'}
        response = self.client.post(self.list_url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Task.objects.count() == 2
