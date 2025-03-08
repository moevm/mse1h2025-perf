from abc import ABC, abstractmethod

class BaseTaskManager(ABC):
    @abstractmethod
    def set_settings(self, settings):
        """Задать настройки для задач."""
        pass

    @abstractmethod
    def create_task(self, task_details):
        """Создать задачу с определенными деталями."""
        pass

    @abstractmethod
    def set_verification_settings(self, verification_settings):
        """Задать настройки проверки задачи (под вопросом)."""
        pass

    @abstractmethod
    def verify_task(self, task, answer):
        """Проверить задачу на основе заданных настроек проверки."""
        pass