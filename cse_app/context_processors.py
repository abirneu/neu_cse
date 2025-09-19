from .models import ScrollingNotice

def scrolling_notice(request):
    notice = ScrollingNotice.objects.filter(is_active=True).first()
    return {'scrolling_notice': notice.text if notice else ''}