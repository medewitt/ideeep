# Default recipe: build the website
default: build

# Build the website
build:
    cargo run --release

# Kill any process using the specified port
kill-port port="8000":
    @lsof -ti:{{port}} | xargs kill -9 2>/dev/null || true

# Serve the website on a local port (default: 8000)
# This will block until interrupted (Ctrl+C)
serve port="8000":
    #!/usr/bin/env bash
    set -e
    PORT="{{port}}"
    # Kill any existing process on the port
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    echo "Serving website on http://localhost:$PORT"
    cd dist
    # Set up trap to ensure cleanup on Ctrl+C
    trap 'echo ""; echo "Shutting down server..."; lsof -ti:$PORT | xargs kill -9 2>/dev/null || true; exit 0' INT TERM
    python3 -m http.server $PORT

# Build and serve in one command
preview port="8000":
    #!/usr/bin/env bash
    set -e
    PORT="{{port}}"
    echo "Building website..."
    cargo run
    # Kill any existing process on the port
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    echo "Serving website on http://localhost:$PORT"
    cd dist
    # Set up trap to ensure cleanup on Ctrl+C
    trap 'echo ""; echo "Shutting down server..."; lsof -ti:$PORT | xargs kill -9 2>/dev/null || true; exit 0' INT TERM
    python3 -m http.server $PORT

logo:
    @echo "Building logo as PDF..."
    pdflatex -interaction=nonstopmode -output-directory=assets wake_biology_logo.tex
    @echo "Building logo as SVG..."
    latex -interaction=nonstopmode -output-directory=assets wake_biology_logo.tex >/dev/null 2>&1
    @if [ -f assets/wake_biology_logo.dvi ]; then \
        dvisvgm --no-fonts --output=assets/wake_biology_logo.svg assets/wake_biology_logo.dvi 2>/dev/null && \
        echo "SVG created successfully" || \
        (echo "Warning: SVG conversion failed. Trying alternative methods..." && \
         if command -v pdf2svg >/dev/null 2>&1; then \
             pdf2svg assets/wake_biology_logo.pdf assets/wake_biology_logo.svg && echo "SVG created via pdf2svg"; \
         elif command -v inkscape >/dev/null 2>&1; then \
             inkscape assets/wake_biology_logo.pdf --export-type=svg --export-filename=assets/wake_biology_logo.svg 2>/dev/null && echo "SVG created via inkscape"; \
         else \
             echo "Warning: Could not convert to SVG. PDF available at assets/wake_biology_logo.pdf"; \
         fi); \
    else \
        echo "Warning: DVI file not created. PDF available at assets/wake_biology_logo.pdf"; \
    fi
    @rm -f assets/wake_biology_logo.aux assets/wake_biology_logo.log assets/wake_biology_logo.dvi assets/wake_biology_logo.out
    @if [ -f assets/wake_biology_logo.svg ]; then \
        echo "Logo built: assets/wake_biology_logo.pdf and assets/wake_biology_logo.svg"; \
    else \
        echo "Logo built: assets/wake_biology_logo.pdf (SVG conversion skipped)"; \
    fi

ideep-logo:
    @echo "Building IDEEP logo as PDF..."
    pdflatex -interaction=nonstopmode -output-directory=assets ideep_logo.tex
    @echo "Building IDEEP logo as SVG..."
    latex -interaction=nonstopmode -output-directory=assets ideep_logo.tex >/dev/null 2>&1
    @if [ -f assets/ideep_logo.dvi ]; then \
        dvisvgm --no-fonts --output=assets/ideep_logo.svg assets/ideep_logo.dvi 2>/dev/null && \
        echo "SVG created successfully" || \
        (echo "Warning: SVG conversion failed. Trying alternative methods..." && \
         if command -v pdf2svg >/dev/null 2>&1; then \
             pdf2svg assets/ideep_logo.pdf assets/ideep_logo.svg && echo "SVG created via pdf2svg"; \
         elif command -v inkscape >/dev/null 2>&1; then \
             inkscape assets/ideep_logo.pdf --export-type=svg --export-filename=assets/ideep_logo.svg 2>/dev/null && echo "SVG created via inkscape"; \
         else \
             echo "Warning: Could not convert to SVG. PDF available at assets/ideep_logo.pdf"; \
         fi); \
    else \
        echo "Warning: DVI file not created. PDF available at assets/ideep_logo.pdf"; \
    fi
    @rm -f assets/ideep_logo.aux assets/ideep_logo.log assets/ideep_logo.dvi assets/ideep_logo.out
    @if [ -f assets/ideep_logo.svg ]; then \
        echo "IDEEP logo built: assets/ideep_logo.pdf and assets/ideep_logo.svg"; \
    else \
        echo "IDEEP logo built: assets/ideep_logo.pdf (SVG conversion skipped)"; \
    fi

