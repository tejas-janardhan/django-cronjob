=====
CronJob
=====

CronJob is a Django app to used to create quick endpoints that can run jobs periodically called from the crontab.
Lets you group jobs together and autogenerates the cron line needed to execute the jobs. Multiple job groups run asynchronously.

Installation
------------
Notes on using the .tar.gz file to install via pip.
Additional installation notes...

Quick start
-----------

1. Add "cronjob" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'cronjob',
    ]

2. Include the cronjob URLconf in your project urls.py like this::

    path('cronjob/', include('cronjob.urls')),

3. Run ``python manage.py migrate`` to create the cronjob models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a jobs and job group (you'll need the Admin app enabled).

5. Test out the endpoint via the cmd prompt and check Job Histories to check if the jobs ran successfully.
