from django_cradmin.viewhelpers import listbuilder
from django_cradmin import crapp
from django_cradmin.viewhelpers import create
from lolchan.lolchan_core.models import Post, Comment
from django import forms
from crispy_forms import layout
from django_cradmin.acemarkdown.widgets import AceMarkdownWidget
from django_cradmin.crispylayouts import DefaultSubmit
from django.utils.translation import ugettext_lazy as _


class CommentItemValue(listbuilder.itemvalue.base.ItemValueRenderer):
    valuealias = 'comment'
    template_name = 'lolchan_channel/listbuilder/commentitemvalue.django.html'

    def __init__(self, value):
        super(CommentItemValue, self).__init__(value)

    def get_extra_css_classes_list(self):
        css_classes_list = super(CommentItemValue, self).get_extra_css_classes_list()
        css_classes_list.append('panel')
        css_classes_list.append('panel-default')
        return css_classes_list


class PostItemFrame(listbuilder.itemframe.DefaultSpacingItemFrame):
    pass


class PostItemValue(listbuilder.itemvalue.FocusBox):
    valuealias = 'post'
    template_name = 'lolchan_channel/listbuilder/postitemvalue.django.html'

    def __init__(self, value):
        super(PostItemValue, self).__init__(value)

    def get_extra_css_classes_list(self):
        css_classes_list = super(PostItemValue, self).get_extra_css_classes_list()
        return css_classes_list

    def __get_comment_queryset(self):
        return Comment.objects.filter(post=self.post).order_by('-publish_date', )[:3]

    def get_context_data(self, request=None):
        context = super(PostItemValue, self).get_context_data(request)
        context['comment_list'] = listbuilder.base.List.from_value_iterable(
            value_iterable=self.__get_comment_queryset(),
            value_renderer_class=CommentItemValue)
        return context


class PostListBuilder(listbuilder.base.List):

    def __init__(self, channel):
        super(PostListBuilder, self).__init__()
        self.channel = channel

    def __get_post_queryset(self):
        return Post.objects.filter(channel=self.channel)

    def build(self):
        self.extend_with_values(value_iterable=self.__get_post_queryset(),
                                frame_renderer_class=PostItemFrame,
                                value_renderer_class=PostItemValue)


class PostForm(forms.ModelForm):

    class Meta:
        fields = ['title', 'text']
        model = Post

    def __init__(self, *args, **kwargs):
        self.channel = kwargs.pop('channel')
        super(PostForm, self).__init__(*args, **kwargs)

    @classmethod
    def get_field_layout(cls):
        return []


class ChannelView(create.CreateView):
    model = Post
    template_name = 'lolchan_channel/channel.django.html'

    def get_pagetitle(self):
        return self.request.cradmin_role.name

    def get_form_class(self):
        return PostForm

    def get_form_kwargs(self):
        kwargs = super(ChannelView, self).get_form_kwargs()
        channel = self.request.cradmin_role
        kwargs['channel'] = channel
        return kwargs

    def get_form(self, form_class=None):
        form = super(ChannelView, self).get_form(form_class=form_class)
        form.fields['text'].widget = AceMarkdownWidget()
        form.fields['text'].label = False
        form.fields['title'].widget = forms.TextInput(attrs={'placeholder': _('Title')})
        form.fields['title'].label = False
        return form

    def save_object(self, form, commit=True):
        obj = super(ChannelView, self).save_object(form)
        return obj

    def get_buttons(self):
        return [
            DefaultSubmit(
                'send_post',
                _('Post'),
                css_class='btn btn-success'
            )
        ]

    def get_field_layout(self):
        field_layout = []
        field_layout.extend(self.get_form_class().get_field_layout())
        field_layout.append('title')
        field_layout.append('text')
        return layout.Fieldset(
            '',
            layout.Div(
                *field_layout
            ),
            layout.Div(
                layout.Div(*self.get_buttons()),
                css_class='text-right'
            ),
            css_class='post-form-container'
        )

    def set_automatic_attributes(self, obj):
        obj.channel = self.request.cradmin_role

    def __get_post_queryset(self):
        return Post.objects.all().filter(channel=self.request.cradmin_role)

    def get_context_data(self, **kwargs):
        context = super(ChannelView, self).get_context_data(**kwargs)
        context['post_list'] = listbuilder.base.List.from_value_iterable(
            value_iterable=self.__get_post_queryset(),
            frame_renderer_class=PostItemFrame,
            value_renderer_class=PostItemValue)
        return context


class App(crapp.App):
    appurls = [
        crapp.Url(r'^$', ChannelView.as_view(), name=crapp.INDEXVIEW_NAME)
    ]
