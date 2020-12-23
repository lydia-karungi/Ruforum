import os, sys

base = '/home/nemesisfixx/LABS/8TECH/ruforum/'
base_parent = os.path.dirname(base)


# Remember original sys.path.
prev_sys_path = list(sys.path)


#new path...
sys.path.append(base)
sys.path.append(base_parent)

env_path = os.path.join(base_parent, 'env/lib/python3.5/site-packages')

# Activate your virtual env
activate_env=os.path.join(base_parent, 'env/bin/activate_this.py')
exec(compile(open(activate_env).read(), activate_env, 'exec'), dict(__file__=activate_env))

#---------------
import os, sys
# add the hellodjango project path into the sys.path

# add the virtualenv site-packages path to the sys.path
sys.path.append(env_path)

# poiting to the project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ruforum.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
