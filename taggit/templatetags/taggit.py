from django.template import Library

register = Library()

def regroup_by_tag(queryset, name=None, slug=None, namespace=None):
  if name is None and slug is None and namespace is None:
    return queryset

  # We need to create a new queryset, otherwise any earlier tag filtering will
  # mess up the extra select
  pk_list = [obj.pk for obj in queryset]
  qs = queryset.model.objects.all()

  if name is not None:
    qs = qs.filter(tags__name=name)

  if slug is not None:
    qs = qs.filter(tags__slug=slug)

  if namespace is not None:
    qs = qs.filter(tags__namespace=namespace)

  qs = qs.order_by('tags__name').extra(select={
        'tag_id': 'taggit_tag.id',
        'tag_name': 'taggit_tag.name',
        'tag_slug': 'taggit_tag.slug',
        'tag_namespace': 'taggit_tag.namespace',
        })
  return qs

def strip_namespace(name):
  return name.partition(":")[2] if name.partition(":")[1] == ":" else name


register.assignment_tag(regroup_by_tag)
register.filter(strip_namespace)
