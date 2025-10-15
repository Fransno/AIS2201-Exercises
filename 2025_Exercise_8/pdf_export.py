import nbformat
from nbconvert import PDFExporter
from traitlets.config import Config
import os


# File data specific to the assignment
assignment_name = "Exercise_8"

files = ["1_FIR_analysis.ipynb", 
         "2_Lowpass_design.ipynb", 
         "3_More_filter_types.ipynb",
         "4_Audio_equalizer.ipynb",
         "5_Speech_filtering.ipynb",
         "6_Exercise_review.ipynb"]

title = "Assignment 8: Analysis and design of FIR filters"

intro_text = r"""
In exercise 7 we learned about convolution and correlation, and how the shape of a filter's impulse response $h[n]$ deterimines what type of signals are allowed to pass through the filter. In this exercies we will focus on the frequency response $H(\hat{\omega})$ of FIR filters, which is calculated by taking the discrete-time fourier transform (DTFT) of the impulse respones $h[n]$. 

The frequency response $H(\hat{\omega})$ of a filter gives insight into how a sinusoidal input $x[n]$ is affected by the filter. The most common way to visualize the frequency response of a filter is with a pair of plots: a magnitude response plot $|H(\hat{\omega})|$ and a phase response plot $\angle H(\hat{\omega})$. The code cell below will load a demo showing the magnitude/phase response of a customizable filter `hn` as well as a time plot showing input/output waveforms for an adjustable frequency.

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
