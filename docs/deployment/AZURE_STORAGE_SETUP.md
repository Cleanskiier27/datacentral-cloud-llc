# Azure Storage Configuration for NetworkBuster

## 🗄️ Azure Storage Infrastructure

**Date:** December 14, 2025
**Status:** Ready for Deployment

---

## 📋 Storage Components

### **1. Storage Account (Primary)**
- **Type:** Azure Storage Account (StorageV2)
- **SKU:** Standard_LRS (Locally Redundant Storage)
- **Tier:** Hot (frequently accessed data)
- **Security:** 
  - HTTPS enforced
  - TLS 1.2 minimum
  - Blob public access disabled
  - Soft delete enabled (7 days)

### **2. Blob Containers (7)**

| Container | Purpose | Access | Retention |
|-----------|---------|--------|-----------|
| **realtime-data** | Live visitor metrics, real-time analytics | Private | 30 days |
| **ai-training-datasets** | ML training data, datasets | Private | 365 days |
| **ml-models** | Trained models, checkpoints | Private | 365 days |
| **immersive-reader-content** | Formatted content for immersive reader | Private | 90 days |
| **analytics-data** | Processed analytics, reports | Private | 180 days |
| **blog-assets** | Blog media, images, videos | Private | Permanent |
| **backups** | Backup archives, snapshots | Private | 365 days |

### **3. File Shares (1)**

| Share | Size | Purpose |
|-------|------|---------|
| **cache** | 100 GB | Cache storage for immersive reader |

### **4. Tables (2)**

| Table | Purpose |
|-------|---------|
| **VisitorMetrics** | Visitor tracking, IP data, behavior |
| **PerformanceMetrics** | Page load times, response latency, uptime |

### **5. Queues (2)**

| Queue | Purpose |
|-------|---------|
| **ai-training-jobs** | Async AI model training tasks |
| **data-processing** | Background data processing jobs |

---

## 🚀 Deployment Instructions

### **Prerequisites**
- Azure CLI installed
- Azure subscription access
- Git repository access
- Administrator permissions

### **Option 1: PowerShell (Windows)**
```powershell
cd networkbuster.net
.\deploy-storage-azure.ps1 `
  -SubscriptionId "<your-subscription-id>" `
  -ResourceGroup "networkbuster-rg" `
  -Location "eastus" `
  -ProjectName "networkbuster"
```

### **Option 2: Bash (Linux/Mac)**
```bash
cd networkbuster.net
bash deploy-storage-azure.sh
```

### **Option 3: Azure Portal**
1. Navigate to Azure Portal: https://portal.azure.com
2. Create new Storage Account
3. Name: `networkbuster[random]sa`
4. Region: `eastus`
5. Performance: Standard
6. Redundancy: LRS (Locally Redundant)
7. Create containers manually or use Bicep template

---

## 🔐 Access Credentials

After deployment, credentials will be saved to `storage-credentials.env`:

```env
AZURE_STORAGE_ACCOUNT_NAME=networkbuster[random]sa
AZURE_STORAGE_ACCOUNT_KEY=[base64-encoded-key]
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...
AZURE_STORAGE_RESOURCE_GROUP=networkbuster-rg

# Container names
AZURE_STORAGE_CONTAINER_REALTIME=realtime-data
AZURE_STORAGE_CONTAINER_AI=ai-training-datasets
AZURE_STORAGE_CONTAINER_MODELS=ml-models
AZURE_STORAGE_CONTAINER_READER=immersive-reader-content
AZURE_STORAGE_CONTAINER_ANALYTICS=analytics-data
AZURE_STORAGE_CONTAINER_BLOG=blog-assets
AZURE_STORAGE_CONTAINER_BACKUPS=backups
```

⚠️ **SECURITY:** Never commit this file to git. Add to `.gitignore`.

---

## 🔑 GitHub Secrets Configuration

After deployment, add to GitHub Secrets:

```bash
gh secret set AZURE_STORAGE_ACCOUNT_NAME -b "networkbuster[random]sa"
gh secret set AZURE_STORAGE_ACCOUNT_KEY -b "[key]"
gh secret set AZURE_STORAGE_CONNECTION_STRING -b "[connection-string]"
```

Or via GitHub UI:
1. Go to Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add above three secrets

---

## 💻 Usage Examples

### **Upload Real-Time Data**
```python
from azure.storage.blob import BlobClient

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob = BlobClient.from_connection_string(
    connection_string,
    container_name="realtime-data",
    blob_name="visitor-metrics-2025-12-14.json"
)

with open("visitor-data.json", "rb") as data:
    blob.upload_blob(data, overwrite=True)
```

### **Upload AI Training Dataset**
```python
from azure.storage.blob import ContainerClient

container = ContainerClient.from_connection_string(
    connection_string,
    container_name="ai-training-datasets"
)

# Upload dataset file
with open("training-data.csv", "rb") as data:
    container.upload_blob(
        name="dataset-2025-12-14.csv",
        data=data,
        overwrite=True
    )
```

