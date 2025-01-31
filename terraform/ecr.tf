resource "aws_ecr_repository" "flask" {
  name         = "flask-api"
  force_delete = true

}