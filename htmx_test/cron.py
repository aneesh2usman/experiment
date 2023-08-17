
from htmx_test.management.commands.automate_requests import Command
def my_scheduled_job():
  command = Command()
  command.handle()