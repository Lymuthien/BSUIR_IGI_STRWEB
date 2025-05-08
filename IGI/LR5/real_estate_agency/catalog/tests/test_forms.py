from django import forms
from django.test import TestCase
from ..forms import PurchaseRequestForm


class PurchaseRequestFormTest(TestCase):
    def test_form_fields(self):
        form = PurchaseRequestForm()
        self.assertEqual(list(form.fields.keys()), ["message"])

    def test_message_label(self):
        form = PurchaseRequestForm()
        self.assertEqual(form.fields["message"].label, "")

    def test_message_widget_attrs(self):
        form = PurchaseRequestForm()
        widget = form.fields["message"].widget
        self.assertEqual(widget.attrs["rows"], 3)
        self.assertEqual(widget.attrs["placeholder"], "Ваши пожелания и вопросы...")
        self.assertIsInstance(widget, forms.Textarea)

    def test_form_message(self):
        test_message = "Test message"
        form_data = {"message": test_message}
        form = PurchaseRequestForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_empty_message(self):
        form_data = {"message": ""}
        form = PurchaseRequestForm(data=form_data)
        self.assertTrue(form.is_valid())
