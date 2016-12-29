import os
import time
import ddbc

os.system("python setup.py install")

os.system("rm -rf dist")
os.system("pandoc README.md --from=markdown --to=rst > README.txt")
os.system("python setup.py sdist bdist_wheel")
os.system("twine upload dist/*")
os.remove('README.txt')
os.system("rm -rf dist")

time.sleep(120)

os.system("git tag v{}".format(ddbc.__version__))
os.system("git push origin v{}".format(ddbc.__version__))
