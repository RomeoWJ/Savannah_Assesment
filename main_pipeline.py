from extract_data import run_extraction
from clean_transform import run_cleaning
from load_bigquery import run_loading

def main():
    run_extraction()
    run_cleaning()
    run_loading()

if __name__ == "__main__":
    main()
