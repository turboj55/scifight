from django.core.management.commands import makemessages as _dj_makemessages


# Overrides Django's default 'makemessages' command to let 'xgettext' recognize
# additional keywords like '_tr' and '_trl'. These names are much shorter to
# type than 'ugettext' and 'ugettext_lazy' and aren't so dangerous as '_' is
# (which is also used for throwing values away).
# noinspection PyClassHasNoInit
class Command(_dj_makemessages.Command):
    xgettext_options = _dj_makemessages.Command.xgettext_options + [
        '--keyword=_tr',
        '--keyword=_trl']
