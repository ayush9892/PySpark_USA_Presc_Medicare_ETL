# Databricks notebook source
def mount_adls(storage_account, container_name):
    # Get id and key
    client_id = dbutils.secrets.get(scope='formula1-scope', key='formula1-databricks-client-id')
    tenant_id = dbutils.secrets.get(scope='formula1-scope', key='formula1-databricks-tenant-id')
    client_secret = dbutils.secrets.get(scope='formula1-scope', key='formula1-databricks-client-secret')

    # Set Spark configs
    configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": client_id,
          "fs.azure.account.oauth2.client.secret": client_secret,
          "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
        }

    # Unmount the mount if its already available
    if any(mount.mountPoint == f'/mnt/{storage_account}/{container_name}' for mount in dbutils.fs.mounts()):
        dbutils.fs.unmount(f'/mnt/{storage_account}/{container_name}')

    # Mount container
    dbutils.fs.mount(
        source = f'abfss://{container_name}@{storage_account}.dfs.core.windows.net/',
        mount_point = f'/mnt/{storage_account}/{container_name}',
        extra_configs = configs
    )

# COMMAND ----------

mount_adls('synapselearningadls', 'raw')

# COMMAND ----------

mount_adls('synapselearningadls', 'processed')

# COMMAND ----------

mount_adls('synapselearningadls', 'presentation')
