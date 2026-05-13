from django.contrib.auth.models import Group


def is_portal_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def is_instructor(user):
    return user.is_authenticated and user.groups.filter(name="Instructor").exists()


def is_trainee_group(user):
    return user.is_authenticated and user.groups.filter(name="Trainee").exists()


def can_manage_trainees(user):
    return is_portal_admin(user) or is_instructor(user)


def can_manage_courses(user):
    return is_portal_admin(user) or is_instructor(user)


def can_manage_instructors(user):
    # Keep hierarchy explicit: only admins can manage instructor accounts.
    return is_portal_admin(user)


def ensure_default_groups():
    """Idempotent: used from AppConfig.ready for local/dev setups."""
    for name in ("Instructor", "Trainee"):
        Group.objects.get_or_create(name=name)
