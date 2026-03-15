from setuptools import setup
import os
from glob import glob

package_name = 'leo_nav_custom'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ahmet Can',
    maintainer_email='ahmetcan@todo.todo',
    description='Custom flat world autonomous navigation package for Leo Rover',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'go_to_goal = leo_nav_custom.go_to_goal:main',
            'user_input = leo_nav_custom.user_input:main',
        ],
    },
)
