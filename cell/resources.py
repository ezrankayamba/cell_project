from import_export import resources
from .models import Member
import re


class MemberResource(resources.ModelResource):
    regex = '(\d{9})\.0$'

    class Meta:
        model = Member

    def before_save_instance(self, instance, using_transactions, dry_run):
        print(instance.phone_no)
        instance.phone_no = f'255{re.findall(self.regex, str(instance.phone_no))[0]}'
        print(instance.phone_no)
        return instance
