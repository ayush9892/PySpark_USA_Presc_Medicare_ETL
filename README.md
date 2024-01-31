# PySpark_USA_Presc_Medicare_ETL

### Concept of the Project 💡
- This project involves the acquisition of USA Presc Medicare Datasets that contains almost 13_lakh records. These datasets are located on Local SFTP Server. The primary objective is to load these datasets from Local SFTP Server to the raw container in ADLS using Azure pipelines and then perform the transformation using Databricks.
  
### Source Data: 📤
- [Download these Datasets](https://drive.google.com/drive/folders/1guqreVonFIrwSD9xtnx2yyssqfAcIMrt?usp=sharing)

### Destination: 📥📍
- Azure Data Lake Gen2 Storage

## Tools ⚙

### Data Integration/Ingestion
- ADF Pipelines

### Transformation
- Databricks


## Approach

### Environment Setup
- Azure Subscription
- Azure Key Vaults
- Data Factory
- Data Lake Storage Gen2
- Azure Databricks Cluster
- Local SFTP Server


### Local SFTP Server Setup
1. Setup SFTP server in newer versions of windows
    - Click windows button and search for “manage optional features”
    - Click on “add a feature” and search for OpenSSH server and install it
    - Now open "services" and start "OpenSSH server" and "OpenSSH Authentication agent":
      ![image](https://github.com/ayush9892/PySpark_USA_Presc_Medicare_ETL/assets/85745368/e3c08c4a-e8cf-4b66-abf0-9d40b1bb9315)
    - Create the appropriate firewall policy to expose the SFTP port 22 to local or remote systems if required

2. Using public key based authentication in SFTP
    - Generate key using PuTTy Key Generator: 
	    - It will create 2 keys: Private(.ppk), Public
    - Copy the public key to ‪C:\Users\<username>\.ssh\authorized_keys . If the file is not present, create a new file at this location.

3. Edit the *sshd_config* file of the SFTP server to configure public key based authentication
   - sshd_config file is located at C:\ProgramData\ssh folder of the SFTP server
   - Open it with a text editor like Notepad or VS code
   - Modify the sshd_config file to make sure the following lines are present in the file:
     - `PubkeyAuthentication yes`
     - `AuthorizedKeysFile .ssh/authorized_keys`
     - `Subsystem sftp internal-sftp`
     - `ChrootDirectory "C:\<folder_name>"` 


### DATA EXTRACTION/ INGESTION
Two different datasets were ingested from Local SFTP Server into Datalake Gen2. They are - 

- USA Presc Medicare Data (SFTP Server)
- US Cities Dimension Data (SFTP Server)


### Pipeline Steps:
1. Create a Linked Service To SFTP
- In Authentication type select SSH public key authentication
  - In this you can directly upload private key. For this, first you have to convert this private ppk file to OpenSSH format because, ADF SFTP connector supports an RSA/DSA OpenSSH key. For conversion use, PuTTy:
    - In PuTTy, click ‘Load’ and select your PPK file.
    - Then, go to ‘Conversions’ in the menu and select ‘Export OpenSSH key’.
    - Then upload that OpenSSH key to linked service.    
  - Or, you can store the private-key to Azure Key Vault Secrets. For this, first you have to encode OpenSSH key in Base-64 encoded. And then add this encoded key to secrets. 
2. Create a Linked Service to Azure Key Vaults
3. Create a Linked Service To Azure Data Lake storage (GEN2)
4. Create a SFTP dataset, pointing to the source folder location.
5. Create a ADLS Gen2 dataset, pointing to the sink location.
6. Create a Pipeline, and use Copy Activity.


# Used Technologies
- Azure DataFactory
- Azure Databricks (Pyspark)
- Azure Storage Account
- Azure Data Lake Gen2
- Azure Key Vaults
- PuTTY Key Generator
