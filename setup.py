from setuptools import setup, find_packages

setup(
    name='gestion-approvisionnement',  # Nom du package
    version='1.0.0',
    author='Tagang Vanelle',
    author_email='tagang@example.com',
    description='Application Django de gestion des stocks et approvisionnements',
    # Suppression de la lecture du README.md
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    url='https://github.com/vanelle1/gestion',  # ou ton site perso
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=3.2',
        'plotly',
        'pandas',
        'requests',
        # ajoute les autres dépendances ici
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
