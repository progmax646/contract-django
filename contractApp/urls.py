from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.loginPage),
    path('logout', views.logout_user, name='logout'),

    path('contract/get-user/<int:id>', views.contract_index, name='contract'),

    # статус контракта
    path('contract/status1/<int:id>', views.contract_status),
    path('contract/status-del/<int:id>', views.contract_status_del),
    path('contract/status-success/<int:id>', views.contract_status_success),

    # фильтр по контрактам
    path('contract/search', views.contract_search),

    # добавление записей в контракт
    path('contract/edit/<int:id>', views.edit_contract),

    # word to pdf
    path('contract/get-pdf/<int:id>', views.get_pdf),

    path('contract/get-page-statuz/<int:inn>', views.get_page),

    path('contract/get-capcha-statuz', views.get_capcha),

#     didox

    path('contract/didox', views.dodox_test),

#     создание пользователей и клиентов

    path('contract/user', views.getUser),

    path('contract/user/create', views.createUser),

    path('contract/all-clients/<int:group>', views.get_client_list)

]


# правило для сохранения файлов

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
