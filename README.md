# Personal RCT

Run [randomised control trials](https://en.wikipedia.org/wiki/Randomized_controlled_trial) on yourself using data from your personal activity tracker
(currently supports Fitbit). Optionally make your findings publicly
available, for example:

* [The effect of magnesium supplementation on sleep quality: evidence from my fitbit](https://peterjrichens.github.io/personal-rct/magnesium_sleep_may_2021.html)
* [The effect of magnesium supplementation on sleep quality: phase II](https://peterjrichens.github.io/personal-rct/magnesium_sleep_july_2021.html)

## Set up environment
You will need to set up your development environment using conda, which you can install [directly](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) or via [pyenv](https://github.com/pyenv/pyenv). Then, ensure you have [GNU Make](https://www.gnu.org/software/make/) installed before running the following command:

```bash
make setup_env
```

## Get your Fitbit data

Follow [instructions](https://help.fitbit.com/articles/en_US/Help_article/1133.htm) to export a complete archive of your Fitbit account data. You will later need to ensure the data path in config.yaml points to the location of your data.

## Create a new report

1. Generate a new config file:

	```bash
	make new_config
	```
2. Edit `config.yaml` as required

3. Run the analysis using the template notebook:

	```bash
	make execute_nb
	```

4. Inspect the results in `temp_output.ipynb`

5. To publish a report:
	
	```bash
	make publish name=magnesium_sleep_may_2021
	```
	
	This will generate html files under `docs/*.html`. Check-in the generated files to make them publicly accessible via github pages.
