from setuptools import find_packages, setup
import os
package_name = 'roma_description'

def package_files(directory_list):
    paths = []
    for directory in directory_list:
        for path, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(path, filename)
                install_path = os.path.join('share', package_name, path)
                paths.append((install_path, [file_path]))
    return paths

data_files = [
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
]
#add all the files in the launch, urdf and meshes directories to the data_files list
data_files.extend(package_files(['launch', 'urdf', 'meshes']))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    #all the files
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Valka CR',
    maintainer_email='valkacr.dev@gmail.com',
    description='Robot description package for Roma URDF and xacro examples.',
    license='BSD-3-Clause',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
