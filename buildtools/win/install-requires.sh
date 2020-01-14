PYINSTALLER_URL=https://files.pythonhosted.org/packages/3c/c9/c3f9bc64eb11eee6a824686deba6129884c8cbdf70e750661773b9865ee0/PyInstaller-3.6.tar.gz
PYINSTALLER_VER=3.6

install gtk3
install python3
install python3-pip
install python3-gobject

type pyinstaller >/dev/null 2>&1 || {

	wget $PYINSTALLER_URL
	tar xf PyInstaller-${PYINSTALLER_VER}.tar.gz
	python3 -m pip install PyInstaller-${PYINSTALLER_VER}/
    rm -rf PyInstaller-${PYINSTALLER_VER}
    rm PyInstaller-${PYINSTALLER_VER}.tar.gz
}

install() {
    pacman -S --noconfirm --needed mingw-w64-x86_64-$1 \;
}
