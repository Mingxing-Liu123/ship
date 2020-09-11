from django.contrib import admin
from .models import Management,SimulationParament

# Register your models here.
@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display=('name','office_address')


@admin.register(SimulationParament)
class SimulationParamentAdmin(admin.ModelAdmin):
    list_display=('SimulationUser','Modulation','MACPtorocols')

#注册模型
from .models import MSG_PH_Attribute,MSG_Press_Attrubute,MSG_Temperature_Attribute # 信息采集三大属性
from .models import Net_Attribute # 网络属性，MAC属性，地理属性
from .models import Raw_Node,Time_Node #原生节点，时刻节点
admin.site.register(MSG_PH_Attribute)
admin.site.register(MSG_Press_Attrubute)
admin.site.register(MSG_Temperature_Attribute)

admin.site.register(Net_Attribute)
admin.site.register(Time_Node)
admin.site.register(Raw_Node)

from .models import Topic,Message_Board
admin.site.register(Topic)
admin.site.register(Message_Board)

from .models import UanEmulation
admin.site.register(UanEmulation)
