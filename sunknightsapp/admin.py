from django.contrib import admin
from django import forms

from .models.discord_roles import DiscordRole
from .models.fight import Fight
from .models.fight_participation import FightParticipation
from .models.points_info import PointsInfo
from .models.point_submission import PointSubmission
from .models.clan_user import ClanUser
from .models.discord_server import DiscordServer
from .models.clan_user_roles import ClanUserRoles
from .models.points_proof import PointsProof
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group



# Register your models here.



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = ClanUser
        fields = ('discord_id', 'discord_nickname')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = ClanUser
        fields = ('discord_id', 'password', 'discord_nickname', 'is_active', 'is_manager','is_manager', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('discord_id', 'discord_nickname', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('discord_id', 'password')}),
        ('Personal info', {'fields': ('discord_nickname',)}),
        ('Permissions', {'fields': ('is_manager','is_superuser',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('discord_id', 'discord_nickname', 'password1', 'password2')}
        ),
    )
    search_fields = ('discord_id',)
    ordering = ('discord_id',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(ClanUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)






admin.site.register(DiscordServer)
admin.site.register(DiscordRole)
admin.site.register(Fight)
admin.site.register(FightParticipation)
admin.site.register(PointsInfo)
admin.site.register(PointSubmission)
admin.site.register(ClanUserRoles)
admin.site.register(PointsProof)