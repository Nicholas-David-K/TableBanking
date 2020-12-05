from django.db import models

# Create your models here.

PAYMENT_PERIODS = (
	('OM', 'One Month'),
	('TM', 'Three Months')
)

PAYMENT_PERIODS_2 = (
	('TF', 'Twenty Four Months'),
	('TS', 'Thirty Six Months')
)

BOOSTER_TYPES = (
	('AG', 'Agriculture'),
	('ED', 'Education')
)

class Saving(models.Model):
	name = models.CharField(max_length=20, default='Saving')
	amount = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.name


class Booster(models.Model):
	name = models.CharField(max_length=20, choices=BOOSTER_TYPES)
	amount = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def booster_percent(self):
		return ((self.amount * 50) / 100) + self.amount

	def __str__(self):
		return f"{self.amount}"



class Repayment(models.Model):
	name = models.CharField(max_length=20)
	amount = models.IntegerField()

	def __str__(self):
		return self.name


class ShortTermInterest(models.Model):
	amount = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.amount}"


class LongTermInterest(models.Model):
	amount = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.amount}"


class Short_term(models.Model):
	name = models.CharField(max_length=20, default='Short Term')
	amount = models.IntegerField()
	payment_period = models.CharField(max_length=2, choices=PAYMENT_PERIODS)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	paid_months = models.ManyToManyField('Repayment', blank=True, null=True, related_name='short_terms')

	def first_second_month(self):
		total = (self.amount * 10) / 100
		return total 
	
	def final_amount(self):
		interest = (self.amount * 10) / 100
		total = self.amount + interest
		return total


	def save(self, *args, **kwargs):

		if ShortTermInterest.objects.all().exists() == True:
			current_interest = ShortTermInterest.objects.all().last().amount
		else:
			current_interest = 0

	
		short_term_interest_repayment = ((self.first_second_month()) * 1) / 100

		interest = ShortTermInterest()
		interest.amount = short_term_interest_repayment + current_interest
		interest.save()
		super(Short_term, self).save(*args, **kwargs)


	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Short Term'
		verbose_name_plural = 'Short Terms'





class Long_term(models.Model):
	name = models.CharField(max_length=20, default='Long Term')
	amount = models.IntegerField()
	amount_left = models.IntegerField(blank=True, null=True)
	payment_period = models.CharField(max_length=2, choices=PAYMENT_PERIODS_2)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def monthly_return_amount(self):
		if self.payment_period == "TS":
			return (self.amount / 36) * 1.12
		return (self.amount / 24) * 1.12


	def __str__(self):
		return self.name 


	class Meta:
		verbose_name = 'Long Term'
		verbose_name_plural = 'Long Terms'