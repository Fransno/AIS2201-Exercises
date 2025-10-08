import nbformat
from nbconvert import PDFExporter
from traitlets.config import Config
import os


# File data specific to the assignment
assignment_name = "Exercise_7"



files = ["1_image_filtering.ipynb", 
         "2_moving_average.ipynb", 
         "3_radar.ipynb", 
         "4_autocorrelation.ipynb",
         "5_exercise_review.ipynb"]
files = ["4_autocorrelation.ipynb"]

title = "Assignment 7: FIR filters, convolution and correlation"

intro_text = r"""
FIR filters are one of the two main categories of digital filters. The abbreviation **FIR** stands for **F**inite **I**mpulse **R**esponse, which means that if the filter is applied to a delta pulse as the input signal ($x[n] = \delta[n]$), the output signal (the impulse response) ($y[n] = h[n]$) will always return to zero after a given number of samples $N$.

The relationship between the input signal $x[n]$ and the output signal $y[n]$ for an FIR filter is given by the general difference equation for FIR filters:

\begin{align*}
y[n] &= \sum_{k=0}^{N} b_k \cdot x[n-k] \\
&= b_0 \cdot x[n]+b_1 \cdot x[n-1] + b_2 \cdot x[n-2] + \ldots + b_N \cdot x[n-N]
\end{align*}

where $N$ is the filter's order, and the sequence of numbers $b_k$ are the filter's *filter coefficients*. 

The relationship between the input signal $x[n]$ and the output signal $y[n]$ can be described as the result of a *convolution operation* between $x[n]$ and the filter's impulse response $h[n]$. 

\begin{align*}
y[n] &= \sum_{n=0}^{N} h[k]\cdot x[n-k] \\
&= h[n]*x[n]
\end{align*}
"""
intro_text = "Introduction"

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
