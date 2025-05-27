import gzip
import csv
from utils import print_file_names_and_sizes

def reduce_csv(input_gz_file,
               output_csv_file,
               fraction=0.1):
    # First pass: count lines
    with gzip.open(input_gz_file, mode='rt', newline='') as f:
        total_lines = sum(1 for _ in f) - 1  # subtract 1 for header

    lines_to_keep = max(1, int(total_lines * fraction))

    # Second pass: write the desired lines
    with gzip.open(input_gz_file, mode='rt', newline='') as f_in, \
         open(output_csv_file, mode='w', newline='') as f_out:

        reader = csv.reader(f_in)
        writer = csv.writer(f_out)

        # Write header
        header = next(reader)
        writer.writerow(header)

        # Write first N rows
        for i, row in enumerate(reader):
            if i >= lines_to_keep:
                break
            writer.writerow(row)

if __name__ == "__main__":

    def main():
        # Hero datasets, original sizes
        # train 1.18M, clients 7.64M, purchases 670M
        # final sizes after uncompressing and reducing by .001
        # train 30K, clients 220K, purchases 45M,
        in_files = ["clients.csv.gz",
                    "uplift_train.csv.gz"]
        out_files = ["small_clients.csv",
                    "small_uplift_train.csv"]
        print_file_names_and_sizes(in_files)
        for i in range(2):
            reduce_csv(in_files[i],
                        out_files[i],
                       fraction=0.01)
        print_file_names_and_sizes(out_files)

    main()