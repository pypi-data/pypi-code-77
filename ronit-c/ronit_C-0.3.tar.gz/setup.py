from distutils.core import setup
setup(
  name = 'ronit_C',         # How you named your package folder (MyLib)
  packages = ['ronit_C'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Ronit_C is a library for python that teaches you how to program really easily!',   # Give a short description about your library
  author = 'Serge Brainin, Yuval Noiman',                   # Type in your name
  author_email = 'forecaster1310@gmail.com',      # Type in your E-Mail
  url = 'https://www.sb-3design.com/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/forecaster-cyber/Ronit_C/archive/0.3.tar.gz',    # I explain this later on
  keywords = ['LOW-CODE', 'EASY', 'PYGAME'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second

          'pygame',
      'pyautogui'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)