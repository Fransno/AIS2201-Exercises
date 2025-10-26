import nbformat
from nbconvert import PDFExporter
from traitlets.config import Config
import os


# File data specific to the assignment
assignment_name = "Exercise_9"

files = ["1_Downsampling.ipynb",
         "2_Upsampling.ipynb",
         "3_Resampling.ipynb",
         "4_exercise_review.ipynb"]

title = "Assignment 9: Sample Rate Conversion"

intro_text = r"""
In a number of situations, it is desirable to convert a digital signal $x_{\text{old}}[n]$ acquired at sampling frequency $f_{s, \text{ old}}$ to a new sampling frequency $f_{s, \text{ new}}$, producing a new signal $x_{\text{new}}[m]$. The reasons for doing this might be comparing streams of data with different sample rates, or reducing the sample rate of a signal which was initially [oversampled](https://en.wikipedia.org/wiki/Oversampling). Given that both $x_{\text{old}}[n]$ and $x_{\text{new}}[m]$ are a discrete-time representation of the same analog signal $x(t)$, the ideal result is for the signal $x_{\text{new}}[m]$ to be an exact discrete-time representation of $x(t)$ (assuming the nyquist criterion is met with the new sampling frequency $f_{s, \text{ new}}$):
$$x_{\text{new}}[m] = x(t) \bigg|_{t = \frac{m}{f_{s, \text{ new}}}}$$

![](figures/sample_rate_conversion.png)

This assignment focuses on sample rate conversion, as discussed in chapter 10 in the book "Understanding Digital Signal Processing". The main learning goal of this exercise is to understand how removing samples or inerpolating a signal with samples affects the frequency-domain characteristics of a signal, and how filters can be used to obtain the frequency-domain characteristics we want.
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
