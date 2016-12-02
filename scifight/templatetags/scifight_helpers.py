from django import template
from django.utils.safestring import mark_safe
from django.utils.translation  import ugettext as _tr

register = template.Library()

_captain_html = (
    '<span style="padding-left: 0.25em;" title="{}">'
    '<i class="fa fa-flag"></i></span>').format(_tr("Team captain"))


@register.filter(is_safe=True)
def captain_flag(player):
    """ Custom template filter for putting nice-looking flag icons after team
        captain names. It lets us to write templates like:

        .. code-block:: none

           {{ player.full_name }}{{ player | captain_flag }}

        where `player` is an object of type :type:`scifight.models.Participant`.
        If `player.is_captain` is true, than the filter emits the HTML code to
        output the flag icon, or empty string otherwise. Note that you shouldn't
        put any spaces between the name and the flag as it would lead to odd
        hyperlink underlining.
    """
    return mark_safe(_captain_html if player and player.is_captain else '')
