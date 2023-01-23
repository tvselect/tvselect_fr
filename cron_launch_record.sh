echo --- crontab start: $(date) >> /var/tmp/cron_launch_record.log

bash launch_record.sh >> /var/tmp/cron_launch_record.log 2>&1

echo --- crontab end: $(date) >> /var/tmp/cron_launch_record.log
