# Image Enhancement Toolkit

A streamlit-based web application that provides various image processing functionalities using OpenCV and PIL.

## Features

- **Image Upload**: Support for JPG, JPEG, and PNG formats
- **Processing Operations**:
  - Grayscale conversion
  - Gaussian blur with adjustable kernel size
  - Edge detection with customizable thresholds
  - Binary thresholding with adjustable values
  - Brightness and contrast adjustment
  - Watershed segmentation for object separation
  - Adaptive threshold segmentation with adjustable parameters
  
- **Download**: Processed images can be downloaded in PNG format

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TheAhmedHazem/Image-Enhancement-Toolkit.git
   cd Image-Enhancement-Toolkit
   ```

2. Install dependencies:
   ```bash
   pip install -r reqs.txt
   ```

## Dependencies

- Python ≥ 3.12
- streamlit ≥ 1.44.1
- numpy ≥ 2.2.5
- matplotlib ≥ 3.10.1
- opencv-python ≥ 4.11.0
- pillow ≥ 11.2.1

## Usage

1. Start the Streamlit server:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and go to the displayed URL (typically http://localhost:8501)

3. Upload an image using the file uploader in the sidebar

4. Select a processing operation and adjust parameters as needed

5. Download the processed image using the download button

## Project Structure

```
Image-Enhancement-Toolkit/
├── app.py          # Main Streamlit application with UI components
├── utils.py        # Utility functions for image processing operations
├── reqs.txt        # Project dependencies
├── static/         # Static assets for web interface
│   └── style.css   # CSS styles for HTML interface
├── templates/      # HTML templates for potential web interface
│   └── index.html  # Main HTML template
├── LICENSE         # MIT License
└── README.md       # Project documentation
```

## Code Organization

The project follows a modular structure:

- **app.py**: Contains the Streamlit UI and application logic
- **utils.py**: Contains reusable image processing functions:
  - Basic operations (grayscale, blur, edge detection)
  - Advanced segmentation techniques (watershed, adaptive thresholding)
  - Helper functions for image conversion and download

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

