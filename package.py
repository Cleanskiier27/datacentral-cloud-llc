"""
NetworkBuster Package Module
Remote connections for Kubernetes and Cloud Organization
"""

__version__ = "1.0.0"
__author__ = "NetworkBuster Team"

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum
import subprocess
import os


# Build Configuration
BUILD_CONFIG = {
    "npm_source_path": r"D:\src downloads\networkbuster",
    "output_path": r"D:\src downloads\networkbuster\dist",
    "node_modules": r"D:\src downloads\networkbuster\node_modules",
}


def npm_install(source_path: str = None) -> subprocess.CompletedProcess:
    """Run npm install in the source directory"""
    path = source_path or BUILD_CONFIG["npm_source_path"]
    return subprocess.run(
        ["npm", "install"],
        cwd=path,
        shell=True,
        capture_output=True,
        text=True
    )


def npm_build(source_path: str = None, script: str = "build") -> subprocess.CompletedProcess:
    """Run npm build script in the source directory"""
    path = source_path or BUILD_CONFIG["npm_source_path"]
    return subprocess.run(
        ["npm", "run", script],
        cwd=path,
        shell=True,
        capture_output=True,
        text=True
    )


def npm_run(script: str, source_path: str = None) -> subprocess.CompletedProcess:
    """Run any npm script in the source directory"""
    path = source_path or BUILD_CONFIG["npm_source_path"]
    return subprocess.run(
        ["npm", "run", script],
        cwd=path,
        shell=True,
        capture_output=True,
        text=True
    )


def build_package(clean: bool = False) -> Dict:
    """
    Full build pipeline for NetworkBuster package
    
    Args:
        clean: If True, removes node_modules before install
    
    Returns:
        Dict with build status and output
    """
    results = {"success": True, "steps": []}
    source_path = BUILD_CONFIG["npm_source_path"]
    
    # Check if source path exists
    if not os.path.exists(source_path):
        return {
            "success": False,
            "error": f"Source path not found: {source_path}",
            "steps": []
        }
    
    # Clean if requested
    if clean:
        node_modules = BUILD_CONFIG["node_modules"]
        if os.path.exists(node_modules):
            import shutil
            shutil.rmtree(node_modules)
            results["steps"].append({"step": "clean", "status": "completed"})
    
    # npm install
    install_result = npm_install(source_path)
    results["steps"].append({
        "step": "npm install",
        "status": "success" if install_result.returncode == 0 else "failed",
        "output": install_result.stdout,
        "error": install_result.stderr if install_result.returncode != 0 else None
    })
    
    if install_result.returncode != 0:
        results["success"] = False
        return results
    
    # npm build
    build_result = npm_build(source_path)
    results["steps"].append({
        "step": "npm build",
        "status": "success" if build_result.returncode == 0 else "failed",
        "output": build_result.stdout,
        "error": build_result.stderr if build_result.returncode != 0 else None
    })
    
    if build_result.returncode != 0:
        results["success"] = False
    
    return results


class CloudProvider(Enum):
    """Supported cloud providers"""
    AZURE = "azure"
    AWS = "aws"
    GCP = "gcp"
    DIGITAL_OCEAN = "digitalocean"
    LINODE = "linode"


class KubernetesDistro(Enum):
    """Supported Kubernetes distributions"""
    AKS = "aks"           # Azure Kubernetes Service
    EKS = "eks"           # Amazon Elastic Kubernetes Service
    GKE = "gke"           # Google Kubernetes Engine
    K3S = "k3s"           # Lightweight Kubernetes
    MINIKUBE = "minikube"
    KIND = "kind"         # Kubernetes in Docker
    OPENSHIFT = "openshift"


@dataclass
class KubernetesRemote:
    """Kubernetes cluster remote configuration"""
    name: str
    distro: KubernetesDistro
    api_server: str
    namespace: str = "default"
    kubeconfig_path: Optional[str] = None
    context: Optional[str] = None
    service_account: Optional[str] = None
    token: Optional[str] = None
    ca_cert_path: Optional[str] = None
    insecure_skip_tls: bool = False
    labels: Dict[str, str] = field(default_factory=dict)

    def get_connection_string(self) -> str:
        """Generate connection string for the cluster"""
        return f"k8s://{self.distro.value}@{self.api_server}/{self.namespace}"

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "distro": self.distro.value,
            "api_server": self.api_server,
            "namespace": self.namespace,
            "kubeconfig_path": self.kubeconfig_path,
            "context": self.context,
            "service_account": self.service_account,
            "insecure_skip_tls": self.insecure_skip_tls,
            "labels": self.labels
        }


@dataclass
class CloudOrganization:
    """Cloud organization/account configuration"""
    name: str
    provider: CloudProvider
    org_id: str
    subscription_id: Optional[str] = None  # Azure
    account_id: Optional[str] = None       # AWS
    project_id: Optional[str] = None       # GCP
    region: str = "us-east-1"
    credentials_path: Optional[str] = None
    environment: str = "production"
    tags: Dict[str, str] = field(default_factory=dict)
    kubernetes_clusters: List[KubernetesRemote] = field(default_factory=list)

    def get_identifier(self) -> str:
        """Get the primary identifier based on provider"""
        if self.provider == CloudProvider.AZURE:
            return self.subscription_id or self.org_id
        elif self.provider == CloudProvider.AWS:
            return self.account_id or self.org_id
        elif self.provider == CloudProvider.GCP:
            return self.project_id or self.org_id
        return self.org_id

    def add_kubernetes_cluster(self, cluster: KubernetesRemote) -> None:
        """Add a Kubernetes cluster to this organization"""
        self.kubernetes_clusters.append(cluster)

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "provider": self.provider.value,
            "org_id": self.org_id,
            "subscription_id": self.subscription_id,
            "account_id": self.account_id,
            "project_id": self.project_id,
            "region": self.region,
            "environment": self.environment,
            "tags": self.tags,
            "kubernetes_clusters": [c.to_dict() for c in self.kubernetes_clusters]
        }


