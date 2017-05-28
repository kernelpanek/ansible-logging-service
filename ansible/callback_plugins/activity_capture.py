from __future__ import (absolute_import, division, print_function)
from collections import defaultdict
import json
import os
import requests
import re
import socket
import time
import urlparse
from ansible import constants as C
from ansible.plugins.callback import CallbackBase
from ansible.executor.task_result import TaskResult
from ansible.executor.stats import AggregateStats
from ansible.playbook import Play, Playbook

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()

__metaclass__ = type


def get_hostip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    result = s.getsockname()[0]
    s.close()
    return result

THIS_HOSTS_IP_ADDRESS = get_hostip()
THIS_HOSTS_NAME = socket.gethostname()
LOG_SERVER_URL = os.environ.get("LOG_SERVER_URL")
LOG_SERVER_TOKEN = os.environ.get("LOG_SERVER_TOKEN")


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "notification"
    CALLBACK_NAME = "activity_capture"
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self, display=None):
        super(CallbackModule, self).__init__(display)
        self.results = defaultdict(dict)
        self.hosts_worked = set([])
        self.ignored_keys = ["_ansible_parsed", "_ansible_no_log", "invocation"]
        self.property_file = os.environ.get("ANSIBLE_BUILD_FILE", None)
        self._playbook = None

    def _ship_logfile(self, object):
        file_name = "ansible_build_file_{}.json".format(time.time())
        url = urlparse.urljoin(LOG_SERVER_URL, "upload", file_name)
        payload = json.dumps(object, sort_keys=True)
        display.v("shipping payload: {}".format(payload))
        result = None
        try:
            result = requests.put(url,
                                   headers={"Content-type": "*/*",
                                            "Content-Disposition": "attachment; filename={}".format(file_name),
                                            "Authorization": "Token {}".format(LOG_SERVER_TOKEN)},
                                   data=payload)
            display.v("**********************************************************")
            display.v("result: {} - {}".format(result.status_code, result.content))
            display.v("**********************************************************")
        except Exception as ex:
            display.display(ex)
        return result

    def _ship_event(self, name, event):
        url = urlparse.urljoin(LOG_SERVER_URL, "api/events/")
        hostip = socket.gethostbyname(event.get("host", THIS_HOSTS_IP_ADDRESS))
        hostname = event.get("task_data", {}).get("ansible_facts", {}).get("ansible_hostname", THIS_HOSTS_NAME)
        payload = json.dumps(dict(
            name=name,
            data=event,
            hostip=hostip,
            hostname=hostname
        ), sort_keys=True)
        display.v("shipping payload: {}".format(payload))
        result = None

        try:
            result = requests.post(url,
                                   headers={"Content-type": "application/json",
                                            "Authorization": "Token {}".format(LOG_SERVER_TOKEN)},
                                   data=payload)
            display.v("**********************************************************")
            display.v("result: {} - {}".format(result.status_code, result.content))
            display.v("**********************************************************")
        except Exception as ex:
            display.display(ex.message)
        return result

    def _ship_play(self, name, play):
        url = urlparse.urljoin(LOG_SERVER_URL, "api/plays/")
        hostip = THIS_HOSTS_IP_ADDRESS
        hostname = THIS_HOSTS_NAME
        payload = json.dumps(dict(
            name=name,
            data=play,
            hostip=hostip,
            hostname=hostname
        ), sort_keys=True)
        display.v("shipping payload: {}".format(payload))
        result = None

        try:
            result = requests.post(url,
                                   headers={"Content-type": "application/json",
                                            "Authorization": "Token {}".format(LOG_SERVER_TOKEN)},
                                   data=payload)
            display.v("**********************************************************")
            display.v("result: {} - {}".format(result.status_code, result.content))
            display.v("**********************************************************")
        except:
            pass
        return result

    def _ship_task(self, name, task):
        url = urlparse.urljoin(LOG_SERVER_URL, "api/tasks/")
        hostip = socket.gethostbyname(task.get("host", THIS_HOSTS_IP_ADDRESS))
        hostname = task.get("task_data", {}).get("ansible_facts", {}).get("ansible_hostname", THIS_HOSTS_NAME)
        payload = json.dumps(dict(
            name=name,
            data=task,
            hostip=hostip,
            hostname=hostname
        ), sort_keys=True)
        display.v("shipping payload: {}".format(payload))
        result = None

        try:
            result = requests.post(url,
                                   headers={"Content-type": "application/json",
                                            "Authorization": "Token {}".format(LOG_SERVER_TOKEN)},
                                   data=payload)
            display.v("**********************************************************")
            display.v("result: {} - {}".format(result.status_code, result.content))
            display.v("**********************************************************")
        except:
            pass
        return result

    def _capture_taskresult(self, result):
        data = result._result.copy()
        task_fields = result._task_fields.copy()
        task_result = dict(task_name=result.task_name,
                           host=result._host.get_name(), )
        [task_result.update({k: data.pop(k, None)}) for k, v in data.items() if type(v) is dict]
        task_result.update(dict(task_data=data))
        task_result.update(dict(task_fields=task_fields))

        result = self._ship_task(task_result.get("task_name"), task_result)
        return result

    def _capture_play(self, play):
        play_dict = dict(name=play.get_name(),
                         vars=play.get_vars(),
                         roles=[r.get_name() for r in play.get_roles()],
                         tasks=[t.get_name() for tg in play.get_tasks() for t in tg],
                         var_mgr=play._variable_manager.extra_vars,
                         playbook=self._playbook)
        result = self._ship_play(play_dict.get("name"), play_dict)
        return result

    def _capture_playbook(self, playbook):
        playbook_dict = dict(basedir=playbook._basedir,
                             file_name=playbook._file_name)
        self._playbook = playbook_dict

    def _capture_stats(self, stats):
        stats_dict = {host: stats.summarize(host) for host in self.hosts_worked}
        stats_dict.update(dict(playbook=self._playbook))
        result = self._ship_event("stats", stats_dict)
        return result

    def _capture_activity(self, *args, **kwargs):
        if "result" in kwargs.keys() and type(kwargs.get("result")) is TaskResult:
            self._capture_taskresult(kwargs.get("result"))

        if "play" in kwargs.keys() and (type(kwargs.get("play")) is Play):
            self._capture_play(kwargs.get("play"))

        if "playbook" in kwargs.keys() and (type(kwargs.get("playbook")) is Playbook):
            self._capture_playbook(kwargs.get("playbook"))

        if "stats" in kwargs.keys() and (type(kwargs.get("stats")) is AggregateStats):
            self._capture_stats(kwargs.get("stats"))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self._capture_activity(evt="v2_runner_on_failed", result=result)

    def v2_runner_on_ok(self, result):
        task_key = re.sub(r"[^a-zA-Z0-9_]", "", result._task.get_name().replace(" ", "_"))
        self.hosts_worked.add(result._host.name)
        self.results[result._host.name].update(
            {task_key: {k: v
                        for k, v in result._result.items()
                        if k not in self.ignored_keys}}
        )
        self._capture_activity(evt="v2_runner_on_ok", result=result)

    def v2_runner_on_skipped(self, result):
        if C.DISPLAY_SKIPPED_HOSTS:
            self._capture_activity(evt="v2_runner_on_skipped", result=result)

    def v2_runner_on_unreachable(self, result):
        self._capture_activity(evt="v2_runner_on_unreachable", result=result)

    def v2_runner_on_async_poll(self, result):
        self._capture_activity(evt="v2_runner_on_async_poll", result=result)

    def v2_runner_on_async_ok(self, result):
        self._capture_activity(evt="v2_runner_on_async_ok", result=result)

    def v2_runner_on_async_failed(self, result):
        self._capture_activity(evt="v2_runner_on_async_failed", result=result)

    def v2_playbook_on_start(self, playbook):
        self._capture_activity(evt="v2_playbook_on_start", playbook=playbook)

    def v2_playbook_on_play_start(self, play):
        self._capture_activity(evt="v2_playbook_on_play_start", play=play)

    def v2_playbook_on_stats(self, stats):
        self.results["stats"] = {host: stats.summarize(host) for host in self.hosts_worked}
        self._ship_logfile(dict(self.results))
        self._capture_activity(evt="v2_playbook_on_stats", stats=stats)

    def v2_runner_item_on_ok(self, result):
        self._capture_activity(evt="v2_runner_item_on_ok", result=result)

    def v2_runner_item_on_failed(self, result):
        self._capture_activity(evt="v2_runner_item_on_failed", result=result)

    def v2_runner_item_on_skipped(self, result):
        self._capture_activity(evt="v2_runner_item_on_skipped", result=result)

    def v2_runner_retry(self, result):
        self._capture_activity(evt="v2_runner_retry", result=result)
