import logging
from collections import defaultdict
from time import perf_counter

from BelHardCRM.settings import MEDIA_URL
from client.models import (Sex, Citizenship, FamilyState, Children, City, State, Telephone, Skills, Education,
                           Certificate, CV, Experience, Employment, TimeJob, TypeSalary, UserModel, Sphere)


# TeamRome
def edit_page_get(client):
    """ views.py ClientEditMain(TemplateView) GET method.
    Загрузка из БД списков для выбора данных клиента. """
    try:
        print("edit_page_get()")
        time_0 = perf_counter()
        response = defaultdict()
        # default select fields
        response['sex'] = Sex.objects.all()
        response['citizenship'] = Citizenship.objects.all()
        response['family_state'] = reversed(FamilyState.objects.all())
        response['children'] = reversed(Children.objects.all())
        response['country'] = response['citizenship']
        response['city'] = reversed(City.objects.all())
        response['state'] = reversed(State.objects.all())
        #
        if client:
            user_model = UserModel.objects.get(id=client.user_client_id)
            response['user_model'] = {
                "first_name": user_model.first_name,
                "last_name": user_model.last_name,
                "email": user_model.email,
            }
            phone_arr = [i['telephone_number'] for i in Telephone.objects.filter(client_phone=client).values()]
            response['cl_phone'] = phone_arr
            response['client'] = client

        print('\tedit_page_get() - OK; Time: %s' % (perf_counter() - time_0))
        return response
    except Exception as ex:
        logging.error("Exception in - edit_page_get()\n %s" % ex)
        return None


# TeamRome
def skills_page_get(client):
    """" views.py ClientEditSkills(TemplateView) GET method.  """
    try:
        print("skills_page_get()")
        time_0 = perf_counter()
        response = defaultdict()

        if client:
            skills_arr = [i['skill'] for i in Skills.objects.filter(client_skills=client).values()]
            response['cl_skill'] = skills_arr

        print('\tskills_page_get() - OK; Time: %s' % (perf_counter() - time_0))
        return response
    except Exception as ex:
        logging.error("Exception in skills_page_get()\n%s" % ex)
        return None


# TeamRome
def education_page_get(client):
    """" views.py ClientEditEducation(TemplateView) GET method.  """
    try:
        print("education_page_get()")
        time_0 = perf_counter()
        response = defaultdict()
        if client:
            edus = [i for i in Education.objects.filter(client_edu=client).values()]
            response['cl_edu'] = edus
            edu_id = [e['id'] for e in response['cl_edu']]
            certs = [[c for c in Certificate.objects.filter(education_id=i).values()] for i in edu_id]
            # print("\tcerts: %s" % certs)
            for e in edus:
                # print("\te: %s" % e)
                for c in certs:
                    # print("\tc: %s" % c)
                    if c:
                        if c[0]['education_id'] == e['id']:
                            e['img'] = "%s%s" % (MEDIA_URL, c[0]['img'])
                            e['link'] = c[0]['link']
                            e['show_img'] = "%s%s" % (MEDIA_URL, c[0]['img'])
            # print("\tcl_edu: %s" % response['cl_edu'])
        print('\teducation_page_get() - OK; Time: %s' % (perf_counter() - time_0))
        return response
    except Exception as ex:
        logging.error("Exception in education_page_get()\n%s" % ex)
        return None


# TeamRome
def cv_page_get(client):
    """" views.py ClientEditCv(TemplateView) GET method. """
    try:
        print("cv_page_get()")
        time_0 = perf_counter()
        response = defaultdict()
        # default select fields
        response['employment'] = Employment.objects.all()
        response['time_job'] = TimeJob.objects.all()
        response['type_salary'] = TypeSalary.objects.all()

        if client:
            cvs = CV.objects.filter(client_cv=client)
            cvs_val = [i for i in cvs.values()]
            response['cl_cvs'] = cvs_val

            for c in cvs_val:
                # add more keys to response['cl_cvs'] dictionary
                c['cl_employment'] = Employment.objects.get(id=c['employment_id']).employment
                c['cl_time_job'] = TimeJob.objects.get(id=c['time_job_id']).time_job_word
                c['cl_type_salary'] = TypeSalary.objects.get(id=c['type_salary_id']).type_word

            print("\tcv_page_get() - OK; Time: %s" % (perf_counter() - time_0))
        return response
    except Exception as ex:
        logging.error("Exception in cv_page_get()\n%s" % ex)
        return None


# TeamRome
def experience_page_get(client):
    """" views.py ClientEditExperience(TemplateView) GET method. """
    try:
        print("experience_page_get()")
        time_0 = perf_counter()
        response = defaultdict()
        response['sphere'] = Sphere.objects.all()
        if client:
            exp = Experience.objects.filter(client_exp=client)
            exp_dict = [i for i in exp.values()]
            response['cl_exp'] = exp_dict

            for i, e in enumerate(exp):
                sphere = [i['sphere_word'] for i in e.sphere.values()]
                exp_dict[i]['sphere'] = sphere

            print("\texperience_page_get() - OK; Time: %s" % (perf_counter() - time_0))
        return response
    except Exception as ex:
        logging.error("Exception in experience_page_get()\n%s" % ex)
        return None
