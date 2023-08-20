import datetime

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from users.models import Action


def create_action(user, verb: str, target=None) -> None:
    """
    Creates an action if no similar actions were made during last ten minutes.
    Use constants from Action model as 'verb' for convenience, e.g. `Action.VIEW_PRODUCT`.
    """
    # Check for any similar action during last ten minutes
    now = timezone.now()
    last_ten_minutes = now - datetime.timedelta(seconds=600)
    similar_actions = Action.objects.filter(
        user_id=user.id, verb=verb, created__gte=last_ten_minutes
    )

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct, target_id=target.id
        )

    if not similar_actions:
        Action.objects.create(user=user, verb=verb, target=target)
