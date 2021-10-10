import pandas
import os
import glob
dirname = os.path.dirname(__file__)


def open_all_dataframes(evaluation_dir):
    all_files = glob.glob(f"{evaluation_dir}/*.xlsx")
    all_df_dict = {}
    # Loop through all files and retrieve their name + open the spreadsheet as a pandas df
    for result in all_files:
        repo_name = result.split(os.path.sep)[-1].split(".")[0]
        df = pandas.read_excel(result)
        all_df_dict[repo_name] = df

    return all_df_dict


def retrieve_all_summaries(all_dfs):
    summarised_df = []
    for repo_name, df in all_dfs.items():
        # Summary line is third from the bottom
        summary = list(df.values[-3])
        total, losses, wins = summary[1], summary[3], summary[5]

        summarised_df.append([repo_name, total, losses, wins])
    columns = ["Repository Name", "Total Comparisons", "PyType Wins", "Scalpel Wins"]

    total = int(sum([x[1] for x in summarised_df]))
    losses = int(sum([x[2] for x in summarised_df]))
    wins = int(sum([x[3] for x in summarised_df]))
    # We shouldn't be dividing by 0 at any time so no need for error checking
    summarised_df.append(["Overall Accuracy:", f"{round((total - losses)/total, 4) * 100}%",
                          "Accuracy vs PyType:", f"{round(wins/losses, 4) * 100}%"])
    df = pandas.DataFrame(summarised_df, columns=columns)

    return df


def main():
    evaluation_dir = os.path.join(dirname, "evaluation_outputs")

    all_dfs = open_all_dataframes(evaluation_dir)

    summarised_df = retrieve_all_summaries(all_dfs)

    summarised_df.to_excel(os.path.join(dirname, "summarised_results.xlsx"), index=False)


if __name__ == '__main__':
    main()