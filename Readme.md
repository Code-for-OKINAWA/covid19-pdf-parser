# Okinawa COVID-19 Cases PDF parser

## Require tool
[pdfplumer](https://github.com/jsvine/pdfplumber)

```
pip install pdfplumer
```

## How-To

### Download PDF from Okinawa Prefecture official report
[Report list](https://www.pref.okinawa.lg.jp/site/hoken/chiikihoken/kekkaku/press/20200214_covid19_pr1.html)

```
curl -OL [PDF Url]
```

### Execute converter
```
python3 convert_table.py path/to/file
```

### Output File

```
output.csv
```