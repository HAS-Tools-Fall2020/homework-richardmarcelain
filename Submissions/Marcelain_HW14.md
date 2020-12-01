# Marcelain 11/30 Assignment 14

___
### Grade

3/3 - nice work.

___

#### Assignment Questions

**1. What is the paper or project you picked? Include a title, a link the the paper and a 1-2 sentence summary of what its about.**
- Title:  Human-induced changes to the global ocean water masses and their time of emergence
- Link:  https://www.nature.com/articles/s41558-020-0878-x  (DOI: https://doi.org/10.1038/s41558-020-0878-x)
- Summary:  The authors of this paper used observation data and 11 climate models (CMIP5) to show the extent to which each ocean basin will release anthropogenically modified (increased temperature and salinity) water mass.

**2. What codes and/or data are associated with this paper? Provide any link to the codes and datasets and a 1-2 sentence summary of what was included with the paper (i.e. was it a github repo? A python package?A database? Where was it stored and how?)**
- Codes included:  Included python and jupyter notebook codes to recreate all the figures included in the research paper:  vertical salinity profiles, timeseries of salinity trends, and box and whisker plots.
- Codes link:  https://github.com/ysilvy/ocean_toe_2020
- Data link:  https://esgf-node.llnl.gov/search/cmip5/
- Summary:  Codes were easy to access via their gitHUB repo.  The files well titled and the code was well documented and easy to follow.  The repo even included codes for the figures in the supplementary information.

**3. Summarize your experience trying to understand the repo: Was their readme helpful? How was their organization? What about documentation within the code itself?**  
- The overall experience was good.  The readme file had basic info like paper link and a sentence describing it, and was extremely unhelpful.  The repo simply stated the database where one could retrieve the data, but did not state which specific files one needed.  However, the code were easy to access and so well organized and documented that it more than made up for the lacking datasets.  I've plotted ocean basin salinity before so I had no issues following the code.

**4. Summarize your experience trying to work with their repo: What happened? Where you successful? Why or why not?**
- The repo was easy to access and sort through.  I appreciated the simplicity of having all the codes in one location, however I have seen better organized repos (seen worse too).  

**5. Summarize your experience working with the data associated with this research. Could you access the data? Where was it? Did it have a DOI? What format was it in?**
- I couldn't access the data, because the author only provided a linke to the CMIP5 database (which is immense).  Without guidance on which specific files I needed to run the code, I could not run the python scripts.  The files were netCDF, and if I spent enough time, I'm sure I could have found the CMIP5 datasets that would have worked.

**6. Did this experience teach you anything about your own repo or projects? Things you might start or stop doing?**
- Yes, in regards to the python codes, I see areas where I can improve.  I went through about 20 repos before this one, and it was one of easier to know what I'm looking at up front.  However, I would have files organized by purpose and figures, rather than lumped into one long list.  Also, I would have a readme file that includes more than the link to the paper.  I like that I could easily open the jupyter notebook and python files, but I wonder why they included both for seemingly random purposes (diff code authors?).
