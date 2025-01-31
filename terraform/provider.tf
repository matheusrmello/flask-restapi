terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.84.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "3.0.0-pre1"
    }
  }
}

provider "helm" {
  kubernetes = {
    host                   = module.kubernetes.endpoint
    cluster_ca_certificate = base64decode(module.kubernetes.ca)
    exec = {
      api_version = "client.authentication.k8s.io/v1beta1"
      args        = ["eks", "get-token", "--cluster-name", module.kubernetes.project_name]
      command     = "aws"
    }
  }
}