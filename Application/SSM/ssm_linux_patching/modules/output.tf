output "patch_baseline_id" {
  value = aws_ssm_patch_baseline.custom_patch_baseline.id
}

output "maintenance_window_id" {
  value = aws_ssm_maintenance_window.install_linux.id
}
