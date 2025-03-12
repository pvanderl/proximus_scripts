class PropertyBundle:

  def __init__(self, name, load_all=False):
    self.name = name
    self.locales = {}
    if load_all:
      self.load_properties('fr')
      self.load_properties('nl')
    self.load_properties('en')

  def get_file_name(self, locale):
    return 'properties/' + self.name + (
        ('_' + locale) if locale != 'en' else '') + '.properties'

  def load_properties(self, locale):
    self.locales[locale] = {}
    file_name = self.get_file_name(locale)
    file = open(file_name, "r", encoding='latin-1')
    str = file.read()
    file.close()
    lines = str.split("\n")
    for line in lines:
      x = line.split("=")
      if len(x) != 2:
        continue
      key, value = x[0], x[1]
      self.locales[locale][key] = value


computed_keys = [
    'ROAMING_TITLE_PAYU', 'NATIONAL_EU_TITLE', 'INTERNATIONAL_TITLE_PAYU',
    'ROAMING_DESCRIPTION', 'NATIONAL_EU_TITLE_PAYU',
    'INTERNATIONAL_TOOLTIP_TITLE', 'TABLE_FIELD_CONSUMED_VOLUME',
    '404_DESCRIPTION', 'INTERNATIONAL_DESCRIPTION', 'PAYU_ONLY_NATIONAL',
    'INTERNATIONAL_TITLE', 'NATIONAL_USAGE_TOOLTIP', 'ROAMING_TITLE',
    'APP_TITLE'
]


def extract_duplicated_keys():
  bundles = [
      #    PropertyBundle('data'),
      PropertyBundle('voice'),
      PropertyBundle('sms'),
      PropertyBundle('mms'),
  ]

  shared_keys = []

  for key in bundles[0].locales['en'].keys():
    present_in_all = True
    same_in_all = True
    value = bundles[0].locales['en'][key]
    for bundle in bundles[1:]:
      if key not in bundle.locales['en'].keys():
        present_in_all = False
        break
    if present_in_all:
      shared_keys.append(key)

  print('shared_keys')
  print(shared_keys)


def extract_properties():

  bundle = PropertyBundle('voice', True)
  for lan in bundle.locales.keys():
    print()
    print(lan)
    for key in computed_keys:
      print(key + '=' + bundle.locales[lan][key])


def remove_keys():

  def for_bundle(bundle: PropertyBundle):
    for locale in bundle.locales.keys():
      loc = bundle.locales[locale]
      file_name = bundle.get_file_name(locale)
      with open(file_name, "w") as file:
        for key in loc.keys():
          if key not in computed_keys:
            file.write(key + "=" + loc[key] + "\n")
        file.close()

  bundles = [
      PropertyBundle('voice', True),
      PropertyBundle('sms', True),
      PropertyBundle('mms', True),
  ]
  for bundle in bundles:
    for_bundle(bundle)


def extended_approach():

  def save_to_common_file(locale: str, key: str, value: str):
    file_name = 'properties/common_' + locale + '.properties'
    with open(file_name, "a") as file:
      file.write(key + "=" + value + "\n")
      file.close()

  bundles = [
      PropertyBundle('voice', True),
      PropertyBundle('sms', True),
      PropertyBundle('mms', True),
  ]
  merged_keys = []
  non_merged_keys = []
  locs = ['en', 'fr', 'nl']
  for key in computed_keys:
    print()
    print('\033[95m' + key)
    for loc in locs:
      print('\033[92m' + loc.upper() + '\033[0m')
      for bundle in bundles:
        print(bundle.locales[loc][key])
    res = input('Merge?\n')
    if res == '1':
      merged_keys.append(key)
      for loc in locs:
        ind = int(
            input('Which input to use for: \033[92m' + loc.upper() +
                  '\033[0m?\n')) - 1
        save_to_common_file(loc, key, bundles[ind].locales[loc][key])
    else:
      non_merged_keys.append(key)

  print('merged_keys')
  print(merged_keys)
  print()
  print('non_merged_keys')
  print(non_merged_keys)


def rename_keys():

  def for_bundle(bundle: PropertyBundle):
    for locale in bundle.locales.keys():
      loc = bundle.locales[locale]
      file_name = bundle.get_file_name(locale)
      with open(file_name, "w") as file:
        for key in loc.keys():
          if key in computed_keys:
            file.write('usage.' + bundle.name + '.' + key + "=" + loc[key] + "\n")
          else:
            file.write(key + "=" + loc[key] + "\n")
        file.close()

  bundles = [
      PropertyBundle('voice', True),
      PropertyBundle('sms', True),
      PropertyBundle('mms', True),
  ]
  for bundle in bundles:
    for_bundle(bundle)

rename_keys()
