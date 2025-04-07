from setuptools import setup, find_packages

setup(
    name="transcription_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai-whisper>=20240930",
        "ffmpeg-python>=0.2.0",
    ],
    entry_points={
        "console_scripts": [
            "transcribe=transcription_app.cli:main",
        ],
    },
    python_requires=">=3.8",
    author="Oliver Oliverio",
    author_email="oliveroliverio@gmail.com",
    description="A Python application for transcribing audio and video files using OpenAI's Whisper",
    keywords="transcription, audio, video, whisper, openai",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
