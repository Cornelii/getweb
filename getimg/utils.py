import os

def dir_check_and_create(path):
  """
  주어진 경로가 존재하는지 확인하고, 없으면 경로에 있는 모든 디렉토리를 생성합니다.

  Args:
    path: 디렉토리 경로

  Returns:
    디렉토리가 존재하면 True, 그렇지 않으면 False를 반환합니다.
  """
  # 경로가 존재하는지 확인합니다.
  if os.path.exists(path):
    return True

  # 경로가 존재하지 않으면 디렉토리를 생성합니다.
  try:
    os.makedirs(path)
    return True
  except OSError:
    return False

def gen_seq(s):
    for a in range(s, s+10000000):
        yield a