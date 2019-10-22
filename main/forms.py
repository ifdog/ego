from django import forms


class NoteEditForm(forms.Form):
    key = forms.CharField(label="key", widget=forms.HiddenInput(attrs={'id': 'edit_key_input'}))
    content = forms.CharField(label="Content",
                              widget=forms.Textarea(attrs={'id': 'edit_md_area', 'class': 'textarea is-warning full_width grow'}))
    tags = forms.CharField(label="Tags", widget=forms.HiddenInput(attrs={'id': 'edit_tags_input'}))