.PHONY: run build-requires requirements

#
# The executable name
#
PROGRAM_NAME=vatsim-monitor

#
# Tools used
#
PYTHON=python3
PIP=$(PYTHON) -m pip
PYINSTALLER_OPTIONS=--noconfirm --clean
PYINSTALLER=pyinstaller ${PYINSTALLER_OPTIONS}

#
# Detect operating system
#
OS := $(shell uname)
OS := $(OS:Linux=nix)
OS := $(OS:%BSD=nix)
OS := $(OS:DragonFlyD=nix)
OS := $(OS:SunOS=nix)
OS := $(OS:MINGW%=win)
OS := $(OS:MSYS%=win)
OS := $(OS:Windows_NT=win)
OS := $(OS:Darwin=mac)

#
# Local directories used
#
BUILDTOOLS=buildtools/${OS}
BUILD=build
DIST=dist

#
# Specification files
#
REQUIREMENTS=requirements.txt
PYINSTALLER_SPEC=${BUILDTOOLS}/${PROGRAM_NAME}.spec

run:
	./program.py

build-requires:
	./${BUILDTOOLS}/install-requires.sh

build: build-requires clean requirements
	${PYINSTALLER} ${PYINSTALLER_SPEC}

requirements: ${REQUIREMENTS}
	${PIP} install -r ${REQUIREMENTS}

clean:
	${RM} -r ${BUILD} ${DIST}
