# Sonnenhut

A crude Python script for photographers. Displays basic information such as current weather conditions and golden hour for a specified location.

<img src="sonnenhut.png" alt="Sonnenhut">

The script provides the following information:

 - Sunrise and sunset
 - Golden hour start and duration
 - Brief weather summary
 - Current temperature
 - Precipitation probability

## Installation

### openSUSE

1. Install Python 3 and Git: `sudo zypper in python3 git`
2. Install the *Astral* module: `sudo pip install astral`
3. Install the *python-forecast.io* module: `sudo pip install python-forecast.io`
4. Clone the Git repository: `git clone https://github.com/dmpop/sonnenhut.git`

## Usage

1. Switch to the *sonnenhut* directory
2. Run the `./sonnenhut.py fürth` command (replace *fürth* with the desired city)

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin new-feature`
5. Submit a pull request

## History

 - 2017-01-21 Initial release

## Credits

Thanks to Thomas Schraitle for help and guidance.

## License

[The GNU General Public License version 3](https://www.gnu.org/licenses/gpl-3.0.txt)
