from setuptools import setup, find_packages

setup(
    name='django-user-comments',
    version='0.0.4',
    description='Library for adding comments of users related with object',
    author='Lubos Matl',
    author_email='matllubos@gmail.com',
    packages=find_packages(),
    install_requires=[
        'django-chamber>=0.5.25',
    ],
    include_package_data=True,
    zip_safe=False,
)
