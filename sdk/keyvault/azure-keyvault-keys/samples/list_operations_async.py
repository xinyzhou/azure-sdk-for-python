import asyncio
import os
from azure.keyvault.keys.aio import KeyClient
from azure.identity.aio import DefaultAzureCredential
from azure.core.exceptions import HttpResponseError

# ----------------------------------------------------------------------------------------------------------
# Prerequistes -
#
# 1. An Azure Key Vault-
#    https://docs.microsoft.com/en-us/azure/key-vault/quick-create-cli
#
# 2. Microsoft Azure Key Vault PyPI package -
#    https://pypi.python.org/pypi/azure-keyvault-keys/
#
# 3. Microsoft Azure Identity package -
#    https://pypi.python.org/pypi/azure-identity/
#
# 4. Set Environment variables AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET, VAULT_URL.
# How to do this - https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-keys#createget-credentials)
#
# ----------------------------------------------------------------------------------------------------------
# Sample - demonstrates the basic list operations on a vault(key) resource for Azure Key Vault. The vault has to be
# soft-delete enabled to perform one of the following operations. [Azure Key Vault soft delete]
# (https://docs.microsoft.com/en-us/azure/key-vault/key-vault-ovw-soft-delete)#
# 1. Create key (create_key)
#
# 2. List keys from the Key Vault (list_keys)
#
# 3. List key versions from the Key Vault (list_key_versions)
#
# 4. List deleted keys from the Key Vault (list_deleted_keys). The vault has to be soft-delete enabled to perform this
# operation.
#
# ----------------------------------------------------------------------------------------------------------
async def run_sample():
    # Instantiate a key client that will be used to call the service.
    # Notice that the client is using default Azure credentials.
    # To make default credentials work, ensure that environment variables 'AZURE_CLIENT_ID',
    # 'AZURE_CLIENT_SECRET' and 'AZURE_TENANT_ID' are set with the service principal credentials.
    VAULT_URL = os.environ["VAULT_URL"]
    credential = DefaultAzureCredential()
    client = KeyClient(vault_url=VAULT_URL, credential=credential)
    try:
        # Let's create keys with RSA and EC type. If the key
        # already exists in the Key Vault, then a new version of the key is created.
        print("\n1. Create Key")
        rsa_key = await client.create_rsa_key("rsaKeyName", hsm=False)
        ec_key = await client.create_ec_key("ecKey1Name", hsm=False)
        print("Key with name '{0}' was created of type '{1}'.".format(rsa_key.name, rsa_key.key_material.kty))
        print("Key with name '{0}' was created of type '{1}'.".format(ec_key.name, ec_key.key_material.kty))

        # You need to check the type of all the keys in the vault.
        # Let's list the keys and print their key types.
        # List operations don 't return the keys with their type information.
        # So, for each returned key we call get_key to get the key with its type information.
        print("\n2. List keys from the Key Vault")
        keys = client.list_keys()
        async for key in keys:
            retrieved_key = await client.get_key(key.name)
            print(
                "Key with name '{0}' with type '{1}' was found.".format(
                    retrieved_key.name, retrieved_key.key_material.kty
                )
            )

        # The rsa key size now should now be 3072, default - 2048. So you want to update the key in Key Vault to ensure
        # it reflects the new key size. Calling create_rsa_key on an existing key creates a new version of the key in
        # the Key Vault with the new key size.
        new_key = await client.create_rsa_key(rsa_key.name, hsm=False, size=3072)
        print("New version was created for Key with name '{0}' with the updated size.".format(new_key.name))

        # You should have more than one version of the rsa key at this time. Lets print all the versions of this key.
        print("\n3. List versions of the key using its name")
        key_versions = client.list_key_versions(rsa_key.name)
        async for key in key_versions:
            print("RSA Key with name '{0}' has version: '{1}'".format(key.name, key.version))

        # Both the rsa key and ec key are not needed anymore. Let's delete those keys.
        await client.delete_key(rsa_key.name)
        await client.delete_key(ec_key.name)

        # To ensure key is deleted on the server side.
        print("\nDeleting keys...")
        await asyncio.sleep(20)

        # You can list all the deleted and non-purged keys, assuming Key Vault is soft-delete enabled.
        print("\n3. List deleted keys from the Key Vault")
        deleted_keys = client.list_deleted_keys()
        async for deleted_key in deleted_keys:
            print("Key with name '{0}' has recovery id '{1}'".format(deleted_key.name, deleted_key.recovery_id))

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
