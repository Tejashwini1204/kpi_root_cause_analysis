import plotly.express as px

print("Running...")

fig = px.scatter(x=[1,2,3], y=[4,5,6])
#fig.write_image("test.png")
fig.show()

print("Done")