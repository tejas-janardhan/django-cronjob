from models import Job

DEFAULT_KWARGS = {

}


def job_factory(number_of_jobs):
    job_list = []

    for i in range(number_of_jobs):
        Job.objects.create(name=f'job_{i + 1}')
