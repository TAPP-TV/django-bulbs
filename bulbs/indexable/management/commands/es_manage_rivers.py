import json
import logging

import requests
from django.core.management.base import BaseCommand
from elasticutils.contrib.django import get_es
from pyelasticsearch.exceptions import ElasticHttpNotFoundError

from bulbs.indexable.conf import settings as indexable_conf


logger = logging.getLogger()


class Command(BaseCommand):
    help = "Manage ElasticSearch rivers from settings."
    url_template = u"{es_url}/_river/{river_name}/{action}"

    def handle(self, *args, **options):
        rivers_conf = getattr(indexable_conf, "ES_RIVERS", {})
        es = get_es()
        # get existing rivers
        existing_rivers = set()
        try:
            qs = es.search({}, index=["_river"])
        except ElasticHttpNotFoundError:
            pass  # no currently existing rivers. that's ok.
        else:
            for row in qs["hits"]["hits"]:
                existing_rivers.add(row["_type"])        
        # add rivers from settings
        for river_name, river_conf in rivers_conf.items():
            logger.debug("Adding river {}".format(river_name))
            es_url, _ = es.servers.get()
            this_url = self.url_template.format(
                es_url=es_url,
                river_name=river_name,
                action="_meta"
            )
            r = requests.put(this_url, data=json.dumps(river_conf))
            if r.status_code not in (200, 201):
                raise Exception(
                    u"Unable to add river named {}: {}".format(
                        river_name, r.content
                    )
                )
            try:
                existing_rivers.remove(river_name)
            except KeyError:
                pass
        # remove remaining rivers
        for river_name in existing_rivers:
            logger.debug("Removing river {}".format(river_name))
            es_url, _ = es.servers.get()
            this_url = self.url_template.format(
                es_url=es_url,
                river_name=river_name,
                action=""
            )
            r = requests.delete(this_url)
            if r.status_code != 200:
                raise Exception(
                    u"Unable to remove river named {}: {}".format(
                        river_name, r.content
                    )
                )
