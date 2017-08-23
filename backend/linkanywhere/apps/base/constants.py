from django.utils.translation import ugettext as _

DRAFT = 'd'
PUBLISHED = 'p'

PUBLICATION_STATUS_CHOICES = (
    (DRAFT, _('draft')),
    (PUBLISHED, _('published')),
)
