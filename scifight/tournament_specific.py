from django.core    import exceptions
from django.contrib import admin
from django.forms   import models


class InlineFormSet(models.BaseInlineFormSet):

    def save_new(self, form, commit=True):
        obj = super().save_new(form, commit=False)
        obj.fill_tournament()
        if commit:
            obj.save()
        return obj

    def save_existing(self, form, instance, commit=True):
        obj = super().save_existing(form, instance, commit=False)
        obj.fill_tournament()
        if commit:
            obj.save()
        return obj


class InlineMixin(object):

    formset = InlineFormSet

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(InlineMixin, self).get_formset(request, obj, **kwargs)
        formset.request = request
        return formset


class ModelAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        self.scifight_user = request.user
        self._exclude_tournament_field()
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            tournament_of_user = None
            # To check if the (OneToOne) relation exists or not,
            # you can use the hasattr function.
            # http://stackoverflow.com/questions/3463240/check-if-onetoonefield-is-none-in-django
            if hasattr(request.user, 'scifight_user_profile'):
                scifight_user_profile = request.user.scifight_user_profile
                if scifight_user_profile.tournament:
                    tournament_of_user = scifight_user_profile.tournament
            qs = qs.filter(tournament=tournament_of_user)
        return qs

    def _process_tournament_field(self, obj, request):
        if request.user.is_superuser:
            if hasattr(obj, "fill_tournament"):
                obj.fill_tournament()
        else:
            if hasattr(request.user, 'scifight_user_profile'):
                scifight_user_profile = request.user.scifight_user_profile
                if scifight_user_profile.tournament:
                    obj.tournament = scifight_user_profile.tournament
                else:
                    raise exceptions.PermissionDenied()

    def _exclude_tournament_field(self):
        self.exclude = ()
        if not self.scifight_user.is_superuser:
            self.exclude = ('tournament',)

    def save_model(self, request, obj, form, change):
        self._process_tournament_field(obj, request)
        obj.save()
