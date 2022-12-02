from blog.models import Category  # наша модель

all_categories = Category.objects.all()  # общий для всех список в sidebar


# общий класс
class DataMixin:
    # формируем общий контекст
    def get_user_context(self, **kwargs):
        # контекст будет словарём {'ключ':'значение'}
        context = kwargs
        # в словарь контекст добавили { 'all_categories' : Category.objects.all()}
        context['all_categories'] = all_categories
        # if 'cat_selected'
        return context
