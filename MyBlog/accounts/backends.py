from .models import User

class EmailBackend(object):

    def authenticate(self,email=None,password=None,**kwargs):
        print("in backend")
        try:
            user=User.objects.get(email=email)
        except User.MultipleObjectsReturned:
           user.objects.filter(email=email).order_by('id').first()
        except User.DoesNotExist:
            return None

        if getattr(user,'is_active' and user.check_password(password)):
            return user
        return None

        def get_user(self,user_id):
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None
