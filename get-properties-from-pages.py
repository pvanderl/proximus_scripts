import yaml


class Page:

  def __init__(self, path, obj):
    self.path = path
    self.categoryL1 = obj.get('categoryL1', '')
    self.categoryL2 = obj.get('categoryL2', '')
    self.categoryL3 = obj.get('categoryL3', '')
    self.categoryL4 = obj.get('categoryL4', '')
    self.categoryL2 = obj.get('categoryL2', '')
    self.pageId = obj.get('pageId', '')
    self.pageName = obj.get('pageName', '')
    self.dynatracePageGroup = obj.get('dynatracePageGroup', '')

  def __str__(self):
    return ('"' + '","'.join([
        self.path, self.pageId, self.pageName,
        self.categoryL1, self.categoryL2, self.categoryL3, self.categoryL4,
        self.dynatracePageGroup
    ]) + '"')


pages = []


def is_page(obj):
  return obj.get("jcr:primaryType") == "mgnl:page"


def is_redirection(obj):
  return obj.get(
      "mgnl:template") == "common-component:pages/redirect" or obj.get(
          "mgnl:template") == "MYENT_FE_Generic:pages/redirect"


def recurse(obj, path):
  if is_page(obj) and not is_redirection(obj):
    pages.append(Page(path, obj))
  for key, value in obj.items():
    if isinstance(value, dict):
      recurse(value, path + '/' + key)


with open("input.yaml", "r") as file:
  obj = yaml.load(file, Loader=yaml.FullLoader)
  recurse(obj, '')

with open("output.csv", "w") as file:
  for p in pages:
    file.write(str(p) + "\n")
