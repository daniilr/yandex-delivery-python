from setuptools import setup, find_packages

setup(
    name='yandex-delivery',
    packages=['yandex_delivery'],
    version='0.0.1',
    description='Yandex Delivery python client (python-клиент «Яндекс.Доставик»',
    long_description=open('DESCRIPTION.rst').read(),
    license='MIT License',
    author='Daniil Ryzhkov',
    author_email='i@daniil-r.ru',
    url='https://github.com/daniilr/yandex-delivery-pythonlj',
    download_url='https://github.com/daniilr/yandex-delivery-python/',
    keywords=['yandex', 'delivery', 'logistics', "business"],
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha"
    ],
    install_requires=[
        'requests>=2.10.0',
    ],
    platforms='osx, posix, linux, windows',
)
