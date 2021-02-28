"""Classes for IO operations"""

import csv
import logging
import os

import numpy as np
import pandas as pd

logger = logging.getLogger('pyautoai')


class IoHandler:
    """Default class for IO operations. Used for testing.
    """
    # pylint: disable=W0613

    @classmethod
    def read_data(cls, data_src):
        """Read preprocessed data

        :param data_src: Where to find data
        """

        logger.debug('Not reading data. No IO specified.')
        return {}


    @classmethod
    def save_data(cls, data, data_src):
        """Save preprocessed data

        :param data: A dict of Pandas DataFrame/Series
        :param output_src: Where to save data
        """

        logger.debug('Not saving data. No IO specified.')


    @classmethod
    def save_results(cls, results, output_src):
        """Save predictions

        :param results: A list of dicts of results
        :param output_src: Directory to save results (str)
        """

        logger.debug('Not saving predictions. No IO specified.')


    @classmethod
    def save_predictions(cls, predictions, score, model_name, output_src):
        """Save results to CSV file

        :param predictions: Model predictions
        :param model_name: Model name (str)
        :param output_src: Output directory (str)
        """

        logger.debug('Not saving predictions. No IO specified.')


class CsvWriter(IoHandler):
    """A class for saving data to CSV files"""

    @classmethod
    def read_data(cls, data_src):
        """Read data files containing preprocessed data

        :param data_src: Directory path to find data files
        :return: A dict of DataFrames & Series, (pd.DataFrame/pd.Series)
        """

        files = [f for f in os.listdir(data_src) if f.endswith('csv')]
        data = {}
        for data_file in files:
            path = os.path.join(data_src, data_file)
            model_name = data_file.split('.')[0]

            try:
                data[model_name] = pd.read_csv(path, delimiter=',')
            except IOError:
                data[model_name] = np.genfromtxt(path, delimiter=',')
        return data


    @classmethod
    def save_data(cls, data, data_src):
        """Save data to disk to pre-load preprocessed data next time.

        :param data: A dict of Pandas DataFrame/Series
        :param output_src: Directory to save data
        """

        info = {}
        for key, dataset in data.items():
            path = os.path.join(data_src, f'{key}.csv')
            try:
                dataset.to_csv(path, sep=',', index=False)
                info[key] = 'pandas'
            except IOError:
                np.savetxt(path, dataset, delimiter=',')
                info[key] = 'numpy'

        with open(os.path.join(data_src, 'info.txt'), 'w') as info_file:
            for key, val in info.items():
                info_file.write(f'{key} -> {val}\n')


    @classmethod
    def save_results(cls, results, output_src):
        """Save results to CSV file

        :param results: A list of dicts of results
        :param output_src: Directory to save results (str)
        """

        assert isinstance(results, list)
        assert len(results) > 0

        # Create directories
        os.makedirs(output_src, exist_ok=True)

        # Sort headers alphabetically. Model name always goes first
        headers = sorted(list(results[0].keys()), key=lambda v: v.upper())
        if 'model' in headers:
            headers.insert(0, headers.pop(headers.index('model')))

        # Check if the file has been created
        file_path = os.path.join(output_src, f'{results[0]["model"]}.csv')
        is_new_file = not os.path.exists(file_path)

        with open(file_path, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)

            # Write file headers
            if is_new_file:
                writer.writeheader()

            # Write data to file line by line
            for data in results:
                data = {k: str(v) for k, v in data.items()}
                writer.writerow(data)


    @classmethod
    def save_predictions(cls, predictions, score, model_name, output_src):
        """Save model predictions

        :param predictions: Model predictions
        :param model_name: Model name (str)
        :param output_src: Output directory (str)
        """

		# Create directories
        folder = os.path.join(output_src, 'predictions', model_name)
        os.makedirs(folder, exist_ok=True)

        # Save predictions
        path = os.path.join(folder, f'{score}.csv')
        np.savetxt(path, predictions, delimiter=',', fmt='%s')


    @classmethod
    def generate_summaries(cls, results_src, placeholder):
        """Generate summary files from results files

        :param results_src: Results directory (str)
        :param placeholder: Placeholder for NaNs, infs, etc.
        """

        if not os.path.exists(results_src):
            raise FileNotFoundError(\
                f'Cannot find results dir ({results_src}). Please run engine first')

        files = [ # Get all results files (but not predictions or other summaries)
            f for f in os.listdir(results_src)
            if (f.endswith('csv')
            and not f.startswith('predictions')
            and not f.startswith('results'))
            ]

        stats = []
        results = []
        unused_values = [
            'FAIL', 'inf', '-inf', float('inf'), float('-inf'),
            np.inf, -np.inf, np.nan, '#NAME?'
            ]

        for file_name in files: # for each model
            model_name = file_name.split('.')[0]
            file_path = os.path.join(results_src, file_name)
            df = pd.read_csv(file_path, delimiter=',')

            # 1. Record failed training attempts
            scores = df['test_MAE'].value_counts()
            fails = scores[scores.isin(unused_values)]
            stats.append(f"Fails for {model_name} -> {str(fails.values)}")

            # 2. Remove unused values and set column types
            df = df.replace(unused_values, placeholder)

            # 3. Get rows of best models
            results = cls.summarise_model(df, model_name, results)

        cls.write_summary_files(results_src, stats, results)


    @classmethod
    def summarise_model(cls, df, model_name, results):
        """Summarise a model's performance

        :param df: Results data (pd.DataFrame)
        :param model_name: Name of model (str)
        :param results: A list of dicts
        :return: Updated results
        """

        for col in ['val_MAE', 'test_MAE', 'val_MAPE', 'test_MAPE']:
            df[col] = df[col].astype('float64')

        for window in df['num_outputs'].unique():
            df_window = df[df['num_outputs'] == window]

            for feature_selection in df_window['feature_selection'].unique():
                df_fs = df_window[df_window['feature_selection'] == feature_selection]

                for multioutput_method in df_fs['multioutput'].unique():
                    df_mm = df_fs[df_fs['multioutput'] == multioutput_method]

                    for resampling_method in df_mm['resampling'].unique():
                        df_rm = df_mm[df_mm['resampling'] == resampling_method]

                        for scaling in df_rm['scaling'].unique():
                            df_sc = df_rm[df_rm['scaling'] == scaling]

                            best_scores = cls.best_scores_by_seed(df_sc)

                            results.append({
                                'model': model_name,
                                'num_outputs': window,
                                'feature_selection': feature_selection,
                                'multioutput_method': multioutput_method,
                                'resampling_method': resampling_method,
                                'scaling': scaling,
                                'MAPE': best_scores['test_MAPE'].median(),
                                'MAE': best_scores['test_MAE'].median(),
                            })
        return results


    @classmethod
    def best_scores_by_seed(cls, df):
        """Get the results of the models with the best validation scores
         for each seed

        :param df: DataFrame of model results
        :return: Best model results
        """

        # Get indices of best models for each seed
        indices = []
        for seed in df['seed'].unique():
            df_seed = df[df['seed'] == seed]
            if df_seed.shape[0] > 0:
                indices.append(df_seed['val_MAPE'].idxmin())
        best_scores = df.loc[indices]

        return best_scores


    @classmethod
    def write_summary_files(cls, results_src, stats, results):
        """Write model summaries to files

        :param results_src: Results directory (str)
        :param stats: A list of strings
        :param results: A list of dicts or results
        """

        results_path = os.path.join(results_src, 'results-summary.csv')
        if os.path.exists(results_path):
            os.remove(results_path)

        with open(results_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=results[0].keys())
            writer.writeheader()

            # Write data to file line by line
            for data in results:
                data = {k: str(v) for k, v in data.items()}
                writer.writerow(data)

        # Record statistics in text file
        if len(stats) > 0:
            with open(os.path.join(results_src, 'stats.txt'), 'w') as info_file:
                for line in stats:
                    info_file.write(line + '\n')
