import os
import sys
import argparse
import pandas as pd
import xmltodict


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")

    args = parser.parse_args()

    with open(args.input_filename) as fd:
        doc = xmltodict.parse(fd.read())

    query_filename = (
        doc["msms_pipeline_analysis"]["msms_run_summary"]["@base_name"].split("\\")[-1]
        + "."
        + doc["msms_pipeline_analysis"]["msms_run_summary"]["@raw_data_type"]
    )

    output_list = []

    # Lets get the relevant information out of this
    for spectrum_query in doc["msms_pipeline_analysis"]["msms_run_summary"]["spectrum_query"]:
        print(spectrum_query)

        output_dict = {}

        output_dict["query_filename"] = query_filename

        output_dict["start_scan"] = spectrum_query["@start_scan"]
        output_dict["end_scan"] = spectrum_query["@end_scan"]
        output_dict["retention_time"] = spectrum_query["@retention_time_sec"]
        output_dict["assumed_charge"] = spectrum_query["@assumed_charge"]

        # Getting the peptide ID
        search_result = spectrum_query["search_result"]
        search_hit = search_result["search_hit"]

        output_dict["peptide"] = search_hit["@peptide"]
        output_dict["massdiff"] = search_hit["@massdiff"]

        # Trying to get the score
        try:
            search_scores = search_hit["search_score"]
            for search_score in search_scores:
                if search_score["@name"] == "hyperscore":
                    output_dict["hyperscore"] = search_score["@value"]
        except:
            pass

        try:
            # Getting the ptm result
            ptm_result = search_hit["ptm_result"]

            if type(ptm_result) == list:
                ptm_result = ptm_result[0]

                # output_dict["localization"] = ptm_result["@localization"]
                output_dict["localization_peptide"] = ptm_result["@localization_peptide"]
                output_dict["ptm_mass"] = ptm_result["@ptm_mass"]
            else:
                # output_dict["localization"] = ptm_result["@localization"]
                output_dict["localization_peptide"] = ptm_result["@localization_peptide"]
                output_dict["ptm_mass"] = ptm_result["@ptm_mass"]
        except:
            pass

        output_list.append(output_dict)

    # creating a df
    output_df = pd.DataFrame(output_list)

    # writing to csv
    output_df.to_csv(args.output_filename, sep="\t", index=False)


if __name__ == "__main__":
    main()
