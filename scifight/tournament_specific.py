from django.core    import exceptions
from django.contrib import admin
from django.forms   import models

from scifight import models as sci_model


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
    def save_model(self, request, obj, form, change):
        self._process_tournament_field(obj, request)
        obj.save()

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not request.user.is_superuser:
            if hasattr(type(self), "foreignkey_filtered_fields"):
                if db_field.name in type(self).foreignkey_filtered_fields:
                    user_tournament = self._get_user_owned_tournament(request)
                    model_field = getattr(self.model, db_field.name)
                    if model_field:
                        kwargs["queryset"] = model_field.get_queryset().filter(
                            tournament=user_tournament)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        self.scifight_user = request.user
        self._exclude_tournament_field()
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            user_tournament = self._get_user_owned_tournament(request)
            if hasattr(self.model, 'tournament'):
                qs = qs.filter(tournament=user_tournament)
            elif hasattr(type(self), 'tournament_alias_field'):
                alias_field = type(self).tournament_alias_field
                qs = qs.filter(**{alias_field: user_tournament})

        return qs

    @staticmethod
    def _get_user_owned_tournament(request):

        if not request:
            return

        tournament_of_user = None

        # To check if the (OneToOne) relation exists or not,
        # you can use the hasattr function.
        # http://stackoverflow.com/questions/3463240
        if hasattr(request.user, 'scifight_user_profile'):
            scifight_user_profile = request.user.scifight_user_profile
            if scifight_user_profile.tournament:
                tournament_of_user = scifight_user_profile.tournament

        return tournament_of_user

    @staticmethod
    def _process_tournament_field(obj, request):
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
        if hasattr(self.model, 'tournament'):
            if not self.exclude:
                self.exclude = []
            if 'tournament' in self.exclude:
                self.exclude.remove('tournament')
            if not self.scifight_user.is_superuser:
                self.exclude.append('tournament')
