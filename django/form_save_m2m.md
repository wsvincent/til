# Form save_m2m() when commit=False

Carlton Gibson's [DjangoCon Europe 2024 talk](https://youtu.be/cLHVM31Rv6A?si=PnDA5LtFCm10Z0W_) highlighted this aspect of working with forms and the [save() method](https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/#the-save-method).

To wit, `commit=False` is often added to a form whenever we want to do some custom processing on the object before saving it (which is often). If our model has a many-to-many relation with another model we have to be careful: Django can't immediately save the form data for the M2M relation because it isn't possible to save M2M data for an instance until the instance exists in the database.

The fix? Add `form.save_m2m()`.

Example code from Carlton's talk:

```python
# form.py
def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    # Probably need this too...
    form.save_m2m()
    return HttpResponseRedirect(
        self.get_success_url()
    )
```