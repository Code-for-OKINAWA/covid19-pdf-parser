# Okinawa COVID-19 Cases PDF parser

## About
The tool will download the latest PDF from [新型コロナウイルス感染症患者・無症状病原体保有者の発生について](https://www.pref.okinawa.lg.jp/site/hoken/chiikihoken/kekkaku/press/20200214_covid19_pr1.html) and convert it to a csv file.

## Important Notice
## ⚠️‼️ This output result cannot be used as a raw data directly ‼️⚠️
Because of the extracted data relies on the PDF format, this parser may miss some data from the PDF document due to incomplete table border.
Please check the raw data before implement to your project.

## Require tool
[pdfplumber](https://github.com/jsvine/pdfplumber)

```
pip install pdfplubmer
```

## How-To

### Execute converter
```
$ python3 auto_parser.py
```

### Output File
```
./data/output.csv
```


