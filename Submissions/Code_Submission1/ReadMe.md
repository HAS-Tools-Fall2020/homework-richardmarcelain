# Week 8 Code Instructions 
# Code author:  Richard Marcelain, marcelain@email.arizona.edu
# Code Review Partner:  Quinn Hull

# Instructions
**1.** Run python script Marcelain_HW8.py using Visual Studio Code

**2.** Enter regression based forecasts below:
- Week 1 forecast(AR):  00.0 cfs
- Week 2 forecast(AR):  00.0 cfs

**3.** Enter final forecasts below:
- Week 1 forecast:  00.0 cfs
- Week 2 forecast:  00.0 cfs

# Written Assignment
**1. Brief Summary:**  The AR model I used was trained on the on the last 5 years of data, which was robust enough to get the general yearly trend in flow.  The simulated results were expected to fail in the lowest flow value months of the year, but that was okay since I plan for it later in the code.

**2. Forecast Generation:**  The forecasts generated using the model are higher than expected for this year.  That's why I used a function which generates predictions adjusted by the low 2020 flow values of this year to produce liklely flow values for weeks 1 and 2.

**3. Peer Evaluation:**  Quinn was immensely helpful in his code review response.  I was able to follow his advice in making my code more efficient, neater, and more unique than the previous version.

**4. Peer Evaluation:**  I'm most proud of adding an adjustment to the AR model in the function portion to account for the low flow values this year compared the the last 20 year average.  The flow predictions look reasonable and I look forward to seeing how well they hold up.
