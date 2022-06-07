from django import forms

from main.models import *


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class ActionFileForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = "__all__"


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "description": forms.Textarea,
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
