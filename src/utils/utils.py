class Utils:
  """
  Utilities container
  """
  @staticmethod
  def merge_dicts(a: dict, b: dict, path=None) -> dict:
    """ Merges b into a """
    path = [] if path is None else path

    for key in b:
      if key in a:
        if isinstance(a[key], dict) and isinstance(b[key], dict):
          Utils.merge_dicts(a[key], b[key], path + [str(key)])
        elif a[key] == b[key]:
          pass
      else:
        a[key] = b[key]

    return a
