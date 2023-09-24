from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super.__init__(self, *args, **kwargs)
        self.fields['transaction_type'].disable = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self):  # amount field ke filter korbo
        min_deposit_amount = 100
        # user er fillup kor a form theke amount field er value ke niye ashlam
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'you need to deposit at least {min_deposit_amount} $'
            )
        return amount
