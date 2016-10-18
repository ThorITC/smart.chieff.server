from django.db import models

# Create your models here.
class Proxy(models.Model):

    class Meta:
        db_table = "ProxyTable"

    proxy_ip = models.CharField(max_length=20)
    proxy_port = models.IntegerField()
    active = models.BooleanField(default=True)

    def set_proxy(self, ip, port):
        if not Proxy.objects.filter(proxy_ip=ip):
            Proxy(proxy_ip=ip, proxy_port=port).save()

    def get_proxy(self, id=0):
        if len(Proxy.objects.all()) > 0:
            #try:
                result = Proxy.objects.get(id=id).values('proxy_ip', 'proxy_port')
                if self.check_proxy_to_valid(result['proxy_ip'], result['proxy_port']):
                    return {'ip': result['proxy_ip'], 'port': result['proxy_port']}
                id = id + 1
                self.change_proxy_activiti(result['proxy_ip'], False)
            #except:
            #    id = 0
            #self.get_proxy(id)
        else:
            return None

    def change_proxy_activiti(self, ip, activiti_flag=True):
        try:
            proxy = Proxy.objects.get(proxy_id=ip)
            if proxy:
                proxy.active = activiti_flag
                proxy.save()
        except:
            pass

    def check_proxy_to_valid(self, ip, port):
        #try:
            
            return True
        #except:
        #    return False
