# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import asyncio
import os
from azure.keyvault.certificates.aio import CertificateClient
from azure.identity.aio import DefaultAzureCredential
from azure.core.exceptions import HttpResponseError

# ----------------------------------------------------------------------------------------------------------
# Prerequistes -
#
# 1. An Azure Key Vault-
#    https://docs.microsoft.com/en-us/azure/key-vault/quick-create-cli
#
# 2. Microsoft Azure Key Vault PyPI package -
#    https://pypi.python.org/pypi/azure-keyvault-certificates/
#
# 3. Microsoft Azure Identity package -
#    https://pypi.python.org/pypi/azure-identity/
#
# 4. Set Environment variables AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET, VAULT_URL.
# How to do this - https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-certificates#createget-credentials)
#
# ----------------------------------------------------------------------------------------------------------
# Sample - demonstrates the basic recover and purge operations on a vault(certificate) resource for Azure Key Vault
#
# 1. Create a certificate (create_certificate)
#
# 2. Delete a certificate (delete_certificate)
#
# 3. Recover a deleted certificate (recover_deleted_certificate)
#
# 4. Purge a deleted certificate (purge_deleted_certificate)
# ----------------------------------------------------------------------------------------------------------


async def run_sample():
    # Instantiate a certificate client that will be used to call the service.
    # Notice that the client is using default Azure credentials.
    # To make default credentials work, ensure that environment variables 'AZURE_CLIENT_ID',
    # 'AZURE_CLIENT_SECRET' and 'AZURE_TENANT_ID' are set with the service principal credentials.
    VAULT_URL = os.environ["VAULT_URL"]
    credential = DefaultAzureCredential()
    client = CertificateClient(vault_url=VAULT_URL, credential=credential)
    try:
        # Let's create certificates holding storage and bank accounts credentials. If the certificate
        # already exists in the Key Vault, then a new version of the certificate is created.
        print("\n1. Create Certificates")
        bank_cert_name = "BankRecoverCertificate"
        storage_cert_name = "ServerRecoverCertificate"

        bank_certificate_poller = await client.create_certificate(name=bank_cert_name)
        storage_certificate_poller = await client.create_certificate(name=storage_cert_name)

        await bank_certificate_poller
        await storage_certificate_poller
        print("Certificate with name '{0}' was created.".format(bank_cert_name))
        print("Certificate with name '{0}' was created.".format(storage_cert_name))

        # The storage account was closed, need to delete its credentials from the Key Vault.
        print("\n2. Delete a Certificate")
        deleted_bank_certificate = await client.delete_certificate(name=bank_cert_name)
        print("Certificate with name '{0}' was deleted on date {1}.".format(
            deleted_bank_certificate.name,
            deleted_bank_certificate.deleted_date)
        )

        # We accidentally deleted the bank account certificate. Let's recover it.
        # A deleted certificate can only be recovered if the Key Vault is soft-delete enabled.
        print("\n3. Recover Deleted Certificate")
        recovered_bank_certificate = await client.recover_deleted_certificate(deleted_bank_certificate.name)
        print("Recovered Certificate with name '{0}'.".format(recovered_bank_certificate.name))

        # Let's delete storage account now.
        # If the keyvault is soft-delete enabled, then for permanent deletion deleted certificate needs to be purged.
        await client.delete_certificate(name=storage_cert_name)

        # To ensure permanent deletion, we might need to purge the secret.
        print("\n4. Purge Deleted Certificate")
        await client.purge_deleted_certificate(name=storage_cert_name)
        print("Certificate has been permanently deleted.")

    except HttpResponseError as e:
        if "(NotSupported)" in e.message:
            print("\n{0} Please enable soft delete on Key Vault to perform this operation.".format(e.message))
        else:
            print("\nrun_sample has caught an error. {0}".format(e.message))

    finally:
        print("\nrun_sample done")


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_sample())
        loop.close()

    except Exception as e:
        print("Top level Error: {0}".format(str(e)))