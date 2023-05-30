# Neural Network course project
This repository contains the source code and assets for the Neural Network course project. The project includes a web application that utilizes LipNet model to perform Visual Speech recognition.

## Installation
To install and run this project, follow these steps:

1. Ensure that Python 3.7 or later is installed on your system.

2. Clone this repository to your local machine or download the ZIP file and extract it.

3. Navigate to the project's root directory in the command line or terminal.

4. Setup the environment.
```
python3 -m venv myenv
myenv\Scripts\activate
```
5. Download [CMake](https://cmake.org/download/) to ensure that all dependecies will work as expected.
6. Install the project dependencies by running the following command:
```
pip install -r requirements.txt
```
7. Once the installation is complete, you can start the web application by running the following command:
```
python src/app.py
```
8. Open the index.html file located at the static folder and enjoy the usage.

## Test cases
* https://github.com/mfedkiv/nn-course-work/assets/89789498/0512eff6-1a35-4780-8d02-42925fe23926

  Predicted result: BIN BLUEE AT Q TWO PLEASE
  
  Expected result: BIN BLUE AT T NINE PLEASE
  
* https://github.com/mfedkiv/nn-course-work/assets/89789498/eeca6569-5557-410d-bb34-315c97f036de

  Predicted result: SET BLUEE IN U TWO SOON
  
  Expected result: BIN BLUE AT L NINE NOW

* https://github.com/mfedkiv/nn-course-work/assets/89789498/7c29ec44-45a2-4e8a-9f90-31e2f7ea6c2a

  Predicted result: BINN WLUEE IN V FUER AGAIN 

  Expected result: BIN BLUE AT V ZERO AGAIN

## Model
Model training, validation and assesment can be found in - https://github.com/nazarkohut/nn-course-work-vsr-models
