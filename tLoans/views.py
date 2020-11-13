from django.shortcuts import render

from .forms import (ShortTermForm, 
                   ReturnShortLoan, 
                   LongTermForm, 
                   ReturnLongTerm, 
                   SavingForm, 
                   RemoveSavingForm, 
                   BoosterForm)

from django.views import View

from django.shortcuts import redirect

from .models import Short_term, Repayment, ShortTermInterest, Long_term, LongTermInterest, Saving, Booster

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
class Home(LoginRequiredMixin, View):
  def get(self, request):
    context = {
      'form': ShortTermForm,
      'form2': LongTermForm,
      'saving_form': SavingForm,
      'saving': Saving.objects.all().last(),
      'remove_saving_form': RemoveSavingForm,
      'short_loans': Short_term.objects.all(),
      'long_loans': Long_term.objects.all()
    }
    return render(self.request, 'tLoans/home.html', context)

  def post(self, request):
    # get form data
    form = ShortTermForm(request.POST or None)
    form2 = LongTermForm(request.POST or None)
    if form.is_valid():
      amount = form.cleaned_data.get('amount')
      payment_period = form.cleaned_data.get('payment_period')


      # validation
      if int(amount) < 1:
        messages.error(request, 'You cannot loan that amount')
        return redirect('home')
      else:
        # save short term loan request
        loan = Short_term(
          amount=amount,
          payment_period=payment_period
        )
        loan.save()
        messages.success(request, 'You have successfully made a loan')
        return redirect('short-term')

    if form2.is_valid():
      amount = form2.cleaned_data.get('amount')
      payment_period = form2.cleaned_data.get('payment_period')

      # validation
      if int(amount) < 1:
        messages.error(request, "You cannot loan that amount")
        return redirect('homt')
      else:
        loan = Long_term(
          amount = amount,
          payment_period = payment_period
        )
        loan.save()
        messages.success(request, "You have successfully made a loan")
        return redirect('long-term')
    messages.error(self.request, 'Something went wrong')
    return redirect('home')

# add short term
class ShortTerm(LoginRequiredMixin, View):
  def get(self, *args, **kwargs):
    context = {
      'form': ReturnShortLoan,
      'loans': Short_term.objects.all(),
      'repayments': Repayment.objects.filter(name='Short Term')
    }
    return render(self.request, 'tLoans/short_term.html', context)


  def post(self, *args, **kwargs):
    # get form data
    form = ReturnShortLoan(self.request.POST or None)
    if form.is_valid():
      amount = form.cleaned_data.get('amount')

      first_two_months_amount = Short_term.objects.all()[0].first_second_month()
      final_month_amount = Short_term.objects.all()[0].final_amount()
      
      

      if amount != first_two_months_amount and amount != final_month_amount:
        messages.error(request, "You cannot repay that amount")
        return redirect('short-term')
      else:
        loan = Short_term.objects.all()[0]

        repayment = Repayment(
          name = "Short Term",
          amount = amount
        )
        repayment.save()
        loan.paid_months.add(repayment.id)
      return redirect('short-term')

# add long term
class LongTerm(LoginRequiredMixin, View):
  def get(self, *args, **kwargs):
    context = {
      'form': ReturnLongTerm(),
      'loans': Long_term.objects.all(),
      'repayments': Repayment.objects.filter(name='Long Term')
    }
    return render(self.request, 'tLoans/long_term.html', context)

  def post(self, *args, **kwargs):

    # get form data
    form = ReturnLongTerm(self.request.POST or None)
    if form.is_valid():
      amount = form.cleaned_data.get('amount')
      
      loan = Long_term.objects.all().first()

      # validation
      if int(amount) >= loan.monthly_return_amount():
        # subtract from loaned amount
        if not loan.amount_left:
          loan.amount_left = loan.amount

        loan.amount_left -= amount

        # add payment to repayment
        repayment = Repayment(
          name = "Long Term",
          amount = amount
        )

        # add long term interest repayment
        if loan.payment_period == 'TF':
          total = (loan.amount / 24) 
        else:
           total = (loan.amount / 36)

        if LongTermInterest.objects.all().exists() == True:
          current_interest = LongTermInterest.objects.all().last().amount
        else:
          current_interest = 0

        long_term_interest_repayement = (total * 1.12) - total

        interest = LongTermInterest(
          amount = long_term_interest_repayement + current_interest
        )
        loan.save()
        repayment.save()
        interest.save()

        # check if loan is completed:
        if not loan.amount_left > 0:
          messages.success(self.request, "You have finished repaying your loan")
          return redirect('long-term')
      else:
        messages.error(self.request, 'You cannot pay that amount')
        return redirect('long-term')
    return redirect('long-term')

