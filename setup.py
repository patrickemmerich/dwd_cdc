from setuptools import setup, find_packages

requires = [
    'click', 'pandas', 'bokeh'
]

deploy_requires = [
]

setup(
    name='dwd_cdc',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description="""Show Climate Information from DWD CDC""",
    author='Patrick Emmerich <mail@patrick-emmerich.de>',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    url='',
    long_description=open('README.md').read(),
    entry_points={"console_scripts": [
        "data = dwd_cdc.cli:show_data",
        "dashboard = dwd_cdc.cli:show_dashboard"
    ]}
)
