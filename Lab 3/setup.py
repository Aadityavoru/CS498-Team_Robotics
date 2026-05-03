from setuptools import setup

package_name = 'lab3'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robert molina',
    maintainer_email='rcmolina@illinois.edu',
    description='lab3 tf2 skeleton code',
    license='MIT license',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'listener_node = lab3.listener_node:main',
            'ball_publisher = lab3.ball_publisher:main',
            'ball_attached_frame = lab3.ball_attached_frame:main'
        ],
    },
)
