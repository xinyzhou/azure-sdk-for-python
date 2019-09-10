# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AlertRuleTemplatePropertiesBase(Model):
    """Base alert rule template property bag.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param alert_rules_created_by_template_count: the number of alert rules
     that were created by this template
    :type alert_rules_created_by_template_count: int
    :ivar created_date_utc: The time that this alert rule template has been
     added.
    :vartype created_date_utc: datetime
    :param description: The description of the alert rule template.
    :type description: str
    :param display_name: The display name for alert rule template.
    :type display_name: str
    :param required_data_connectors: The required data connectors for this
     template
    :type required_data_connectors:
     list[~azure.mgmt.securityinsight.models.DataConnectorStatus]
    :param status: The alert rule template status. Possible values include:
     'Installed', 'Available', 'NotAvailable'
    :type status: str or ~azure.mgmt.securityinsight.models.TemplateStatus
    :param tactics: The tactics of the alert rule template
    :type tactics: list[str or
     ~azure.mgmt.securityinsight.models.AttackTactic]
    """

    _validation = {
        'created_date_utc': {'readonly': True},
    }

    _attribute_map = {
        'alert_rules_created_by_template_count': {'key': 'alertRulesCreatedByTemplateCount', 'type': 'int'},
        'created_date_utc': {'key': 'createdDateUTC', 'type': 'iso-8601'},
        'description': {'key': 'description', 'type': 'str'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'required_data_connectors': {'key': 'requiredDataConnectors', 'type': '[DataConnectorStatus]'},
        'status': {'key': 'status', 'type': 'str'},
        'tactics': {'key': 'tactics', 'type': '[str]'},
    }

    def __init__(self, *, alert_rules_created_by_template_count: int=None, description: str=None, display_name: str=None, required_data_connectors=None, status=None, tactics=None, **kwargs) -> None:
        super(AlertRuleTemplatePropertiesBase, self).__init__(**kwargs)
        self.alert_rules_created_by_template_count = alert_rules_created_by_template_count
        self.created_date_utc = None
        self.description = description
        self.display_name = display_name
        self.required_data_connectors = required_data_connectors
        self.status = status
        self.tactics = tactics
