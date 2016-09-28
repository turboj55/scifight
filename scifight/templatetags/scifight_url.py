from django import template
from scifight import models
from django.core.urlresolvers import reverse, NoReverseMatch
import logging


logger = logging.getLogger(__name__)
register = template.Library()

_single_arg_views = {
#   Model type           View name                 Field to pass as arg
    models.Participant: ("scifight:participant",   'id'),
    models.Leader:      ("scifight:leader",        'id'),
    models.Juror:       ("scifight:juror",         'id'),
    models.Room:        ("scifight:room",          'id'),
    models.Fight:       ("scifight:fight",         'id'),
    models.Problem:     ("scifight:problem",       'problem_num')
}


@register.filter(is_safe=True)
def scifight_url(model):
    """ Custom filter for reverse-getting URLs for models
        in :mod:`scifight.models`. Traditional Django way for generating links
        implies using `{% url ... %}` template construct, which leads to overly
        long and error-prone code due to having to explicitly pass all URL
        pattern parameters. Fortunately, our model objects already contain all
        information needed for reverse-lookup, in their direct fields or through
        foreign key references.

        Consider, for example, the following template code:

        .. code-block:: none

           {% url "scifight:problem" tournament_slug problem.problem_num %}

        It's obvious that the `problem` object already know which tournament it
        belongs to, and also holds it's number. This is exactly what this filter
        was written for: it lets you write the above line in a greatly
        simplified way:

        .. code-block:: none

           {{ problem | scifight_url }}

        This filter works only for models specific to the SciFight project,
        like :class:`scifight.models.Problem` or :class:`scifight.models.Fight`,
        and is highly project-specific aid for template shortening.
    """
    def wrapped_reverse(view_name, *args, **kwargs):
        try:
            return reverse(view_name, args=args, kwargs=kwargs)
        except NoReverseMatch:
            logger.error(
                'NoReverseMatch: model = %s '
                'model_type = %s '
                'args = %s '
                'kwargs = %s ' % (model, type(model), args, kwargs)
            )
            return ''

    model_type = type(model)

    if model_type == models.Team:
        if model.slug:
            return wrapped_reverse('scifight:team_slug',
                                   tournament_slug=model.tournament.slug,
                                   team_slug=model.slug)
        else:
            return wrapped_reverse('scifight:team_id',
                                   tournament_slug=model.tournament.slug,
                                   team_id=model.id)

    if model_type == models.Tournament:
        return wrapped_reverse('scifight:tournament', model.slug)

    if model_type in _single_arg_views:
        (view_name, field_name) = _single_arg_views[model_type]
        return wrapped_reverse(view_name,
                               model.tournament.slug,
                               getattr(model, field_name))

    logger.error("unsupported model passed: %s" % model_type)
    return ''
