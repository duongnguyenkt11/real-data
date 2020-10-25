
def exec3(cmd): #
  print(f"****\n running: {cmd} ****")
  import subprocess
  process = subprocess.Popen(cmd.split(" "),
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE)
  stdout, stderr = process.communicate()
  print (stdout.decode("utf-8"), stderr.decode("utf-8"))
  return stdout.decode("utf-8"), f"""error code: {stderr.decode("utf-8")}"""