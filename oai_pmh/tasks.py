from __future__ import absolute_import
from logging import getLogger
from mgi.models import OaiRegistry
from mgi.settings import OAI_HOST_URI, OAI_USER, OAI_PASS
import requests
from mgi.celery import app


logger = getLogger(__name__)


def init_harvest():
    #Purge all current tasks in the harvest queue
    t = 't'
    harvest_task()

def harvest_task():
    registries = OaiRegistry.objects.all()
    #We launch the backround task for each registry
    for registry in registries:
        harvest.apply_async((str(registry.id),), countdown=10)

    # stop_harvest_tasks()
    # logger.debug('demo_task. message={0}'.format(message))

@app.task
def harvest(registryId):
    try:
        #Get the registry
        registry = OaiRegistry.objects.get(pk=registryId)
        #If we need to harvest
        if registry.harvest:
            #Get the uri
            uri = OAI_HOST_URI + "/oai_pmh/api/update/all/records"
            # Call the API to update all records for this registry
            req = requests.post(uri,
                               {"registry_id": registryId},
                               auth=(OAI_USER, OAI_PASS))
            #New update in harvestrate seconds
            t = harvest.apply_async((registryId,), countdown=registry.harvestrate)

        return registry.name + "updated"
    except Exception as e:
        return False
        # return HttpResponseBadRequest('An error occurred. Please contact your administrator.')

@app.task
def stop_harvest_tasks():
    app.control.r