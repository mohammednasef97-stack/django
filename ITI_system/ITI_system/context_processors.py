"""Expose role flags for templates (nav visibility, action buttons)."""


def role_capabilities(request):
    u = request.user
    caps = {
        "is_portal_admin": False,
        "is_portal_instructor": False,
        "is_portal_trainee": False,
        "can_manage_trainees": False,
        "can_manage_courses": False,
        "can_manage_instructors": False,
    }
    if u.is_authenticated:
        groups = set(u.groups.values_list("name", flat=True))
        caps["is_portal_admin"] = bool(u.is_staff or u.is_superuser)
        caps["is_portal_instructor"] = "Instructor" in groups
        caps["is_portal_trainee"] = "Trainee" in groups
        caps["can_manage_trainees"] = caps["is_portal_admin"] or caps["is_portal_instructor"]
        caps["can_manage_courses"] = caps["is_portal_admin"] or caps["is_portal_instructor"]
        caps["can_manage_instructors"] = caps["is_portal_admin"]
    return caps
