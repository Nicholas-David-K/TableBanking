from django import forms
from .models import Short_term, Long_term, Saving, Booster



class ShortTermForm(forms.ModelForm):
  
  class Meta:
    model = Short_term
    fields = ('amount', 'payment_period')
    widgets = {
      'amount': forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Amount to loan...',
        'type': 'number'
      }),
      'payment_period': forms.Select(attrs={
        'class': 'form-control',
        'name': 'loan-period',
        'required': 'required'
      })
    }


class LongTermForm(forms.ModelForm):

  class Meta:
    model = Long_term
    fields = ('amount', 'payment_period')
    widgets = {
      'amount': forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Amount to loan...',
        'type': 'number'
      }),
      'payment_period': forms.Select(attrs={
        'class': 'form-control',
        'name': 'payment-period',
        'required': 'required'
      })
    }

class ReturnShortLoan(forms.ModelForm):

  class Meta:
    model = Short_term
    fields = ('amount',)
    widgets = {
      'amount': forms.NumberInput(attrs={
        'class': 'form-control',
        'type': 'number',
        'placeholder': 'Amount to repay...'
      })
    }

class ReturnLongTerm(forms.ModelForm):

  class Meta:
    model = Long_term
    fields = ('amount',)
    widgets = {
      'amount': forms.NumberInput(attrs={
        'class': 'form-control',
        'type': 'number',
        'placeholder': 'Amount to repay...'
      })
    }


class SavingForm(forms.ModelForm):

  class Meta:
    model = Saving
    fields = ('amount',)
    widgets = {
      'amount': forms.NumberInput(attrs={
        'type': 'number',
        'placeholder': 'Amount to save...',
        'class': 'form-control'
      })
    }

class RemoveSavingForm(forms.ModelForm):

  class Meta:
    model = Saving
    fields = ('amount',)
    widgets = {
      'amount': forms.NumberInput(attrs={
        'type': 'number',
        'placeholder': 'Amount to deduct...',
        'class': 'form-control'
      })
    }

class BoosterForm(forms.ModelForm):

  class Meta:
    model = Booster
    fields = ('name', 'amount')
    widgets = {
      'name': forms.Select(attrs={
        'class': 'form-control',
        'required': 'required'
      }),
      'amount': forms.NumberInput(attrs={
        'type': 'number',
        'placeholder': 'Amount to save...',
        'class': 'form-control',
        'required': 'required'
      })
    }