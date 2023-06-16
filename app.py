from flask import Flask, render_template, request, jsonify
import os
import csv
import PyPDF2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


def extract_key_value_pairs(pdf_path):
    header_data = {}
    table_data = []

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        # Extract header data from the first page
        first_page = first_page = reader.pages[0]

        header_text = first_page.extract_text()
        lines = header_text.split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                header_data[key.strip()] = value.strip()

        # Extract tabular data from the remaining pages
        for page_num in range(1, num_pages):
            page = reader.getPage(page_num)
            table = page.extract_tables()[0]  # Assumes the first table on the page
            for row in table:
                table_data.append(row)

    return header_data, table_data


def save_to_csv(data, csv_path):
    header_data, table_data = data

    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Key', 'Value'])

        for key, value in header_data.items():
            writer.writerow([key, value])

        writer.writerow([])  # Add an empty row to separate header and table data

        for row in table_data:
            writer.writerow(row)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file
    file = request.files['pdfFile']
    filename = file.filename

    # Save the uploaded file to the 'uploads' folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Run the data extraction script
    pdf_path = r'"C:\Users\Timi Laja\Downloads\Sample Files.pdf'
    csv_path = r'C:\Users\Timi Laja\Downloads\Sample Files\sample2.csv'
    extracted_data = extract_key_value_pairs(pdf_path)

    # Save extracted data to CSV
    save_to_csv(extracted_data, csv_path)

    # Return the extracted data as JSON response
    return jsonify(extracted_data)


if __name__ == '__main__':
    app.run(debug=True)
