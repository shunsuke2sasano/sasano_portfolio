from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from accounts.models import Like, CustomUser
from accounts.views import monthly_like_ranking, yearly_like_ranking
from django.http import JsonResponse
from accounts.models import CustomUser, GeneralUserProfile, Like, UserProfile

@login_required
def admin_dashboard(request):
    """管理者用ダッシュボード（一般ユーザーのみ表示）"""
    current_year = now().year
    current_month = now().month

    # 月間ランキング（一般ユーザープロフィールの user に紐づくいいねを集計）
    monthly_profiles = GeneralUserProfile.objects.filter(
        user__is_active=True,
        user__is_deleted=False,
        user__is_staff=False,       # 管理者でない
        user__is_superuser=False    # スーパーユーザーでない
    ).annotate(
        total_likes=Count(
            "user__likes_received_records",
            filter=Q(
                user__likes_received_records__created_at__year=current_year,
                user__likes_received_records__created_at__month=current_month
            )
        )
    ).order_by("-total_likes")[:10]

    # 年間ランキング
    yearly_profiles = GeneralUserProfile.objects.filter(
        user__is_active=True,
        user__is_deleted=False,
        user__is_staff=False,
        user__is_superuser=False
    ).annotate(
        total_likes=Count(
            "user__likes_received_records",
            filter=Q(
                user__likes_received_records__created_at__year=current_year
            )
        )
    ).order_by("-total_likes")[:10]

    return render(request, "dashboard/admin_dashboard.html", {
        "monthly_profiles": monthly_profiles,
        "yearly_profiles": yearly_profiles,
    })

@login_required
def user_dashboard(request):
    """ユーザー用ダッシュボード"""
    if request.user.is_superuser or request.user.is_staff:
        return redirect('dashboard:admin_dashboard')  # 管理者は管理者ダッシュボードへ

    current_year = now().year
    current_month = now().month

    # **年間・月間のいいね数取得**
    yearly_likes = Like.objects.filter(liked_user=request.user, created_at__year=current_year).count()
    monthly_likes = Like.objects.filter(liked_user=request.user, created_at__year=current_year, created_at__month=current_month).count()

    return render(request, 'dashboard/user_dashboard.html', {
        'yearly_likes': yearly_likes,
        'monthly_likes': monthly_likes,
    })
