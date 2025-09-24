import nbformat
from nbconvert import PDFExporter
from traitlets.config import Config
import os


# File data specific to the assignment
assignment_name = "Exercise_6"



files = ["1_DSP_Library.ipynb", 
         "2_Device_config.ipynb", 
         "3_Buffer_management.ipynb", 
         "4_RFFT_on_STM32.ipynb",
         "5_exercise_review.ipynb"]

title = "Exercise 6: Spectral Analysis in Real-Time on an STM32 MCU"

intro_text = r"""
The goal of this assignment is to program the STM32 microcontroller to run a simple frequency detection algorithm. The algorithm in question will perform frequency detecion in 3 steps:

1. Compute the real-valued fast fourier transform ([`rfft`](https://numpy.org/doc/stable/reference/generated/numpy.fft.rfft.html)) of the sampled input signal.
    * The `rfft` function exploits the symmetric nature of a real-valued signal's DFT, so it does not have to perform quite as many calculations. The output is limited to *only* the positive half of the frequency spectrum, meaning that for $N$ signal samples the `rfft` output has length $\frac{N}{2} + 1$.
2. Identify the highest peak location in the `rfft` output.
3. Convert peak location to wave frequency measured in $\text{Hz}$, and present this value as system output.

"""


def write_to_PDF(student_name: str):
    """
    Function to compile 1 PDF document from a list of '.ipynb' in consecutive order.

    Parameters
    ----------
    assignment_name : str
        Name of output file (file format '.pdf' will be appended)
        Default value for document title
    files : list[str]
        List of Jupyter Notebook files (.ipynb) to compile into output pdf.
    student_name : str
        Sets the author in the output file's title section
    title : str, optional
        The output PDF's title. Defaults to 'assignment_name' if not specified.
    intro_text : str, optional
        Text for initial paragraph preceding content of the first Jupyter Notebook
        file in the 'files' argument.

    Output
    -------
    output file : <assignment_name>.pdf
        Document to be uploaded to learning management system (Blackboard, Canvas, 
        Inspera etc..).
    """

    # c = Config()
    # c.TemplateExporter.extra_template_basedirs = ["./assignment_template"]
    # c.TemplateExporter.template_name = 'latex'
    
    merged = nbformat.v4.new_notebook()
    merged.metadata["title"] = title if title != "" else assignment_name
    merged.metadata["authors"] = [{"name": student_name}]
    merged_cells = []
    if intro_text != "":
        merged_cells.append(nbformat.v4.new_markdown_cell(source=intro_text))

    for file in files:
        with open(file, 'r', encoding='utf-8') as fh:
            nb = nbformat.read(fh, as_version=4)
            #nb.cells.pop(0) # Remove header
            #nb.cells.pop(-1) # Remove footer
            merged_cells.extend(nb.cells)
            
    merged.cells = merged_cells

    exporter = PDFExporter()

    # Export to PDF bytes
    pdf_data, _resources = exporter.from_notebook_node(
        merged,
        resources={"metadata": {"path": os.getcwd()}},
    )

    # Write the PDF
    with open(assignment_name + ".pdf", "wb") as f:
        f.write(pdf_data)

def pdf_convert_debug():
    student_name = "Ola Normann"
    merged = nbformat.v4.new_notebook()
    merged.metadata["title"] = title if title != "" else assignment_name
    merged.metadata["authors"] = [{"name": student_name}]


    for file in files:
        print(f"Processing {file}")
        with open(file, 'r', encoding='utf-8') as fh:
            nb = nbformat.read(fh, as_version=4)
            for cell in nb.cells:
                merged.cells = [cell]
                exporter = PDFExporter()
                try:
                    # Export to PDF bytes
                    pdf_data, _resources = exporter.from_notebook_node(
                        merged,
                        resources={"metadata": {"path": os.getcwd()}},
                    )
                except:
                    raise Exception(f"problem encountered converting '{file}' \n cell contents: \n {cell.source}")
