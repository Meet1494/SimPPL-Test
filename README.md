So the dataset provided was very unstructured and in '.jsonl', so I flattened out the json to convert it into more readable and workable csv.
Pre-processed the dataset and found out 5 major parameters on which analytics could be done :
1) Time based Posts
2) Community-wise engagament on the posts(likes,comments,shares)
3) Most used keywords in title
4) Most used keywords in body text
5) Most used keywords overall (including comments, searches, title and body text)

Then created a flask server 'app.py' which renders all these plots in real-time and sends it across to the frontend.
Used plotly to create dynamic and interactive charts.
Then used HTML+CSS+JS(Due to time limitations) to create a dashboard.
Dasboard takes all the graphs in real-time and sends it across to the user.

Here is the video link for the same : https://drive.google.com/file/d/1Pmaa-LuP8he-0_XyGK8deiGqmJ7oZjcl/view?usp=drive_link

For Using it :
Download the cleaned dataset
Run app.py
Run the HTML file(it has css and js emebedded)
