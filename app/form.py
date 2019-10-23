from django import forms


class Form_register(forms.Form):
    user_name = forms.CharField(max_length=20, label='用户名')
    pass_word1 = forms.CharField(max_length=20, label='密码',widget=forms.PasswordInput)
    pass_word2 = forms.CharField(max_length=20, label='重复密码',widget=forms.PasswordInput)

class Form_login(forms.Form):
    user_name=forms.CharField(max_length=20,label='用户名')
    pass_word=forms.CharField(max_length=20,label='密码',widget=forms.PasswordInput)

class Add_good(forms.Form):
    good_name=forms.CharField(max_length=100,label='商品名')
    good_price=forms.FloatField(max_value=9999999999,label='商品价格',min_value=0)
    good_info=forms.CharField(max_length=1500,label='商品详情',widget=forms.Textarea)
    good_img=forms.CharField(max_length=400,label='图片地址')