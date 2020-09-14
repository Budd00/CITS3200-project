from django.db import models
import uuid

# Create your models here.
class member_info(models.Model):
    username = models.CharField(max_length= 50, default= '')
    student_number = models.IntegerField(default=00000000)
    user_name = models.CharField(max_length = 50)
    password = model.CharField(max_length = 50)
    member_name = models.CharField(max_length=100, null= False)
    notes = models.CharField(max_length=250)
    dob = models.DateField(null=False)
    is_committee = models.BooleanField(default=False)
    pronouns = models.CharField(max_length=25)
    join_date = models.DateField(null=False)  # initial join date
    def __str__(self):
        result = " user name: " + self.username \
                 + " student_number: " + str(self.student_number) \
                + " member_name: " + self.member_name \
                + " notes: " + self.notes \
                + " dob" + str(self.dob) \
                + " is_commitee: "+ str(self.is_committee) \
                + " pronouns: " + self.pronouns \
                + " join date: " + str(self.join_date)
        return result
# only for current memberships - replication of the membership form
class member_details(models.Model):
    detail_id = models.AutoField(primary_key = True)
    id = models.ForeignKey("member_info", on_delete= models.CASCADE)
    email = models.EmailField(max_length=50,null=False)
    phone_num = models.IntegerField(null=False)
    # for later, if active date is null, check current expiry date against last
    # active date value. If difference is x amount of time, check against member_info,
    # if notes = NULL. Delete member data
    active_date = models.DateField # can be null, if null, no current member ship
    expire_date = models.DateField
