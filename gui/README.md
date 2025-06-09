# Matrix Ingestor

**Matrix Ingestor** is a powerful, local-first Excel transformation toolkit with a modern UI built using Python and Tkinter. It enables you to visually manipulate, transform, and join Excel data with real-time previews and export capabilities.

---

## 🚀 Features

### ✅ Interactive Excel Management

* Load `.xlsx` or `.xls` files
* Multi-sheet navigation
* Configurable header row

### ✅ Visual Column Selection

* Select columns via checkboxes
* Apply and preview formulas using `pandas.eval()` and `asteval`
* Live validation and result previews

### ✅ Preset System

* Save and apply column/formula presets
* Persist configurations for repeated use

### ✅ Reference Data Join

* Load secondary Excel file
* Map primary and reference keys
* Left join with selected reference columns

### ✅ Export and Upload

* Export processed data to Excel
* Optional upload to Confluence with comments and token security

---

## 📦 Requirements

* Python 3.7+
* Dependencies:

  ```bash
  pip install pandas openpyxl asteval
  ```

---

## 🛠️ Running the App

```bash
python main.py
```

---

## 🗂️ Project Structure (Full)

```
matrix-ingestor/
├── main.py
├── read2txt.py
├── app_settings.json
├── config.json
├── presets.json
├── gui/
│   ├── __init__.py
│   ├── app.py
│   ├── app copy.py
│   ├── config.json
│   ├── confluence/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── ui.py
│   │   ├── uploader.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config_manager.py
│   │   ├── exporter.py
│   │   ├── formula_engine.py
│   │   ├── loader.py
│   │   ├── presets.py
│   │   ├── conflunce/
│   │   │   ├── config.py
│   │   │   ├── metadata.py
│   │   │   ├── uploader.py
│   ├── tools/
│   │   ├── refactor_layout.py
│   │   ├── split_utils.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── layout.py
│   │   ├── layout copy.py
│   │   ├── theme.py
│   │   ├── export_filename_customizer.py
│   │   ├── custom_widgets.py
│   │   ├── utils.py
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── column_controls_section.py
│   │   │   ├── config_export_section.py
│   │   │   ├── header.py
│   │   │   ├── main_file_section.py
│   │   │   ├── presets_section.py
│   │   │   ├── reference_join_section.py
│   │   │   ├── status_bar.py
│   │   ├── helpers/
│   │   │   ├── __init__.py
│   │   │   ├── dialogs.py
│   │   │   ├── file_utils.py
│   │   │   ├── palette.py
│   │   │   ├── statusbar.py
│   │   │   ├── tooltips.py
│   │   │   ├── window.py
```

---

## 🤝 Contributing

Contributions are welcome. Feel free to open issues or submit PRs.

---

## 📄 License

MIT License
