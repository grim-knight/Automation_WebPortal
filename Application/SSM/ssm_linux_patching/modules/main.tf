# Create a custom patch baseline
resource "aws_ssm_patch_baseline" "custom_patch_baseline" {
  name                              = var.custom_patch_name
  operating_system                  = var.operating_system
  approved_patches                  = var.approved_patches # List of approved patches
  approved_patches_compliance_level = var.patches_compliance_level
  description                       = "Custom patch baseline for RHEL instances"
}

# Assign the custom patch baseline to a patch group
resource "aws_ssm_patch_group" "linux_patch_group" {
  baseline_id = aws_ssm_patch_baseline.custom_patch_baseline.id
  patch_group = var.patch_group
}

# Specify the default the patch baseline
resource "aws_ssm_default_patch_baseline" "example" {
  baseline_id      = aws_ssm_patch_baseline.custom_patch_baseline.id
  operating_system = var.operating_system
}

# Create the maintenance window
resource "aws_ssm_maintenance_window" "install_linux" {
  name     = var.name
  schedule = var.schedule
  duration = var.maintenance_window_duration
  cutoff   = var.maintenance_window_cutoff
}

# Assign the targets using the patch group for the maintenance window
resource "aws_ssm_maintenance_window_target" "target_install" {
  window_id     = aws_ssm_maintenance_window.install_linux.id
  resource_type = var.resource_type

  targets {
    key    = var.rhel_target.key
    values = [var.rhel_target.values]
  }
}

# Assign the RunCommandTask to the maintenance window -> AWS-RunPatchBaseline
resource "aws_ssm_maintenance_window_task" "task_install_patches" {
  name             = var.name
  window_id        = aws_ssm_maintenance_window.install_linux.id
  task_type        = var.task_type
  task_arn         = var.task_arn # Use the appropriate ARN for the AWS-RunPatchBaseline document
  priority         = var.task_install_priority
  service_role_arn = var.service_role_arn
  max_concurrency  = var.max_concurrency
  max_errors       = var.max_errors
  targets {
    key    = var.targets
    values = aws_ssm_maintenance_window_target.target_install.*.id
  }

  task_invocation_parameters {
    run_command_parameters {
      comment          = "Apply patches using custom patch baseline"
      document_version = "$LATEST" # Use the latest version of the document
      parameter {
        name   = var.task_parameters.key1
        values = [var.task_parameters.value1]
      }
      parameter {
        name   = var.task_parameters.key2
        values = [var.task_parameters.value2]
      }

      output_s3_bucket     = var.s3_bucket_name
      output_s3_key_prefix = var.s3_bucket_prefix_install_logs
      service_role_arn     = var.service_role_arn
      notification_config {
        notification_arn    = var.notification_arn # Specify your SNS topic ARN here
        notification_events = [var.notification_events]
        notification_type   = var.notification_type
      }

    }
  }
}
