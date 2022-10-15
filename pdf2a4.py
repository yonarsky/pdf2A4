from multiprocessing import Pool
import os
import subprocess
import time

file_list = []
output_dir = "output"
pdf_directory = "pdf"
start_time = time.time()
os.makedirs(output_dir, exist_ok=True)

for root, dirs, files in os.walk(pdf_directory):
    for file in files:
        if file.endswith(".pdf"):
            file_path = os.path.join(root, file)
            file_list.append(file_path)


def convert_pdf(file_path, output_dir):
    file_name = os.path.basename(file_path)
    file_name = file_name.split(".")[0]

    # Ghostscript command
    results = subprocess.run(
        ["gs", "-dNOPAUSE", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-sPAPERSIZE=a4", "-dPDFFitPage",
         "-dFIXEDMEDIA", f"-sOutputFile={output_dir}/{file_name}.pdf",
         f"{file_path}", "-dBATCH"], stdout=subprocess.PIPE)


def process_pdf(args):
    file_path, i = args
    convert_pdf(file_path, output_dir)


if __name__ == "__main__":
    num_processes = 30
    pool = Pool(processes=num_processes)
    pool.map(process_pdf, zip(file_list, range(len(file_list))))
    pool.close()
    print(f"Last file completed in {time.time() - start_time} seconds")