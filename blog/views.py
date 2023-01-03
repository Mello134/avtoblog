from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy  # перенаправление
from django.views.generic import UpdateView, DeleteView, DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from relatepost.forms import RatingForm
from relatepost.models import LikeMarkPost, Rating
from .forms import CarAddForm, CarUpdateForm  # наши формы forms.py (blog app)
from comments.forms import CommentForm  # наши формы forms.py (comments app)
from .models import *
from .utils import DataMixin
from unidecode import unidecode  # преобразование символов в UTF8
from django.template.defaultfilters import slugify  # преобразование строки в slug


# http://127.0.0.1:8000, вход на сайт
def show_index(request):
    return render(request, 'blog/index.html', {'title': 'Вход на сайт'})


# домашняя страница Блога (отображение всех машин)
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


# вывод машин избранных статей пользователя
class CarsBookmarksShow(LoginRequiredMixin, DataMixin, ListView):
    login_url = 'login'  # перенаправление если пользователь не авторизован (LoginRequiredMixin)
    model = Car
    template_name = 'blog/bookmarks.html'  # шаблон
    context_object_name = 'cars'  # objects = cars (просто имя)
    # allow_empty = True - покажет пустой список если ничего не будет
    # allow_empty = False - покажет 404, при отсутствии совпадений в get_queryset
    allow_empty = True  # для отображения 404

    # параметры вывода (выводим записи только из, закладок пользователя)
    def get_queryset(self):
        # получаем список всех записей LikeMarkPost ао фильтру (текущий пользователь, есть закладка)
        bookmarks_post_list = LikeMarkPost.objects.filter(user_like_mark__pk=self.request.user.pk,
                                                          is_bookmarks_post=True)
        pk_list_bookmarks_for_user = []  # создал пустой список pk
        # перебираем все записи по вышеуказанной выборке
        for one_rec in bookmarks_post_list:
            # добавляю в наш список, id/pk записей, которые есть в закладки
            pk_list_bookmarks_for_user.append(one_rec.post_like_mark.pk)
        # Вывожу только записи из закладок
        # pk - это Car.pk,  __in - необходим когда атрибутов одного поля несколько
        # после __in - атрибуты поиска нужно выводить списком
        # пример = Model.objects.filter(цвет__in=['белый','чёрный','синий'])
        return Car.objects.filter(pk__in=pk_list_bookmarks_for_user)

    # полный контекст
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(cat_selected='закладки',
                                      title=f'Избранные статьи')
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

    # получение реакций пользователя к посту
    def get_user_relation_to_post(self, **kwargs):
        # пробуем получить реакции (лайк И ИЛИ закладки)
        # по pk пользователя и slag статьи
        relation = LikeMarkPost.objects.filter(user_like_mark__pk=self.request.user.pk,
                                               post_like_mark__slug=self.kwargs['car_slug'])
        # если количество реакций > 0
        if relation.count() > 0:
            return relation  # возвращаем весь QuerySet
        else:
            relation = 'no'
            return relation  # возвращаем строку 'no' (для проверки в шаблоне)

    # получение рейтинга поста
    def get_rating_post(self, **kwargs):
        # получаем все записи рейтинга к конкретному посту
        rating_records = Rating.objects.filter(post_rate__slug=self.kwargs['car_slug'])
        sum_rating = 0  # промежуточная переменная, сумма всех рейтингов
        # если количество записей рейтинга больше 0
        if rating_records.count() > 0:
            # перебираем все записи модели Rating
            for rec in rating_records:
                # к переменной прибавляем рейтинг из каждой записи Rating (конкретного поста)
                # value - потому что поле star не совсем число, и его нужно привести к числу!
                sum_rating += rec.star.value
            # сумма всех рейтингов / количество записей по рейтингу
            rating = sum_rating / rating_records.count()
            # округляем до 2-х чисел после запятой
            rating = round(rating, 2)
        else:  # если к посту рейтинг никто не ставил
            rating = 0
        return rating  # возвращаем итоговый рейтинг!

    # получение количества лайков к посту
    def get_total_likes_post(self, **kwargs):
        # получаю все записи реакций (лайк и/или закладки) относящиеся к конкретному посту
        likes_or_marks_records = LikeMarkPost.objects.filter(post_like_mark__slug=self.kwargs['car_slug'])
        total_likes = 0
        # если реакций (количество записей) лайк и/или закладки больше 0
        if likes_or_marks_records.count() > 0:
            # перебираем все записи
            for rec in likes_or_marks_records:
                # упрощено от if rec.is_like_post == True:
                # если в записи в поле лайков стоит True
                if rec.is_like_post:
                    # прибавляем к результату единицу
                    total_likes += 1
        return total_likes  # возвращаем подсчёт лайков

    # формируем полный контекст
    # kwargs = {'cat_slug': self.cat.slug, 'car_slug': self.slug}
    # kwargs (пример из одного поста) = {'cat_slug': 'italy', 'car_slug': 'ferrari-488-gtb'}
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # распаковываем изначальный контекст
        context['star_form'] = RatingForm()  # добавляем нашу форму в контекст (ключ star_form: значение=наша форма)
        c_def = self.get_user_context(cat_selected=self.kwargs['cat_slug'],  # выбор категории
                                      relation=self.get_user_relation_to_post(),  # реакции
                                      rating=self.get_rating_post(),  # рейтинг
                                      total_likes=self.get_total_likes_post(),  # количество лайков
                                      )
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
            car.slug = slugify(unidecode(car.title))  # Автозаполнение slug/слага! по заполненному в форме полю title
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

