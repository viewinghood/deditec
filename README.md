# Python Wrapper for the Deditec RO-Modules (RO-USB and RO-ETH)

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-orange)

## Overview

This project provides a convenient Python wrapper for the Deditec RO-Series modules, including RO-USB and RO-ETH. It supports both Windows and Linux platforms.

### Features

- **Cross-Platform**: Works on Windows and Debian-based Linux distributions (e.g., Ubuntu 22.04 and 24.04).
- **Shared Library Support**: Includes support for `.so` libraries on Linux.
- **Easy Integration**: Simplifies interaction with Deditec RO-Series modules.

## Installation

### Clone the Repository

To get started, clone this repository:

```bash
git clone https://github.com/your-username/deditec-wrapper.git
cd deditec-wrapper
```

### Setup

1. Unpack the zip file and place it in the correct driver samples location.
2. Copy the `delib_eth_so` directory to the appropriate location (see wrapper for details).
3. Compile the `.so` file using `gcc` (instructions are inside the file).

## Usage

Refer to the Python wrapper for defined constants and functions to interact with the Deditec RO-Series modules.

## License

This project is licensed under the [MIT License](LICENSE).

> [!TIP]
> From the defined constants, you can estimate the wrapper's capabilities. Have fun!
