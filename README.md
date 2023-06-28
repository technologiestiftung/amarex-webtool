# Amarex web tool

## Compile Abimo

1. Clone the [Abimo repo](https://github.com/KWB-R/abimo/tree/build-dll-2) on your computer

    ```
    git clone https://github.com/KWB-R/abimo.git
    ```

2. Install [Qt](https://www.qt.io/). 

    If you use macOS:
    
    ```
    brew install qt@5
    ```

3. You may also need to set:

    ```
    export LDFLAGS="-L/opt/homebrew/opt/qt@5/lib"\n
    export CPPFLAGS="-I/opt/homebrew/opt/qt@5/include"
    
    echo 'export PATH="/opt/homebrew/opt/qt@5/bin:$PATH"' >> ~/.zshrc
    ```

4.  Call `qmake` referencing the `.pro` file. For that, run the following command from the root directory. This will create a makefile.

    ```
    qmake src/app/app.pro
    ```

5. Finally, compile the C++ program by running the following command.

    ```
    make release
    ```
   
## Install requirements

To install the required python packages, run this command from the root directory.

```
pip install requirements.txt
```
   
## Call the compiled Abimo app from Python

Run the Python wrapper with the `run_abimo.py` script.
You will need to provide the following positional arguments:

`lib_dir:` Path to the directory storing the compiled Abimo library.

`output_dir:` Path to the dir where to save the output DBF file.

`input_file:` Path to the config XML file.

And optionally:

`config_file:` Path to the config XML file. 
If you don't specify a config file, the default values will be used.

```
python run_abimo.py LIB_DIR OUTPUT_DIR INPUT_FILE [CONFIG_FILE]
```

The results will be stored in a DBF file in the output directory that you provided.

## Read the output

To print the results that you obtained in your console, run the `read_dbf.py` script with the following positional argument:

`input_file:` Path to the DBF file to read, i.e., the output file you obtained in the previous step.

And optionally:

`n_rows:` Print only the first N rows.

```
python read_dbf.py INPUT_FILE [N_ROWS]
```