class NetworkBusterPackage:
    """
    Main NetworkBuster package manager for cloud and Kubernetes remotes
    """

    def __init__(self, package_name: str = "networkbuster"):
        self.package_name = package_name
        self.version = __version__
        self.cloud_organizations: List[CloudOrganization] = []
        self.kubernetes_remotes: List[KubernetesRemote] = []

    def add_cloud_organization(self, org: CloudOrganization) -> None:
        """Register a cloud organization"""
        self.cloud_organizations.append(org)

    def add_kubernetes_remote(self, remote: KubernetesRemote) -> None:
        """Register a standalone Kubernetes remote"""
        self.kubernetes_remotes.append(remote)

    def get_all_kubernetes_clusters(self) -> List[KubernetesRemote]:
        """Get all Kubernetes clusters (standalone + org-attached)"""
        clusters = list(self.kubernetes_remotes)
        for org in self.cloud_organizations:
            clusters.extend(org.kubernetes_clusters)
        return clusters

    def list_remotes(self) -> Dict:
        """List all configured remotes"""
        return {
            "cloud_organizations": [org.to_dict() for org in self.cloud_organizations],
            "kubernetes_remotes": [k.to_dict() for k in self.kubernetes_remotes],
            "total_clusters": len(self.get_all_kubernetes_clusters())
        }

    def connect_kubernetes(self, cluster_name: str) -> Optional[KubernetesRemote]:
        """Find and return a Kubernetes cluster by name"""
        for cluster in self.get_all_kubernetes_clusters():
            if cluster.name == cluster_name:
                return cluster
        return None

    def connect_cloud(self, org_name: str) -> Optional[CloudOrganization]:
        """Find and return a cloud organization by name"""
        for org in self.cloud_organizations:
            if org.name == org_name:
                return org
        return None


# Default package instance
default_package = NetworkBusterPackage()


def create_azure_aks_remote(
    name: str,
    resource_group: str,
    cluster_name: str,
    subscription_id: str,
    region: str = "eastus"
) -> KubernetesRemote:
    """Helper to create an Azure AKS remote configuration"""
    return KubernetesRemote(
        name=name,
        distro=KubernetesDistro.AKS,
        api_server=f"https://{cluster_name}.{region}.azmk8s.io",
        labels={
            "resource_group": resource_group,
            "subscription_id": subscription_id,
            "region": region
        }
    )


def create_aws_eks_remote(
    name: str,
    cluster_name: str,
    account_id: str,
    region: str = "us-east-1"
) -> KubernetesRemote:
    """Helper to create an AWS EKS remote configuration"""
    return KubernetesRemote(
        name=name,
        distro=KubernetesDistro.EKS,
        api_server=f"https://{cluster_name}.{region}.eks.amazonaws.com",
        labels={
            "account_id": account_id,
            "region": region
        }
    )


def create_gcp_gke_remote(
    name: str,
    cluster_name: str,
    project_id: str,
    zone: str = "us-central1-a"
) -> KubernetesRemote:
    """Helper to create a GCP GKE remote configuration"""
    return KubernetesRemote(
        name=name,
        distro=KubernetesDistro.GKE,
        api_server=f"https://{cluster_name}.{zone}.container.googleapis.com",
        labels={
            "project_id": project_id,
            "zone": zone
        }
    )


if __name__ == "__main__":
    # Example usage
    pkg = NetworkBusterPackage()

    # Add Azure organization with AKS cluster
    azure_org = CloudOrganization(
        name="NetworkBuster-Azure",
        provider=CloudProvider.AZURE,
        org_id="networkbuster-org",
        subscription_id="00000000-0000-0000-0000-000000000000",
        region="eastus",
        environment="production"
    )
    
    aks_cluster = create_azure_aks_remote(
        name="prod-aks",
        resource_group="networkbuster-rg",
        cluster_name="nb-aks-prod",
        subscription_id=azure_org.subscription_id
    )
    azure_org.add_kubernetes_cluster(aks_cluster)
    pkg.add_cloud_organization(azure_org)

    # Add AWS organization with EKS cluster
    aws_org = CloudOrganization(
        name="NetworkBuster-AWS",
        provider=CloudProvider.AWS,
        org_id="networkbuster-aws",
        account_id="123456789012",
        region="us-west-2",
        environment="production"
    )
    
    eks_cluster = create_aws_eks_remote(
        name="prod-eks",
        cluster_name="nb-eks-prod",
        account_id=aws_org.account_id,
        region="us-west-2"
    )
    aws_org.add_kubernetes_cluster(eks_cluster)
    pkg.add_cloud_organization(aws_org)

    # Print configuration
    import json
    print(json.dumps(pkg.list_remotes(), indent=2))
