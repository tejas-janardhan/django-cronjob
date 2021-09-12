from django.http import Http404, JsonResponse
from django.views.generic import View

from cronjob.models import JobGroup, JobHistory


class JobEndpoint(View):
    """
    Creates a job endpoint based on the endpoint configuration.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_job_group(self, kwargs):
        try:
            job_group = JobGroup.objects.get(name=kwargs['job_group'])
        except JobGroup.DoesNotExist:
            raise Http404

        return job_group

    def _run_job(self, job):
        job_history = JobHistory.objects.create(job=job,
                                                time_interval=self.job_group.time_interval,
                                                job_group=self.job_group)
        try:
            job.get_job_function()(*job.args, **job.kwargs)
        except Exception as e:
            job_history.set_failure(str(e))
        else:
            job_history.set_success()

    def post(self, request, **kwargs):
        self.job_group = self._get_job_group(kwargs)
        if str(self.job_group.token) != kwargs['token']:
            return JsonResponse({'errors': ['invalid token']})

        job_list = self.job_group.jobs.all()

        for job in job_list:
            self._run_job(job)

        return JsonResponse({'errors': []})
