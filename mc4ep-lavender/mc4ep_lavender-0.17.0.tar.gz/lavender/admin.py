from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django_json_widget.widgets import JSONEditorWidget
from django_jsonfield_backport.models import JSONField

from lavender.models import Package, Player, LogHistory, GameLog, Quenta, Texture


class PlayerAdmin(UserAdmin):
    def token_uuid(self, obj):
        return obj.token.uuid

    filter_horizontal = ('packages',)

    list_display = ('username', 'email', 'is_active', 'date_joined', 'token_uuid')
    list_select_related = ['token']
    ordering = ('date_joined',)
    search_fields = ['username', 'email', 'token__uuid']
    readonly_fields = ['token_uuid']

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            perm_fields = ('is_active', 'is_staff')

        return [
            (None, {'fields': ('username', 'password')}),
            (_('Personal info'), {'fields': ('email',)}),
            (_('Permissions'), {'fields': perm_fields}),
            ('Minecraft', {'fields': ('packages', 'token_uuid')})
        ]


class LogHistoryAdmin(ModelAdmin):
    list_filter = ('date', 'source')
    list_display = ('player', 'date', 'source')
    search_fields = (
        'player__username',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('player')


class GameLogAdmin(ModelAdmin):
    list_display = ('player', 'date', 'kind',)
    list_filter = ('date', 'kind')
    search_fields = (
        'player__username',
        'kind'
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('player')


class QuentaAdmin(ModelAdmin):
    list_display = ('player', 'approved',)
    list_filter = ('approved',)
    search_fields = (
        'player__username',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('player')


class PackageAdmin(ModelAdmin):
    list_display = ('name', 'title', 'location', 'is_default')
    list_filter = ('is_default',)


class JSONViewerWidget(JSONEditorWidget):
    def __init__(self, *args, **kwargs):
        kwargs['mode'] = 'view'
        kwargs['width'] = '20rem'
        kwargs['height'] = 'auto'
        super(JSONViewerWidget, self).__init__(*args, **kwargs)


class TextureAdmin(ModelAdmin):
    list_display = ('username', 'race', 'size', 'gender', 'kind', 'created', 'active',)
    list_filter = ('deleted',)
    search_fields = (
        'token__player__username',
    )

    list_select_related = ['token', 'token__player']
    readonly_fields = ['username', 'preview', 'image', 'height', 'width', 'kind', 'created', ]
    exclude = ['token']

    def username(self, obj):
        return obj.token.player.username

    def active(self, obj):
        return not obj.deleted
    active.boolean = True

    def race(self, obj):
        return obj.metadata.get("race")

    def race(self, obj):
        return obj.metadata.get("race")

    def size(self, obj):
        return obj.metadata.get("size")

    def gender(self, obj):
        return obj.metadata.get("gender")

    def preview(self, obj):
        return mark_safe('<image src="%s" />' % obj.image.url)

    formfield_overrides = {
        JSONField: {'widget': JSONViewerWidget},
    }


admin.site.register(Player, PlayerAdmin)
admin.site.register(Texture, TextureAdmin)
admin.site.register(LogHistory, LogHistoryAdmin)
admin.site.register(GameLog, GameLogAdmin)
admin.site.register(Quenta, QuentaAdmin)
admin.site.register(Package, PackageAdmin)
