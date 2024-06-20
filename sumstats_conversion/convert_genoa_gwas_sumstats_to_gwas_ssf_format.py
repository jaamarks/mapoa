import typer
from pathlib import Path
import pandas as pd
import numpy as np
import re
from typing_extensions import Annotated

app = typer.Typer()

typer.Argument
@app.command()
def main(
    infile: Annotated[Path, typer.Argument(help = "Input sumstats file path")],
    outfile: Annotated[Path, typer.Argument(help = "Output GWAS-SSF formatted file path")],
    chrom: str = "CHROM",
    variant: str = "ID",
    keep_indels: bool = False
) -> Path:
    """Transform GENOA GWAS sumstats to GWAS-SSF-v1.0 format

    This tool was designed specifically for the sumstats that went into

    the GENOA GWAS meta-analysis. It expects the input file to be

    formatted in a particular way. In particular, the tool expects

    certain column names and variant ID patterns like:

    * rs544698705:672940:G:C

    * 1:768116:A:AGTTTT

    * 1:766600:<CN0>:G

    * 1:3011887:<INS:ME:ALU>:A

    It creates the required and recommended columns for GWAS-SSF v1.0

    and arranges them in the expected order. You should then validate

    the output the GWAS SumStats tools: https://github.com/EBISPOT/gwas-sumstats-tools
    """

    df = pd.read_csv(infile, sep='\t')

    # apply formatting steps
    df = split_expand(df, variant)
    if not keep_indels:
        df = remove_indels(df)
    df = non_rs(df, chrom)
    df = ref_allele(df)
    df = remove_extra(df)
    df = rename_reorder(df, chrom)

    # Save the DataFrame to a TSV file
    df.to_csv(outfile, sep='\t', index=False)

    # pretty print message
    pretty_print(infile, outfile)


# Define the function to split the string using the regular expression
def _split_variant_id(variant):
    # Split on colons not preceded by "<", or after ">" e.g., 1:3011887:<INS:ME:ALU>:A
    #pattern = r'(?<!<):+|(?<=>:)'
    return re.findall(r'[^:<>]+|<[^>]+>', variant)


# Split and expand into new columns
def split_expand(df, variant):
    try:
        df[['rs', 'pos', '1kg_ref', '1kg_alt']] = df[variant].apply(_split_variant_id).apply(pd.Series)
        return df
    except ValueError as e:
        print("Error occurred while splitting the values. The line that caused the error:")
        print(e)
        #print(df[df[variant].str.count(':') != 3])

def remove_indels(df):
    # remove any line which contains indels
    mask = df.apply(lambda x: x.astype(str).str.contains('<|>', regex=True)).any(axis=1)
    filtered_df = df[~mask]
    return filtered_df

# Set non-'rs' entries to '#NA'
def non_rs(df, chrom):
    df['rs'] = df['rs'].apply(lambda x: x if x.startswith('rs') else '#NA')
    df['variant_id'] = df[[chrom, 'pos', '1kg_ref', '1kg_alt']].apply(lambda x: '_'.join(x.astype(str)), axis=1)
    return df

# create ref_allele column
def ref_allele(df):
    # compare ALT (effect_allele) to 1kg_ref
    df['ref_allele'] = np.where(df['1kg_ref'] == df['ALT'], 'EA', 'OA')
    return df

def remove_extra(df):
    # remove unecessary columns for gwas-ssf-v1.0
    columns_to_drop = ['ID', 'MAF', 'INFORMATIVE_ALT_AC', 'CALL_RATE', 'HWE_PVALUE', 'N_REF', 'N_HET', 'N_ALT', 'U_STAT', 'SQRT_V_STAT', '1kg_ref', '1kg_alt', 'pos', 'UNKOWN', 'POP_MAF', 'SOURCE', 'IMP_QUAL']

    # Check if each column exists before dropping it
    columns_to_drop_existing = [col for col in columns_to_drop if col in df.columns]
    df.drop(columns=columns_to_drop_existing, axis=1, inplace=True)
    return df

def rename_reorder(df, chrom):
    # rename columns
    column_map = {chrom: 'chromosome',
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
                    }

    new_order = ['chromosome', 'base_pair_location',
             'effect_allele', 'other_allele',
             'beta', 'standard_error',
             'effect_allele_frequency', 'p_value',
             'rsid', 'variant_id',
             'ref_allele', 'n']

    newdf = df.rename(columns=column_map)
    newdf = newdf[new_order]
    return newdf

def pretty_print(infile, outfile):
    RESET = "\033[0m"
    RED ="\033[31m"
    UNDERLINE = "\033[4m"
    inf = f"{UNDERLINE}{RED}{infile}{RESET}"
    outf = f"{UNDERLINE}{RED}{outfile}{RESET}"
    print(f"\nSuccessfully processed {inf} and wrote to {outf}")

if __name__ == "__main__":
    app()
