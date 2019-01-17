from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import SignUpForm

User = get_user_model()


# Create your views here.
@method_decorator(login_required, name='dispatch')
class UserUpdataView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self, queryset=None):
        return self.request.user


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
