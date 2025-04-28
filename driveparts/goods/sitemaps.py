from django.contrib.sitemaps import Sitemap
from .models import Goods


class PostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Goods.manager.all()
    
    def lastmode(self, obj):
        return obj.time_update