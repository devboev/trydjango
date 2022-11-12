from django import forms

from articles.models import Article

# class ArticleOldForm(forms.Form):
    # title = forms.CharField()
    # content = forms.CharField()
    
    # def clean_title(self):
    #     cleaned_data = self.cleaned_data
    #     title = cleaned_data.get('title')
    #     qs =Article.objects.filter(title__icontains=title)
    #     if qs.exists():
    #         raise forms.ValidationError('this tile is alrready taken.')
    #     return title
    
    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     title = cleaned_data.get('title')
    #     qs =Article.objects.filter(title__icontains=title)
    #     if qs.exists():
    #         #self.add_error('title','this tile is alrready taken.') #field_error same as clean_title
    #         raise forms.ValidationError('this tile is alrready taken.') # non field_error
    #     return title
    
class ArticleForm(forms.ModelForm):
    class Meta:
        model=Article
        fields=['title','content']   
    
    def clean(self):
        data = self.cleaned_data
        title_str = data.get('title')
        qs =Article.objects.filter(title__icontains=title_str)
        if qs.exists():
            self.add_error('title',f"\"{title_str}\" as title is already taken.") #field_error same as clean_title
            #raise forms.ValidationError('this tile is alrready taken.') # non field_error
        return data    