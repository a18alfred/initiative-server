from rest_framework.permissions import BasePermission


class IsSuperUserOrModeratorUser(BasePermission):
    """
    Является ли пользователь модератором или суперюзером
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous or not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.is_moderator


class IsSuperUser(BasePermission):
    """
    Является ли пользователь суперюзером
    """

    def has_permission(self, request, view):
        return (not request.user.is_anonymous) and request.user.is_authenticated and request.user.is_superuser


class IsActive(BasePermission):
    """
    Активный ли пользователь
    """

    def has_permission(self, request, view):
        return (not request.user.is_anonymous) and request.user.is_authenticated and request.user.is_active


class IsPhoneConfirmed(BasePermission):
    """
    Телефонный номер подтвержден
    """

    def has_permission(self, request, view):
        return (not request.user.is_anonymous) and request.user.is_authenticated and request.user.is_phone_confirmed


class IsOwner(BasePermission):
    """
    Редактировать/читать объект может только владелец (профайла) или создатель проекта.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous or not request.user.is_authenticated:
            return False
        return obj.account == request.user


class IsOwnerOrSuperUser(BasePermission):
    """
    Редактировать/читать объект может только владелец (профайла) или создатель проекта или суперюзер
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous or not request.user.is_authenticated:
            return False
        return obj.account == request.user or request.user.is_superuser


class IsAccountOwnerOrSuperUser(BasePermission):
    """
    Удалить объект может только владелец аккаунта или суперюзер
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous or not request.user.is_authenticated:
            return False
        return obj == request.user or request.user.is_superuser


class IsOwnerOrSuperUserOrModerator(BasePermission):
    """
    Редактировать/читать объект может только владелец (профайла) или создатель проета или суперюзер
    или модератор
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous or not request.user.is_authenticated:
            return False
        return obj.account == request.user or request.user.is_superuser or request.user.is_moderator


class IsAccountOwnerOrSuperUserOrModerator(BasePermission):
    """
    Редактировать/читать аккаунт может только владелец или суперюзер или модератор
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous or not request.user.is_authenticated:
            return False
        return obj == request.user or request.user.is_superuser or request.user.is_moderator


class IsUploadsOwnerOrSuperUserOrModerator(BasePermission):
    """
    Редактировать загруженные файлы и ссылки может только владелец, суперюзер или модератор
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous or not request.user.is_authenticated:
            return False
        return obj.project.account == request.user or request.user.is_superuser or request.user.is_moderator
