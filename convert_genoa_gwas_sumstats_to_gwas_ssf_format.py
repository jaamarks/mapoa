import argparse
import pandas as pd
import re
import numpy as np

# need to add Type

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process sumstats by creating a variant and rsID column.")
    parser.add_argument("--input-file", "-i", dest="input_file", type=str, help="Path to the input file")
    parser.add_argument("--output-file", "-o", dest="output_file", type=str, help="Path to the output file")
    parser.add_argument("--chrom", dest="chrom", type=str, help="Name of the column containing the chromosome information.")
    parser.add_argument("--variant", dest="variant", type=str, help="Name of the column containing the variant ID (e.g., rs544698705:672940:G:C)  information.")
    parser.add_argument("--sep", dest="sep", type=str, default="\t", help="Delimiter.")

    return parser.parse_args()

def process_data(infile, chrom, variant, outfile, sep="\t"):
    """
    Process sumstats by creating a variant and rsID column.

    Args:
        data (tsv file): The file containing the sumstats data.
        chrom (str): The original name of the chromosome column.
        variant (str): The original name of the variant column.
        outfile (str): The name of the output file to save processed sumstats.
        sep (char): The delimeter (default "\t")

    Returns:
        pd.DataFrame: The processed DataFrame with the chromosome column renamed and repositioned.
    """

    df = pd.read_csv(infile, sep=sep)

    # Define the function to split the string using the regular expression
    def _split_variant_id(variant):
        # Split on colons not preceded by "<", or after ">" e.g., 1:3011887:<INS:ME:ALU>:A
        return re.findall(r'[^:<>]+|<[^>]+>', variant)
    #pattern = r'(?<!<):+|(?<=>:)'

    # Split and expand into new columns
    try:
        df[['rs', 'pos', '1kg_ref', '1kg_alt']] = df[variant].apply(_split_variant_id).apply(pd.Series)
    except ValueError as e:
        print("Error occurred while splitting the values. The line that caused the error:")
        print(e)
        #print(df[df[variant].str.count(':') != 3])

    # Set non-'rs' entries to '#NA'
    df['rs'] = df['rs'].apply(lambda x: x if x.startswith('rs') else '#NA')
    df['variant_id'] = df[[chrom, 'pos', '1kg_ref', '1kg_alt']].apply(lambda x: '_'.join(x.astype(str)), axis=1)

    # compare ALT (effect_allele) to 1kg_ref
    # Use np.where to compare columns and make a decision
    df['ref_allele'] = np.where(df['1kg_ref'] == df['ALT'], 'EA', 'OA')

    # remove unecessary columns for gwas-ssf-v1.0
    columns_to_drop = ['ID', 'MAF' 'INFORMATIVE_ALT_AC', 'CALL_RATE', 'HWE_PVALUE', 'N_REF', 'N_HET', 'N_ALT', 'U_STAT', 'SQRT_V_STAT', '1kg_ref', '1kg_alt', 'pos', 'UNKOWN', 'POP_MAF', 'SOURCE', 'IMP_QUAL']

    # Check if each column exists before dropping it
    columns_to_drop_existing = [col for col in columns_to_drop if col in df.columns]
    df.drop(columns=columns_to_drop_existing, axis=1, inplace=True)

    # rename columns (some of the cohorts have different column names)
    df.rename(columns={chrom: 'chromosome',
                       'P': 'p_value',
                       'PVALUE': 'p_value',
                       'POS': 'base_pair_location',
                       'REF': 'other_allele',
                       'ALT': 'effect_allele',
                       'AF': 'effect_allele_frequency',
                       'ALT_EFFSIZE': 'beta',
                       'SE': 'standard_error',
                       'rs': 'rsid',
                       'N_INFORMATIVE': 'n',
                       'N': 'n',
                    }, inplace=True)

    # reorder
    df = df[['chromosome', 'base_pair_location',
             'effect_allele', 'other_allele',
             'beta', 'standard_error',
             'effect_allele_frequency', 'p_value',
             'rsid', 'variant_id',
             'ref_allele', 'n']]

    # Save the DataFrame to a TSV file
    df.to_csv(outfile, sep='\t', index=False)

def main():
    """Main function to parse arguments and call the processing function."""
    args = parse_arguments()
    data = process_data(
                         infile=args.input_file,
                         chrom=args.chrom,
                         outfile=args.output_file,
                         variant=args.variant,
                         sep=args.sep
                        )
    print(f"\nSuccessfully processed {args.input_file} and wrote to {args.output_file}")

if __name__ == "__main__":
  main()
