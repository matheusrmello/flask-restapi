module "kubernetes" {
  source       = "git@github.com:matheusrmello/terraform-eks.git?ref=main"
  cidr_block   = "10.34.0.0/16"
  project_name = "flask-restapi"
  region       = "us-east-1"
  tags = {
    "Department" = "DevOps"
    "Project"    = "Flask-RestAPI-eks"
  }
}
