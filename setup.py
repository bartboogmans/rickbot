from setuptools import setup

package_name = 'rickbot'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # include srt/Rick-Astley-Never-Gonna-Give-You-Up.srt
        ('share/' + package_name, ['srt/Rick-Astley-Never-Gonna-Give-You-Up.srt']),
    ],

    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bart',
    maintainer_email='bartboogmans@hotmail.com',
    description='Streams srt subtitles to specified ros topic',
    license='MIT License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rickbotmain = rickbot.rickbotmain:main'
        ],
    },
)