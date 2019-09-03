# BT BEATS
Transforming The Business Times’ articles into an indicator of Business & Economic Activity Trends & Sentiment, or [BEATS](https://btbeats.herokuapp.com/).

### Goal

- Create a new BT business sentiment index based on BT news articles. Each BT article within a timeframe is scored by algorithms for sentiment and the scores are aggregated to indicate economic outlook over that period, forming a new tool for readers and companies to keep their fingers on Singapore’s economic pulse.

- Group articles into topics automatically to surface underlying trends that may not have been obvious, providing new avenues of interest for subscribers and possible follow-ups for journalists.

- Perform subject analysis by allowing users to track the sentiment towards a subject compared to overall sentiment of all articles, and the number of articles written on the subject.

### Why use The Business Times?

- [The Business Times](https://www.businesstimes.com.sg) is Singapore's flagship business media outlet and is already business/economy focused.

- We are riding on the vast experience of editors and journalists to pick the information that has the most impact on Singapore's economy.

- BT is published six days a week, producing a constant stream of real-time, high-frequency data.

## The process:
- For this project, permission was obtained from [Singapore Press Holdings](https://www.sph.com.sg) to use BT articles from Jan 1, 2014 to Aug 15, 2019.

- After data gathering and cleaning, we have:
  - one 208 MB `.txt` file
  - 49,159 articles
  - 31,284,599 words

- Converting duff `VADER` to smart `VADER`:
  - Added the [Loughran-McDonald list](https://sraf.nd.edu/textual-analysis/resources/#LM%20Sentiment%20Word%20Lists) of financial terms

- Discovering trends:
  - Remove capitalisation, punctuation, and stop words. Words were also lemmatised to remove differences between, say, "say" and "said".
  - Use `latent Dirichlet Allocation` for topic modelling.

- Dashboard creation:
  - Use `Plotly` and `Dash` to create a [dashboard](https://btbeats.herokuapp.com/).

  ## Conclusion

  ### Findings

  - The new BT BEATS Index shows good potential as an indicator of GDP growth in Singapore.
  - This is a tool that builds on existing content to offer new service to:
    - Government and business entities
    - Communications professionals
    - Subscribers

  ### Limitations

  - It should be noted that BT BEATS is more of an indicator of the health of the economy and less a classic machine learning model that gives predictions of a target based on input of features.
  - It should thus be used to complement traditional economic indicators to enhance one's sense of the health of the economy.
  - The subject analysis tool is also highly dependent on the number of articles written about the subject in the time period. A higher number of articles means a more reliable sentiment can be gauged about the subject.

  ### Further exploration

  - Expand the timeframe of articles taken into consideration.
  - Ride on existing segmentation of articles to further zoom into articles relevant to the economy. For example, we can consider disregarding restaurant reviews and explore how that affects the BEATS Index.
  - Invest in a proprietary lexicon that suits the unique context of the Singapore economy.

  Further notes:
  - The `.csv` file containing all the BT articles is not included in this repository as copyright lies with SPH. Instead, an abridged file containing the headlines and sentiment scores is uploaded.
