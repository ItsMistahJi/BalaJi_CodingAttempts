import os

import sys

env_path = sys.prefix
print(f'The path to the environment is: {env_path}')

#for key, value in os.environ.items():
#    print(f'{key}: {value}')

# Replace 'VARIABLE_NAME' with the name of the environment variable you want to check
variable_value = os.getenv('VARIABLE_NAME')
print(f'The value of VARIABLE_NAME is: {variable_value}')