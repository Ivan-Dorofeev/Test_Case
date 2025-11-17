from enum import Enum


class AnnouncementStatus(str, Enum):
    """Статусы объявления (аукциона, тендера и т.п.)."""

    DRAFT = "draft"  # Черновик — объявление создано, но ещё не опубликовано
    ACTIVE = "active"  # Активное — доступно для пользователей
    CLOSED = "closed"  # Закрыто — завершено, больше не доступно
    MODERATION = "moderation"  # На модерации — ожидает проверки администратором


class CompanyUserRole(str, Enum):
    """Роль пользователя в компании."""

    OWNER = "owner"  # Владелец компании (полные права)
    ADMIN = "admin"  # Администратор (почти полные права, кроме удаления владельца)
    EMPLOYEE = "employee"  # Сотрудник (ограниченные права, может работать с данными)
    VIEWER = "viewer"  # Наблюдатель (доступ только для просмотра)


class TransactionStatus(str, Enum):
    """Статусы финансовой транзакции."""

    PENDING = "pending"  # Ожидает подтверждения (обработка в процессе)
    SUCCESS = "success"  # Успешно завершена
    FAILED = "failed"  # Ошибка при выполнении
    CANCELLED = "cancelled"  # Отменена пользователем или системой


class ActionType(str, Enum):
    """Типы действий пользователя (для логирования)."""

    CREATE = "create"  # Создание объекта
    UPDATE = "update"  # Обновление существующего объекта
    DELETE = "delete"  # Удаление объекта
    LOGIN = "login"  # Вход в систему
    LOGOUT = "logout"  # Выход из системы
