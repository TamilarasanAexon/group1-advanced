module "networking" {
  source = "./modules/networking"

  count = var.enable_networking ? 1 : 0

  project_name = var.project_name
  environment  = var.environment
  vpc_cidr     = var.vpc_cidr
}

module "security" {
  source = "./modules/security"

  count = var.enable_security ? 1 : 0

  project_name = var.project_name
  environment  = var.environment
}

module "application_baseline" {
  source = "./modules/application-baseline"

  project_name = var.project_name
  environment  = var.environment
}