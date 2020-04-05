from django.forms import ModelForm
from blog.posts.models import Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.urls import reverse


# Create the form class.
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'author']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-new-post'
        self.helper.form_class = 'NewPost'
        self.helper.form_method = 'post'
        self.helper.form_action = '/posts/new'
        self.helper.add_input(Submit('submit', 'Publicate'))


class EditPostForm(PostForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse('post-edit', args=[self.instance.id])
        self.helper.inputs[0].value = 'Save'