### **Store ML Model**
```python
import pickle

# Serialize model
model_bytes = pickle.dumps(trained_model)

# Upload to storage
blob_client = container.get_blob_client("models/classifier-v1.pkl")
blob_client.upload_blob(model_bytes, overwrite=True)
```

### **Access Data in Immersive Reader**
```javascript
// Fetch formatted content from Azure
const response = await fetch(
  `https://[account].blob.core.windows.net/immersive-reader-content/article.json?sv=2021-06-08&...`
);
const content = await response.json();

// Render in immersive reader
immersiveReaderToolbar.launchAsync(content);
```

---

## 📊 Pricing Estimate

| Service | Amount | Unit Price | Monthly Cost |
|---------|--------|-----------|--------------|
| Storage Account | 1 | $0.06 | $0.06 |
| Blob Storage | 100 GB | $0.0184/GB | $1.84 |
| File Shares | 100 GB | $0.0194/GB | $1.94 |
| Table Storage | 10 GB | $0.03/GB | $0.30 |
| Queue Storage | 1 GB | $0.05/GB | $0.05 |
| **Total Estimated** | | | **~$4-6/month** |

---

## 🔄 Integration Points

### **Real-Time Overlay**
```
Azure Log Analytics → Processing → Storage (realtime-data) → Immersive Reader → Visualization
```

### **AI Training Pipeline**
```
Upload Dataset → Training Queue → AI Training Job → ML Models Container → Inference
```

### **Blog & Content**
```
Blog CMS → Storage (blog-assets) → CDN → Delivery
```

### **Analytics**
```
Visitor Tracking → Log Analytics → Processing → Analytics Tables → Dashboard
```

---

## 🛠️ Maintenance

### **Monitor Storage Usage**
```bash
# PowerShell
$context = New-AzStorageContext -StorageAccountName "networkbuster[random]sa" -UseConnectedAccount
Get-AzStorageAccount -ResourceGroupName "networkbuster-rg" | Get-AzStorageUsage

# Azure CLI
az storage account show --name networkbusterxyz --resource-group networkbuster-rg --query "creation"
```

### **Backup & Restore**
```bash
# Enable versioning
az storage blob service-properties update \
  --account-name networkbuster[random]sa \
  --enable-versioning true

# Download backup
az storage blob download \
  --account-name networkbuster[random]sa \
  --container-name backups \
  --name "backup-2025-12-14.zip" \
  --file local-backup.zip
```

### **Cleanup Old Data**
```bash
# Set lifecycle policy to delete data older than 90 days
az storage account management-policy create \
  --account-name networkbuster[random]sa \
  --resource-group networkbuster-rg \
  --policy @lifecycle-policy.json
```

---

## 🔒 Security Best Practices

1. ✅ **Never hardcode credentials** - Use connection strings from environment
2. ✅ **Enable soft delete** - Recover accidentally deleted blobs
3. ✅ **Use SAS tokens** - Temporary access with limited permissions
4. ✅ **Enable logging** - Monitor access and changes
5. ✅ **Rotate keys regularly** - Every 90 days minimum
6. ✅ **Use private endpoints** - Restrict network access
7. ✅ **Enable Azure Defender** - Security threat detection

---

## 📞 Support & Troubleshooting

### **Common Issues**

**Issue:** "Insufficient permissions"
```bash
# Solution: Check role assignment
az role assignment list --scope /subscriptions/[subid]/resourceGroups/networkbuster-rg
```

**Issue:** "Container not found"
```bash
# Solution: List containers
az storage container list --account-name networkbuster[random]sa
```

**Issue:** "Connection timeout"
```bash
# Solution: Check firewall rules
az storage account network-rule list --account-name networkbuster[random]sa
```

---

## 📚 Documentation Links

- [Azure Storage Documentation](https://docs.microsoft.com/en-us/azure/storage/)
- [Azure Blob Storage Python SDK](https://docs.microsoft.com/en-us/python/api/azure-storage-blob/)
- [Azure Files Documentation](https://docs.microsoft.com/en-us/azure/storage/files/)
- [Azure Table Storage Documentation](https://docs.microsoft.com/en-us/azure/storage/tables/)
- [Azure Queue Storage Documentation](https://docs.microsoft.com/en-us/azure/storage/queues/)

---

## ✅ Deployment Checklist

- [ ] Azure CLI installed and authenticated
- [ ] PowerShell or Bash script ready
- [ ] Bicep template downloaded
- [ ] Deployment parameters configured
- [ ] Resource group exists
- [ ] Run deployment script
- [ ] Verify storage account created
- [ ] Save credentials to `storage-credentials.env`
- [ ] Add to `.gitignore`
- [ ] Configure GitHub Secrets
- [ ] Update application code for storage integration
- [ ] Test uploading to containers
- [ ] Monitor storage costs

---

**Status:** Ready for Production Deployment
**Last Updated:** December 14, 2025
