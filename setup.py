from setuptools import setup, find_packages

setup(
    name="novnc-for-vcenter",
    version="1.0",
    description="Just for vcenter novnc console.",
    license="CertuseNet",
    author="Hongquan Zhu",
    author_email="zhuhq@certusnet.com.cn",
    packages= find_packages(),
    include_package_data=True,
    install_requires=[
        'oslo_log',
        'six',
        'websockify',
        'exceptions',
        'base64',
        "json"
    ]
)