from django.contrib import admin

from .models import Saving, Short_term, Long_term, Booster, Repayment, ShortTermInterest, LongTermInterest

# Register your models here.
class SavingAdmin(admin.ModelAdmin):
  list_display = ('amount', 'created_at')
  list_display_links = ('amount',)

admin.site.register(Saving, SavingAdmin)


class ShortTermAdmin(admin.ModelAdmin):
  list_display = ('amount', 'payment_period', 'created_at')
  list_display_links = ('amount',)

admin.site.register(Short_term, ShortTermAdmin)


class LongTermAdmin(admin.ModelAdmin):
  list_display = ('amount', 'payment_period', 'created_at')
  list_display_links = ('amount',)

admin.site.register(Long_term, LongTermAdmin)




class BoosterAdmin(admin.ModelAdmin):
  list_display = ('amount', 'name', 'created_at')

admin.site.register(Booster, BoosterAdmin)




class RepaymentAsmin(admin.ModelAdmin):
  list_display = ('amount', 'name')
  list_display_links = ('amount',)

admin.site.register(Repayment, RepaymentAsmin)



admin.site.register(ShortTermInterest)

admin.site.register(LongTermInterest)