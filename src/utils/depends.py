from src.repository.tasks import TaskRepository
from src.repository.users import UserRepository
from src.services.tasks import TaskService
from src.services.users import UserService

task_repo = TaskRepository()
task_service = TaskService(task_repo)

user_repo = UserRepository()
user_service = UserService(user_repo)


def get_task_service() -> TaskService:
    return task_service

def get_user_service() -> UserService:
    return user_service
