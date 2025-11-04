from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from apps.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    """Detail view for User model."""

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update view for User model."""

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        """Get URL to redirect to after successful update."""
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self, _queryset: QuerySet | None = None) -> User:
        """Get the user object to update (always the current user)."""
        assert self.request.user.is_authenticated
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """Redirect view to user's detail page."""

    permanent = False

    def get_redirect_url(self) -> str:
        """Get URL to redirect to (user's detail page)."""
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
