#!/usr/bin/env nextflow
nextflow.enable.dsl=2

params.input_spectra_folder = ""
params.input_pepxml_file = ""

TOOL_FOLDER = "$baseDir/bin"

process processDataPython {
    publishDir "./nf_output", mode: 'copy'

    conda "$TOOL_FOLDER/conda_env.yml"

    input:
    file input

    output:
    file 'output.tsv'

    """
    python $TOOL_FOLDER/convert_pepxml.py $input output.tsv
    """
}


workflow {
    data = Channel.fromPath(params.input_pepxml_file)
    
    // Outputting Python
    processDataPython(data)
}