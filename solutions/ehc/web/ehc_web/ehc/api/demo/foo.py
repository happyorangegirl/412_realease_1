import time

timeout = 60

def main():
  while timeout > 0:
    print 'Timeout: {}s'.format(timeout)
    timeout -= 1

  print 'Task has been timeout.'


if __name__ == '__main__':
  main()