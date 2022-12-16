from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy  # перенаправление
from django.views.generic import UpdateView, DeleteView, DetailView, ListView
from django.views.generic.edit import FormMixin

from .forms import CarAddForm, CarUpdateForm  # наши формы forms.py (blog app)
from comments.forms import CommentForm  # наши формы forms.py (comments app)
from .models import *
from .utils import DataMixin


# домашняя страница (отображение всех машин)
class CarsAllShow(DataMixin, ListView):
    paginate_by = 6  # пагинация
    model = Car  # модель cars = Car.objects.all()
    template_name = 'blog/home.html'  # шаблон
    context_object_name = 'cars'  # objects = cars (просто имя)

    # формируем полный контекст
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # контекст Car.object.all()
        c_def = self.get_user_context(cat_selected='all',
                                      title='Все модели')  # наш контекст + DataMixin
        return {**context, **c_def}  # в шаблон передаём полный контекст


# вывод машин по категориям
class CarsCategoryShow(DataMixin, ListView):
    paginate_by = 2
    model = Car
    template_name = 'blog/category.html'
    context_object_name = 'cars'
    allow_empty = False  # для отображения 404

    # параметры вывода (выводим записи только определенной категории)
    def get_queryset(self):
        return Car.objects.filter(cat__slug=self.kwargs['cat_slug'])

    # полный контекст
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # получение выбранной категории - для получения параметров категории
        select_category = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(cat_selected=select_category.slug,
                                      title=f'Производство: {select_category.name}')
        return {**context, **c_def}


# страница отдельной машины
class ShowCar(SuccessMessageMixin, DataMixin, DetailView, FormMixin):
    model = Car
    template_name = 'blog/car.html'
    # !указываем только car_slug - из get_absolute_ur
    # !несмотря на то что в пути есть и car_slug ? почему так хз
    slug_url_kwarg = 'car_slug'  # !для пути 'category/<slug:cat_slug>/<slug:car_slug>/'
    # context_object_name = 'car'  # обращаемся в шаблоне {{ car.поле }} - вместо object
    form_class = CommentForm  # наша форма для комментариев
    success_message = "Комментарий успешно создан!"  # всплывающий комментарий {% if messages %} - {% for m in messages %}

    # определим перенаправление на нашу страницу, после отправки комментария, так как в пути у нас есть cat_slug, car_slug
    def get_success_url(self, **kwargs):
        # get_object() - это по сути Car.objects.get(1 штука)
        # kwargs - мы добавляем /<slug:cat_slug>/<slug:car_slug>/
        # полный наш путь равен пути path = 'car' - для этого и добавляли cat_slug car_slug
        # То есть при успешном заполнении формы (отправка комментария, нас оставит на этой же странице)
        return reverse_lazy('car', kwargs={'cat_slug': self.get_object().cat.slug, 'car_slug': self.get_object().slug})

    # переопределяем метод пост (для того чтобы сохранялись комментарии)
    # self - это все объекты класса
    # request- запрос от пользователя
    def post(self, request, **kwargs):
        form = self.get_form()  # в переменной form занесли ту форму которую отправили
        # 2
        if form.is_valid():  # проверка правильности формы
            return self.form_valid(form)  # выполняется после form_valid - передаёт уже сохранённую форму
        else:
            return self.form_invalid(form)  # иначе вернёт что у нас неправильно

    # 1
    def form_valid(self, form):  # берём форм
        self.object = form.save(commit=False)
        self.object.car_post = self.get_object()  # получение и запись экземпляра статьи (одной машины)
        self.object.author_comment = self.request.user  # получение и запись имени автора
        self.object.save()  # форма пересохраняется с новыми данными
        return super().form_valid(form)  # форма передаётся в базу данных и программа продолжит свои действия

    # формируем полный контекст
    # kwargs = {'cat_slug': self.cat.slug, 'car_slug': self.slug}
    # kwargs (пример из одного поста) = {'cat_slug': 'italy', 'car_slug': 'ferrari-488-gtb'}
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # распаковываем изначальный контекст
        c_def = self.get_user_context(cat_selected=self.kwargs['cat_slug'])
        return {**context, **c_def}  # в шаблон передаём полный контекст


# можно сделать через класс представления CreateView
# можно запретить не авторизованным пользователем - через класс LoginRequiredMixin
# оставил как есть - для наглядности
# добавление нового поста
def show_add_post(request):
    if request.method == 'POST':  # если уже введены какие-то данные
        # request.FILES - Обязательно если есть файлы, изображения и ТД
        form = CarAddForm(request.POST, request.FILES)  # форма = заполненная форма
        if form.is_valid():  # проверка правильности формы, если форма заполнена правильно
            car = form.save(commit=False)  # commit=False - когда нужно внести изменение в поле модели не из формы!
            car.author = request.user  # поле автора заполняется автоматически (залогиненый пользователь)
            car.save()  # сохраняем модель
            return redirect('home')  # перенаправление домой при успешном заполнении
    else:  # если никаких данный пользователь ещё не вводил
        form = CarAddForm()  # отображаем пустую форму для заполнения

    all_categories = Category.objects.all()
    context = {
        'title': 'Добавление статьи',
        'all_categories': all_categories,
        'form': form,
      }
    return render(request, 'blog/add_post.html', context=context)


# редактирование Поста
class UpdatePostView(DataMixin, UpdateView):
    model = Car  # связываемся с моделью Car
    form_class = CarUpdateForm  # связываемся с формой
    # указываем только car_slug - из get_absolute_ur
    # несмотря на то что в пути есть и car_slug ? почему так хз
    slug_url_kwarg = 'car_slug'
    template_name = 'blog/update_post.html'  # путь к шаблону

    # формируем полный контекст
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # распаковываем изначальный контекст
        c_def = self.get_user_context(title='Изменение поста')  # переменная контекста DataMixin + title
        return {**context, **c_def}  # в шаблон передаём полный контекст


# Представление для удаления статьи
class DeletePostView(DataMixin, DeleteView):
    model = Car  # модель из models.py
    template_name = 'blog/delete_post.html'  # шаблон
    success_url = reverse_lazy('home')  # после удаления отправит домой

    # !указываем только car_slug - из get_absolute_ur
    # !несмотря на то что в пути есть и car_slug ? почему так хз
    slug_url_kwarg = 'car_slug'

    # form_class = не нужно никакой формы

    # формируем полный контекст
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # распаковываем изначальный контекст
        c_def = self.get_user_context(title='Удаление поста')  # переменная контекста DataMixin + title
        return {**context, **c_def}  # в шаблон передаём полный контекст




