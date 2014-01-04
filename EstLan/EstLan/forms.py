from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _, ugettext

from EstLan.models import ObjectComment, CustomPage

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Layout, Field
from EstLan.utils import sanitize_html


class ArticleCommentForm(ModelForm):
    class Meta:
        model = ObjectComment
        fields = ('comment', )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.article = kwargs.pop('article')

        super(ArticleCommentForm, self).__init__(*args, **kwargs)

        self.fields['comment'].label = ''
        self.fields['comment'].widget = Textarea()

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Div(
                HTML(_('Commenting as: ')),
                HTML('<span>%s</span>' % self.user.get_name() if self.user.is_authenticated() else ''),
                css_class='align-right commenting-as'
            ),

            Field('comment', css_class='comments-textarea'),

            Div(
                HTML('<button type="submit" class="btn btn-green">%s</button>' % ugettext('Comment')),
                css_class='align-right',
            )
        )

    def clean_comment(self):
        data = self.cleaned_data['comment']
        return sanitize_html(data, tags='p i strong b u a pre br', attrs='href')

    def save(self, commit=True):
        instance = super(ArticleCommentForm, self).save(commit=False)

        if commit:
            instance.for_object = self.article
            instance.user = self.user
            instance.save()
        return instance
