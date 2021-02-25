"""
sentry_dingding_bot.models
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2021 by lpcoder, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

import time
import json
import requests
import logging
import six
import sentry

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from sentry import tagstore
from sentry.exceptions import PluginError
from sentry.plugins.bases import notify
from sentry.http import is_valid_url, safe_urlopen
from sentry.utils.safe import safe_execute

from sentry.utils.http import absolute_uri
from django.core.urlresolvers import reverse


# for dingtalk signature
import hmac
import hashlib
import base64
import urllib

def validate_urls(value, **kwargs):
    output = []
    for url in value.split('\n'):
        url = url.strip()
        if not url:
            continue
        if not url.startswith(('http://', 'https://')):
            raise PluginError('Not a valid URL.')
        if not is_valid_url(url):
            raise PluginError('Not a valid URL.')
        output.append(url)
    return '\n'.join(output)


class DingtalkForm(notify.NotificationConfigurationForm):
    urls = forms.CharField(
        label=_('Dingtalk robot url'),
        widget=forms.Textarea(attrs={
            'class': 'span6', 'placeholder': 'https://oapi.dingtalk.com/robot/send?access_token=9bacf9b193f'}),
        help_text=_('Enter dingtalk robot url.'))

    def clean_url(self):
        value = self.cleaned_data.get('url')
        return validate_urls(value)

 
class DingtalkPlugin(notify.NotificationPlugin):
    author = 'lpcoder'
    author_url = 'https://github.com/liupcoder/sentry-dingding-bot'
    version = 1.2.2
    description = "Integrates dingtalk robot."
    resource_links = [
        ('Bug Tracker', 'https://github.com/liupcoder/sentry-dingding-bot/issues'),
        ('Source', 'https://github.com/liupcoder/sentry-dingding-bot'),
    ]

    slug = 'dingtalk'
    title = 'dingtalk'
    conf_title = title
    conf_key = 'dingtalk'  

    project_conf_form = DingtalkForm
    timeout = getattr(settings, 'SENTRY_DINGTALK_TIMEOUT', 3) 
    logger = logging.getLogger('sentry.plugins.dingtalk')

    def is_configured(self, project, **kwargs):
        return bool(self.get_option('webhook', project))

    def get_config(self, project, **kwargs):
        return [
            {
                "name": "webhook",
                "label": "Webhook URL",
                "type": "url",
                "placeholder": "https://oapi.dingtalk.com/robot/send?access_token=**********",
                "required": True,
                "help": "Your custom dingding webhook URL.",
                "default": self.set_default(project, "webhook", "DINGTALK_WEBHOOK"),
            },
            {
                "name": "custom_keyword",
                "label": "Custom Keyword",
                "type": "string",
                "placeholder": "e.g. [Sentry] Error title",
                "required": False,
                "help": "Optional - A custom keyword as the prefix of the event title",
                "default": self.set_default(
                    project, "custom_keyword", "DINGTALK_CUSTOM_KEYWORD"
                ),
            },
            {
                "name": "signature",
                "label": "Additional Signature",
                "type": "string",
                "required": False,
                "help": "Optional - Attach Dingtalk webhook signature to the request headers.",
                "default": self.set_default(project, "signature", "DINGTALK_SIGNATURE"),
            },
            {
                "name": "include_tags",
                "label": "Include Tags",
                "type": "bool",
                "required": False,
                "help": "Include tags with notifications",
                "default": self.set_default(
                    project, "include_tags", "DINGTALK_INCLUDE_TAGS"
                ),
            },
            {
                "name": "included_tag_keys",
                "label": "Included Tags",
                "type": "string",
                "required": False,
                "help": (
                    "Only include these tags (comma separated list). "
                    "Leave empty to include all."
                ),
                "default": self.set_default(
                    project, "included_tag_keys", "DINGTALK_INCLUDE_TAG_KEYS"
                ),
            },
            {
                "name": "include_rules",
                "label": "Include Rules",
                "type": "bool",
                "required": False,
                "help": "Include triggering rules with notifications.",
                "default": self.set_default(
                    project, "include_rules", "DINGTALK_INCLUDE_RULES"
                ),
            },
        ]

    def set_default(self, project, option, env_var):
        if self.get_option(option, project) != None:
            return self.get_option(option, project)
        if hasattr(settings, env_var):
            return six.text_type(getattr(settings, env_var))
        return None

    def _get_tags(self, event):
        tag_list = event.tags
        if not tag_list:
            return ()

        return (
            (tagstore.get_tag_key_label(k), tagstore.get_tag_value_label(k, v))
            for k, v in tag_list
        )

    def get_tag_list(self, keys):
        if not keys:
            return None
        return set(tag.strip().lower() for tag in keys.split(","))

    def send_webhook(self, url, payload):
        return safe_urlopen(
            url=url,
            json=payload,
            timeout=self.timeout,
            verify_ssl=False,
        )

    def notify_users(self, group, event, *args, **kwargs): 
        event = notification.event
        group = event.group
        project = group.project

        if not self.is_configured(project):
            return
        if group.is_ignored():
            return
        
        custom_keyword = self.get_option("custom_keyword", project)
        signature = self.get_option("signature", project)
        include_tags = self.get_option("include_tags", project)
        included_tag_keys = self.get_option("included_tag_keys", project)
        include_rules = self.get_option("include_rules", project)

        webhookUrl = self.get_option("webhook", project)

        if signature:
            timestamp = str(round(time.time() * 1000))
            secret = signature
            secret_enc = secret.encode("utf-8")
            string_to_sign = "{}\n{}".format(timestamp, secret)
            string_to_sign_enc = string_to_sign.encode("utf-8")
            hmac_code = hmac.new(
                secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
            ).digest()
            sign = urllib.parse.quote(base64.b64encode(hmac_code))
            webhookUrl = u"{}&timestamp={}&sign={}".format(webhookUrl, timestamp, sign)

        # 报警规则
        ruleStr = ""
        if include_rules:
            if notification.rules:
                rule = notification.rules[0]
                rule_link = "/%s/%s/settings/alerts/rules/%s/" % (
                    group.organization.slug,
                    project.slug,
                    rule.id,
                )
                rule_link = absolute_uri(rule_link)
                ruleStr = (
                    u"\n> Triggered by Rule [{}]({})".format(rule.label, rule_link)
                ).encode("utf-8")

        # 标签
        tagStr = ""
        if include_tags:
            included_tags = set(self.get_tag_list(included_tag_keys) or [])
            for tag_key, tag_value in self._get_tags(event):
                key = tag_key.lower()
                std_key = tagstore.get_standardized_key(key)
                if (
                    included_tags
                    and key not in included_tags
                    and std_key not in included_tags
                ):
                    continue
                tagStr = tagStr + "\n- {}: {} ".format(tag_key, tag_value)

        payload = title

        if ruleStr:
            payload = payload + ruleStr
        if tagStr:
            payload = payload + tagStr

        # title
        title = "{}\n#### From project: {}\n".format(event.title, project.slug)
        if custom_keyword:
            title = u"[{}] {}".format(custom_keyword, title)
        title = "### " + title

        # link = self.get_group_url(group)
        # message_format = '[%s] %s   %s'
        # message = message_format % (event.title, event.message, link)
        # data = {"msgtype": "text",
        #             "text": {
        #                 "content": message
        #             }
        #         }
        data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": payload
                    },
                "at": {
                    "atMobiles": [],
                    "isAtAll": false
                    }
                }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        requests.post(webhookUrl, data=json.dumps(data), headers=headers)