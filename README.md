# SpO₂ Calculator

🩺 A simple and user-friendly application for calculating blood oxygen saturation (SpO₂) based on multi-wavelength pulse oximetry.

## Description

SpO₂ Calculator is a desktop Python application with a graphical user interface for calculating blood oxygen saturation levels. The program uses data from four wavelengths (660, 805, 880, 940 nm) and applies a specialized formula for accurate SpO₂ calculation.

## Features

- ✨ Modern and intuitive user interface
- 📊 Support for four wavelengths (660, 805, 880, 940 nm)
- 🔢 Display of intermediate calculations (R-values)
- 📋 Copy results to clipboard functionality
- 🎨 Color coding for different wavelengths
- ✂️ Context menu for text operations
- 🧮 Support for decimal numbers with both dot and comma

## Requirements

- Python 3.12
- tkinter (usually included with Python standard distribution)

## Installation and Usage

1. Clone the repository:
```bash
git clone https://github.com/fortrane/spo2-calculator.git
cd spo2-calculator
```

2. Run the program:
```bash
python spo2_calculator.py
```

## How to Use

1. Enter **Id** (incident light) and **Is** (scattered light) values for each wavelength
2. Click the **"🧮 Calculate"** button
3. View the intermediate R-values and final SpO₂ result
4. Use **"📋 Copy"** buttons to copy results to clipboard
5. Click **"🗑 Clear"** to reset all data if needed

### Calculation Formula

The program uses the following formula to calculate SpO₂:

```
SpO₂ = (1.587×R₁ - 5.348×R₂ - 4.009×R₃ + 3.426×R₄) / (5.43×R₁ - 140.05×R₂ + 168.532×R₃ - 73.191×R₄)
```

where R = ln(Id/Is) for each wavelength.

## Interface

- **Input Data**: Table for entering Id and Is values
- **Intermediate Calculations**: Display of R-values for each wavelength
- **Results**: SpO₂ shown both as a fraction and percentage

## Notes

- Is values must be smaller than corresponding Id values
- All input values must be positive numbers
- Supports number input with both dot and comma as decimal separator

## Screenshots

The application features a clean, modern interface with:
- Color-coded wavelength indicators
- Readonly intermediate calculation fields
- Easy-to-use copy buttons for results
- Clear visual separation between input, calculations, and results sections
