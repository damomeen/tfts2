from setuptools import setup, find_packages

setup(name='tfts2',
      version='0.1',
      author='Damian Parniewicz',
      author_email='damian.parniewicz@gmail.com',
      package_dir = {'tfts2': 'src'},
      packages=find_packages(),
      description = ("tfts2 subagent plugin for NET-SNMP"),
      keywords = 'SNMP,  AgentX',
      install_requires=['pyagentx', 'xmltodict'],
      include_package_data = True,
)
