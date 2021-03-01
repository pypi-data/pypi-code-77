from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import transaction


def update(request):
    try:
        if request.user.is_authenticated and request.session.session_key is not None:
            with transaction.atomic():
                # print(request.session.session_data)
                master_session = Session.objects.get(session_key=str(request.session.session_key))
                print(master_session.session_key)
                for i in settings.DATABASES:
                    if i != 'default':
                        try:
                            sync_session = Session.objects.using(i).get(session_key=master_session.session_key)
                            sync_session.session_data = master_session.session_data
                            sync_session.expire_date = master_session.expire_date
                            sync_session.save()
                        except Session.objects.using(i).model.DoesNotExist:
                            Session.objects.using(i).create(session_key=master_session.session_key,
                                                            session_data=master_session.session_data,
                                                            expire_date=master_session.expire_date)
    except:
        print('already have session key')
