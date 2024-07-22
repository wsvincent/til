# Previous and Next Links in a Template

I had a use case of needing links to the previous or next page for a Section. This was a little tricky and I'm sure there is a more elegant way to do this, but for posterity here is the example.

I have a `Course` model that has a related `Section`.

```python
# courses/models.py
from django.db import models
from django.urls import reverse

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)
    description = models.CharField(max_length=200)
    content = models.TextField()
    price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    def str(self):
        return self.title

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})

    def get_price(self):
        return f"{self.price / 100:.2f}"

class Section(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="sections",
    )
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(null=False, unique=False)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        unique_together = ("course", "slug")

    def str(self):
        return self.title

    def get_absolute_url(self):
        return reverse("section_detail", args=[self.course.slug, self.slug])
```

I have three views for course list, course detail, and section detail.

```python
# courses/views.py
from django.views.generic import DetailView, ListView

from .models import Course, Section

class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "courses/course_list.html"

class CourseDetailView(DetailView):
    model = Course
    context_object_name = "course"
    template_name = "courses/course_detail.html"

class SectionDetailView(DetailView):
    model = Section
    context_object_name = "section"
    template_name = "sections/section_detail.html"
    slug_url_kwarg = "section_slug"

    def get_queryset(self):
        return Section.objects.filter(
            course__slug=self.kwargs["slug"], slug=self.kwargs["section_slug"]
        )
```

Now here's how to update the context data on the section detail page.

```python
# courses/views.py
from django.shortcuts import get_object_or_404  # new

class SectionDetailView(DetailView):
    model = Section
    context_object_name = "section"
    template_name = "sections/section_detail.html"
    slug_url_kwarg = "section_slug"

    def get_queryset(self):
        return Section.objects.filter(
            course__slug=self.kwargs["slug"], slug=self.kwargs["section_slug"]
        )

    # new here...
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        current_section = self.object
        
        context['next_section'] = Section.objects.filter(
            course=course, order__gt=current_section.order
        ).order_by('order').first()
        
        context['previous_section'] = Section.objects.filter(
            course=course, order__lt=current_section.order
        ).order_by('-order').first()
        
        return context
```

And here is the template that uses this context data for the previous/next links.

```html
<!-- templates/section_detail.html -->
 {% extends "base.html" %}

{% block content %}
<h1>{{ section.title }}</h1>
<p>{{ section.description }}</p>

<div class="section-content">
    {{ section.content|safe }}
</div>

<div class="navigation-buttons">
    {% if previous_section %}
        <a href="{{ previous_section.get_absolute_url }}" class="btn btn-primary">Previous: {{ previous_section.title }}</a>
    {% endif %}

    {% if next_section %}
        <a href="{{ next_section.get_absolute_url }}" class="btn btn-primary">Next: {{ next_section.title }}</a>
    {% endif %}
</div>

<p><a href="{{ section.course.get_absolute_url }}">Back to {{ section.course.title }}</a></p>
{% endblock %}
```

This works and the template logic means it doesn't show previous or next links on there isn't one.