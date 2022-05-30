from django import forms

from main.models import *


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class ActionFileForm(forms.ModelForm):
    class Meta:
        model = ActionFile
        fields = [
            "*"
        ]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "*"
        ]
        widgets = {
            "description": forms.Textarea,
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["subject"].widget = forms.RadioSelect()
        self.fields["subject"].queryset = Task.objects.all()


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "*"
        ]


class GroupForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "*"
        ]
