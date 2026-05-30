from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def quick_order_url(context, product):
    return product.get_primary_order_url(
        site_settings=context.get('site_settings'),
        request=context.get('request'),
    )
