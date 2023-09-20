module "patching" {
  source = "./modules"

  custom_patch_name             = var.custom_patch_name
  operating_system              = var.operating_system
  approved_patches              = var.approved_patches
  patches_compliance_level      = var.patches_compliance_level
  patch_group                   = var.patch_group
  name                          = var.name
  schedule                      = var.schedule
  maintenance_window_duration   = var.maintenance_window_duration
  maintenance_window_cutoff     = var.maintenance_window_cutoff
  resource_type                 = var.resource_type
  rhel_target                   = var.rhel_target
  task_type                     = var.task_type
  task_arn                      = var.task_arn
  task_install_priority         = var.task_install_priority
  service_role_arn              = var.service_role_arn
  notification_arn              = var.notification_arn
  notification_events           = var.notification_events
  notification_type             = var.notification_type
  max_concurrency               = var.max_concurrency
  max_errors                    = var.max_errors
  targets                       = var.targets
  task_parameters               = var.task_parameters
  s3_bucket_name                = var.s3_bucket_name
  s3_bucket_prefix_install_logs = var.s3_bucket_prefix_install_logs
}
