sudo apt-get update
sudo apt-get install -y python-dev
sudo apt-get install -y python-pip
sudo apt-get install -y python-smbus
sudo apt-get install -y bluez
sudo apt-get install -y libbluetooth-dev
sudo apt-get install -y unzip
sudo pip install pybluez
sudo wget --no-check-certificate https://pybluez.googlecode.com/files/PyBluez-0.20.zip
sudo unzip PyBluez-0.20.zip
sudo python PyBluez-0.20/setup.py install



