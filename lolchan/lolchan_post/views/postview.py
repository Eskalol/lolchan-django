from django_cradmin.viewhelpers import create
from django_cradmin import crapp
from django_cradmin.viewhelpers import listbuilder


from lolchan.lolchan_core.models import Post, Comment


class CommentItemValue(listbuilder.itemvalue.FocusBox):
    valuealias = 'comment'
    template_name = 'lolchan_post/listbuilder/comment.django.html'

    def __init__(self, value):
        super(CommentItemValue, self).__init__(value)

    def get_extra_css_classes_list(self):
        css_classes_list = super(CommentItemValue, self).get_extra_css_classes_list()
        return css_classes_list


class PostView(create.CreateView):
    model = Post
    template_name = 'lolchan_post/postbase.django.html'

    def get_pagetitle(self):
        return self.request.cradmin_role.title

    def get_queryset(self):
        return Post.objects.get(id=self.request.cradmin_role.id)

    def __get_comment_queryset(self, **kwargs):
        return Comment.objects.all().filter(post=self.request.cradmin_role)

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['comments'] = listbuilder.base.List.from_value_iterable(
            value_iterable=self.__get_comment_queryset(),
            value_renderer_class=CommentItemValue
        )
        context['post'] = self.get_queryset()
        return context


class App(crapp.App):
    appurls = [
        crapp.Url(r'^$', PostView.as_view(), name=crapp.INDEXVIEW_NAME),
    ]