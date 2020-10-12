# Week 7 Instructions for Code Review Partner:  Quinn Hull
# Code author:  Richard Marcelain, marcelain@email.arizona.edu

**1.** Run python script marcelain_HW7.py using Visual Studio Code

**2.** Enter forecasts for weeks 1 and 2 (retrieved from code output) below:
- Week 1 forecast:  00.0 cfs
- Week 2 forecast:  00.0 cfs

**3.** Enter regression based forecasts for weeks 1 and 2 (retrieved from code output) below:
- Week 1 forecast(AR):  00.0 cfs
- Week 2 forecast(AR):  00.0 cfs

## Code Review:
- Richard, great work! This seems to me to be a simple but efficient way to generate your streamflow prediction for the coming two weeks. I successfully ran the code and understand what you're doing in the script. I believe this is a great job! But, for the sake of thoroughness (and being both affirming and unfortunately nitpicky) see my comments below! I hope you are equally nitpicky with me!

### I like:
  - This script is super well documented and it took me very little time to understand exactly what it was doing.(**3/3 on readability**)
    - The variables and functions are descriptively named
    - the comments are helpful (generally)
    - the doc string did a decent job of describing your function
    - The script can run on its own
  - This follows the pep8 standards really well. I like that you avoided inline comments except for `[30], [31]` (**3/3 on style**)
  - This script is succinct and efficient re the tasks described by this assignment. (**3/3 on code awesome**)
    - There are few superflous codes (see below)
    - The use of functions is appropriate (although there were some issues, see below)
    - Code was decently elegant, but some time could have been saved using for loops etc...
  - Other comments:
    - a simple regression using only the the 1 week lagged data for your regression. (Ultimately, I did the same)
    - sampling a different time interval than Laura did in the original script

### I wish I had seen:
  - A bit more daring with your code! With the exception of rows `[53] - [55]` and `[88] - [108]` this code is pretty much unmodified from the starter code that Laura gave us.
  - Some justification for the choices and changes you made to Laura's script (why did you decide to run a single parameter regression, for example? Why slice the flow_weekly regression to rows (900:1500), or 2006-04-02 through 2017-09-24? Were these arbitrary choices, or did it involved investigation of the data in another way?
  - Some graphical representation of your model, and its fit w real data
  - DRY: use some `for` loops to simplify repetitive tasks
  - Remove some of the spurious / unnecessary variables in Laura's original script. i.e.
    - `[47] data['dayofweek']` is a duplicate of `[47] data['day']` and was unused
    - `[70] test`, as you didn't attempt to test the fit of your model on any other data sets and it was unused
    - `[65] flow_weekly['flow_tm2']` is never used because you decided to just use the 1 week lagged data
  - The function `[15] def predictions(lastweek_flow):`:
    - A bit more documentation on your function specifying the object types of the inputs and the outputs. I think it will pass any scaler value, not just `the previous week's flow (from streamflow7.txt)`. (There was also an extra `'` in your docstring)
    - There should be two parameters to your function. `lastweek_flow` is necessary because it contains the value used to make the prediction. However, this function also needs to pass an sklearn linear regression model object as a parameter. So your def statement should look like this `[15] def predictions(lastweek_flow, model):`. Right now, the function only works if you have made a linear regression variable of the exact name 'model' outside of the formula elsewhere in the script (which you did). But what if I wanted to run the formula using a new model that I made, for example `model2`. There's no way to use that model with this function unless I edit the function so that all instances of `model` are renamed `model2`. If we have 3, 4, 5, or 20 different AR models in one script (like I did), then it becomes a really hairy task, and totally undermines the very usefulness of your function.
  - Avoid creating a whole new 'data' folder in your Submissions:
    - You did this `[31] filepath = os.path.join('../data', filename)`
    - You should do this `[31] filepath = os.path.join('../../data', filename)`
  - Because of how you sampled the data in `[53] october2020_flow`, you actually took the final two weeks of data `flow_weekly` (2020-10-04 and 2020-10-11). As such, your `lastweek_flow` variable isn't actually last week's flow, but two weeks ago flow.
    - you did this `[54] lastweek_flow = october2020_flow.values[0]`
    - you need this `[54] lastweek_flow = october2020_flow.values[1]`
  - Careful with your predictions. I totally understand why you decided not to use the AR (I didn't either). But:
    - `[92] oct2019` is a data frame of weekly flows from September 2019. Did you mean to call this `sept2019`?
    - `[93] flow_forecast` takes not the last two flows from September 2019, but actually the first two. The syntax of your statement is nearly perfect but:
      - you did this `[93] flow_forecast = oct2019['flow_tm2'].tail(2).round(1)`
      - you should do this `[93] flow_forecast = oct2019['flow'].tail(2).round(1)`
    - But then again maybe taking the first two weeks of data from September 2019 is what you wanted to use for your prediction?


