from setuptools import find_packages, setup

package_name = 'tb3_obstacle_avoider'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ishita',
    maintainer_email='ishitachaudhary2003@gmail.com',
    description='Obstacle Avoider',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'avoider = tb3_obstacle_avoider.avoider_node:main',
        ],
    },
)
