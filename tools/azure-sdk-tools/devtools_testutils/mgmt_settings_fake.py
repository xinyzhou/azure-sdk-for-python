﻿#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

from azure.common.credentials import (
    BasicTokenAuthentication,
    UserPassCredentials
)

SUBSCRIPTION_ID = "00000000-0000-0000-0000-000000000000"

# this is used explicitly for ADLA job id replacement in recordings.
ADLA_JOB_ID = "00000000-0000-0000-0000-000000000000"
# GraphRBAC tests
AD_DOMAIN = "myaddomain.onmicrosoft.com"
# Keyvault tests
TENANT_ID = '00000000-0000-0000-0000-000000000000'
CLIENT_OID = '00000000-0000-0000-0000-000000000000'
# Cognitive Services tests
CS_SUBSCRIPTION_KEY = '0000000000000000000000000000'
# Event Grid key
EVENT_GRID_KEY = '0000000000000000000000000000'
# HDInsight tests
HDI_ADLS_ACCOUNT_NAME = 'fakehdiadlsaccount'
HDI_ADLS_CLIENT_ID = '00000000-0000-0000-0000-000000000000'

# Ubuntu image
LINUX_OS_VHD = "https://mystorageaccount.blob.core.windows.net/inputtestdatadonotdelete/ubuntu.vhd"

# Storage tests related
ACTIVE_DIRECTORY_APPLICATION_ID  = '00000000-0000-0000-0000-00000000000'
ACTIVE_DIRECTORY_APPLICATION_SECRET = '000000000ft5g5g5g5g5g5g5g5000000?'
ACTIVE_DIRECTORY_TENANT_ID = '00000000-0000-0000-0000-000000000000'
IS_SERVER_SIDE_FILE_ENCRYPTION_ENABLED = True

# Read for details of this file:
# https://github.com/Azure/azure-sdk-for-python/wiki/Contributing-to-the-tests

def get_credentials(**kwargs):
    # Put your credentials here in the "real" file
    #return UserPassCredentials(
    #    'user@myaddomain.onmicrosoft.com',
    #    'Password'
    #)
    # note that UserCredential does not work any longer. Must use a ServicePrincipal. 
    # for deprecated APIs I believe will still work.
    # return ServicePrincipalCredentials(
    #     client_id = '<AAD App client id>',
    #     secret = '<secret for the aad app>',
    #     tenant = '<microsoft aad tenant id>'
    # )
    # Needed to play recorded tests
    return BasicTokenAuthentication(
        token = {
            'access_token':'faked_token'
        }
    )