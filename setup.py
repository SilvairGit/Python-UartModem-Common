from setuptools import setup

__version__ = '2.8.0'

setup(
    name="silvair_uart_common_libs",
    version=__version__,
    author="Tomasz Szewczyk",
    author_email="tomasz.szewczyk@silvair.com",
    packages=["silvair_uart_common_libs"],
    include_package_data=True,
    python_requires=">=3.6.0",
    install_requires=["psutil==5.4.1",
                      "pyserial>=3.4",
                      "crcmod==1.7",
                      "setuptools>=30.0.0"]
)
