from Notification.models import PersonalNotification
from Video.models import Video, Comment, Like, Favorite
from django.views.generic import ListView, View
from django.shortcuts import redirect, render
from Account.mixins import RequiredLoginMixin
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import SubCategory
from django.db.models import Q


class VideoListView(ListView):
    template_name = "video/video_list.html"
    model = Video
    paginate_by = 6


class VideoDetailView(HitCountDetailView):
    model = Video
    template_name = "video/video-detail.html"
    count_hit = True

    def post(self, req, *args, **kwargs):
        text = self.request.POST.get("text")
        parent_id = self.request.POST.get("parent_id")

        if text:
            Comment.objects.create(video=self.get_object(), text=text, author=req.user,
                                   parent_id=parent_id)
        if parent_id:
            comment = Comment.objects.filter(id=parent_id).get()
            PersonalNotification.objects.create(message=F"{self.request.user} به نظر شما پاسخ داد ",
                                                user=comment.author,
                                                sender=req.user,
                                                link=comment.video.get_absolute_url())

        return redirect('video:video_detail', self.get_object().slug)

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        context.update({
            'popular_posts': Video.objects.order_by('-views')[:3],
        })
        # Pagination of Comments
        comments = Comment.objects.filter(video=self.get_object()).order_by('-created_at')
        paginator = Paginator(comments, 10)
        page = self.request.GET.get("page")
        context["comments"] = paginator.get_page(page)

        if Like.objects.filter(video__slug=self.object.slug, user_id=self.request.user.id).exists():
            context['is_like'] = True

        if Favorite.objects.filter(video__slug=self.object.slug, user_id=self.request.user.id).exists():
            context['is_fav'] = True
        else:
            context['is_fav'] = False
        return context


class SearchView(ListView):
    template_name = "video/search.html"
    model = Video
    paginate_by = 3

    def get_queryset(self):
        q = self.request.GET.get('q')
        return Video.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))


# CategoryDetail

class CatDetailView(View):
    template_name = "video/category_detail.html"

    def get(self, req, **kwargs):
        sub = SubCategory.objects.get(slug=self.kwargs.get('slug'))
        videos = sub.videos.all()

        # pagination of videos
        paginator = Paginator(videos, 4)
        page = self.request.GET.get("page")
        object_list = paginator.get_page(page)

        return render(req, self.template_name, {"videos": object_list})


class RemoveCommentView(View):
    def get(self, req, **kwargs):
        comment_obj = Comment.objects.get(id=self.kwargs.get('pk'))
        comment_obj.delete()
        return redirect('home:home')


class FavoriteView(RequiredLoginMixin, View):
    template_name = "video/favorite.html"

    def get(self, req, **kwargs):
        favorites = Video.objects.filter(favorites__user=req.user)
        return render(req, self.template_name, {"favorites": favorites})


def like(req, slug, pk):
    try:
        like = Like.objects.get(video__slug=slug, user_id=req.user.id)
        like.delete()
        return JsonResponse({"response": "unliked"})

    except:
        Like.objects.create(video_id=pk, user_id=req.user.id)
        return JsonResponse({"response": "liked"})


def favorite(req, slug, pk):
    try:
        fav = Favorite.objects.get(video__slug=slug, user_id=req.user.id)
        fav.delete()
        return JsonResponse({"response": "deleted"})

    except:
        Favorite.objects.create(video_id=pk, user_id=req.user.id)
        return JsonResponse({"response": "added"})
