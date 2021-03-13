import urllib
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode
import urllib.request
from dateutil.relativedelta import relativedelta

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile
from django.conf import settings


from geekshop.settings import BASE_DIR


def save_user_profile(backend, user, response, *args, **kwargs):
    # print(backend.name)
    # print(f'BACKEND: {backend.__dict__}')
    # print(f'BACKEND strategy: {backend.strategy.__dict__}')
    # print(f'USER: {user.__dict__}')
    # print(f'USER_state: {user._state.__dict__}')
    # print(f'RESPONSE: {response}')
    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_100')),
                                                    access_token=response['access_token'],
                                                    v='5.92')),
                              None
                              ))
        # print(f'API_URL: {api_url}')

        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        if data['sex']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        if data['about']:
            user.shopuserprofile.aboutMe = data['about']

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
            age = relativedelta(datetime.now(), bdate).years

            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')
            user.age = age

        if data['photo_100']:
            # avatar = requests.get(data['photo_100'])
            # with open(f'{BASE_DIR}{settings.MEDIA_URL}users_avatars/{user.pk}.jpg', 'wb') as f:
            #     f.write(avatar.content)
            urllib.request.urlretrieve(data['photo_100'], f'{settings.MEDIA_ROOT}/users_avatars/{user.pk}.jpg')
            user.avatar = f'users_avatars/{user.pk}.jpg'

        user.save()
    elif backend.name == 'github':

        urllib.request.urlretrieve(response['avatar_url'], f'{settings.MEDIA_ROOT}/users_avatars/{user.pk}.jpg')
        user.avatar = f'users_avatars/{user.pk}.jpg'
        # api_url = urlunparse(('https',
        #                       'api.github.com',
        #                       '/user',
        #                       None,
        #                       response['access_token'],
        #                       urlencode(OrderedDict(fields=','.join(('avatar_url',)),
        #                                             access_token=response['access_token'],
        #                                             v='5.92')),
        #                       None
        #                       ))

        # print(f'API_URL: {api_url}')



        # resp = requests.get(api_url)
        # # print(resp.status_code)
        # if resp.status_code != 200:
        #     return
        #
        # data = resp.json()['response'][0]
        # # print(f'DATA: {data}')
        # if data['sex']:
        #     user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE
        #
        # if data['about']:
        #     user.shopuserprofile.aboutMe = data['about']
        #
        # if data['bdate']:
        #     bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        #
        #     age = timezone.now().date().year - bdate.year
        #     if age < 18:
        #         user.delete()
        #         raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        #     user.age = age
        #
        # if data['photo_100']:
        #     # avatar = requests.get(data['photo_100'])
        #     # with open(f'{BASE_DIR}{settings.MEDIA_URL}users_avatars/{user.pk}.jpg', 'wb') as f:
        #     #     f.write(avatar.content)
        #     urllib.request.urlretrieve(data['photo_100'], f'{settings.MEDIA_ROOT}/users_avatars/{user.pk}.jpg')
        #     user.avatar = f'users_avatars/{user.pk}.jpg'

        user.save()

    elif backend.name == 'google-oauth2':

        urllib.request.urlretrieve(response['picture'], f'{settings.MEDIA_ROOT}/users_avatars/{user.pk}.jpg')
        user.avatar = f'users_avatars/{user.pk}.jpg'

        # if data['photo_100']:
        # avatar = requests.get(data['photo_100'])
            # with open(f'{BASE_DIR}{settings.MEDIA_URL}users_avatars/{user.pk}.jpg', 'wb') as f:
            #     f.write(avatar.content)
            # urllib.request.urlretrieve(response['photo_100'], f'{settings.MEDIA_ROOT}/users_avatars/{user.pk}.jpg')
            # user.avatar = f'users_avatars/{user.pk}.jpg'


        # api_url = urlunparse(('https',
        #                       'api.google.com',
        #                       '/method/users.get',
        #                       None,
        #                       urlencode(OrderedDict(fields=','.join(('keys_url',)),
        #                                             access_token=response['access_token'],
        #                                             v='5.92')),
        #                       None
        #                       ))
        # resp = requests.get(api_url)
        # print(resp.status_code)
        # if resp.status_code != 200:
        #     return
        #
        # data = resp.json()['response'][0]
        # print(f'DATA: {data}')
        # if data['sex']:
        #     user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE
        #
        # if data['about']:
        #     user.shopuserprofile.aboutMe = data['about']
        #
        # if data['bdate']:
        #     bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        #
        #     age = timezone.now().date().year - bdate.year
        #     if age < 18:
        #         user.delete()
        #         raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        #     user.age = age
        #
        # if data['photo_100']:
        #     # avatar = requests.get(data['photo_100'])
        #     # with open(f'{BASE_DIR}{settings.MEDIA_URL}users_avatars/{user.pk}.jpg', 'wb') as f:
        #     #     f.write(avatar.content)
        #     urllib.request.urlretrieve(data['photo_100'], f'{settings.MEDIA_ROOT}/users_avatars/{user.pk}.jpg')
        #     user.avatar = f'users_avatars/{user.pk}.jpg'

        user.save()
    else:
        return