# save booster
class SaveBooster(LoginRequiredMixin, View):
  def get(self, *args, **kwargs):
    context = {
      'form': BoosterForm,
      'education': Booster.objects.filter(name='ED').last(),
      'agriculture': Booster.objects.filter(name='AG').last()
    }
    return render(self.request, "tLoans/boosters.html", context)

  def post(self, *args, **kwargs):
    form = BoosterForm(self.request.POST or None)
    if form.is_valid():
      amount = form.cleaned_data.get('amount')
      name = form.cleaned_data.get('name')

      booster = Booster()

      # check current booster
      if amount >= 200:
        if Booster.objects.filter(name=name).exists() == True:
          current_booster = Booster.objects.filter(name=name).last().amount
          booster.name = name
          booster.amount += (amount + current_booster)
          booster.save()
          messages.success(self.request, 'Booster successfully added')
          return redirect('save_booster')
        else:
          booster.name = name
          booster.amount = amount
          booster.save()
          messages.success(self.request, 'Booster successfully added')
          return redirect('save_booster')
      messages.error(self.request, 'You cannot save that amount')
      return redirect('save_booster')

      return redirect('save_booster')



# Add savings
class AddSavings(LoginRequiredMixin, View):
  def post(self, *args, **kwargs):
    form = SavingForm(self.request.POST or None)
    if form.is_valid():
      amount = form.cleaned_data.get('amount')

      # check if there's a saving
      if Saving.objects.all().first():
        current_amount = Saving.objects.all().last().amount
      else:
        current_amount = 0
      
      saving = Saving()
      if amount < 2000:
        messages.error(self.request, "You cannot save that amount")
        return redirect('home')
      else:
        saving.amount = (amount + current_amount)
        saving.save()

        messages.success(self.request, 'Saving successfully added')
        return redirect('home') # return redirect to table
    messages.error(self.request, 'Something went wrong')
    return redirect('home')


# deduct savings
class DeductSaving(LoginRequiredMixin, View):
  def post(self, *args, **kwargs):
    form = RemoveSavingForm(self.request.POST or None)
    if form.is_valid():
      amount = form.cleaned_data.get('amount')

      saving = Saving.objects.all().last()
      if amount > saving.amount:
        messages.error(self.request, "You cannot deduct that amount")
        return redirect('home')
      else:
        saving.amount -= amount
        saving.save()
        messages.success(self.request, 'Amount successfully deducted from your savings')
        return redirect('home')
    messages.error(self.request, 'Something went wrong')
    return redirect('home')


class LoanInformation(LoginRequiredMixin, View):
  def get(self, *args, **kwargs):
    context = {
      'saving': Saving.objects.all().last(),
      'short_term': Short_term.objects.all().first(),
      'long_term': Long_term.objects.all().first(),
      'short_term_interest': ShortTermInterest.objects.all().last(),
      'long_term_interest': LongTermInterest.objects.all().last(),
      'education': Booster.objects.filter(name='ED').last(),
      'agriculture': Booster.objects.filter(name='AG').last()
    }
    return render(self.request, 'tLoans/table.html', context)

# delete payment 
class DeleteLongTermPayment(LoginRequiredMixin, View):

  def get(self, request, pk):
    try:
      repayment = Repayment.objects.filter(pk=pk)
      if repayment.exists():
        amount = repayment.first()
        amount.delete()

        # re-add amount to amount_left
        loan = Long_term.objects.all().first()
        loan.amount_left += amount.amount
        loan.save()
        return redirect('long-term')
    except ObjectDoesNotExist:
      messages.error(request, 'Something went wrong')
      return redirect('long-term')


# delete Short Terms
class DeleteShortTermLoan(LoginRequiredMixin, View):

  def get(self, request, pk):
    try:
      loan = Short_term.objects.filter(pk=pk)
      if loan.exists():
        loan = loan.first()
        loan.delete()
        messages.success(request, 'Loan successfully deleted')
        return redirect('home')
    except ObjectDoesNotExist:
      messages.error(request, 'Something went wrong')
      return redirect('short_term')

# delete long term Loan
class DeleteLongTermLoan(LoginRequiredMixin, View):

  def get(self, request, pk):
    try:
      loan = Long_term.objects.filter(pk=pk)
      if loan.exists():
        loan = loan.first()
        loan.delete()
        messages.success(self.request, 'Loan successfully deleted')
        return redirect('long-term')
    except ObjectDoesNotExist:
      messages.error(self.request, 'Something went wrong')
      return redirect('long-term')

