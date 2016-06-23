#!/usr/bin/env python
import MySQLdb

################please enter your password in the place of password#######
# open databases connection
db = MySQLdb.connect("localhost","root","gorkha","pollutiondata" )
print "content-type: text/html"
print 
con = '''
<html>
<head>
   <title> Pollution in the U.S. </title>
</head>
<body>


  <script src="http://d3js.org/d3.v3.min.js"></script>
  <script src="http://d3js.org/topojson.v1.min.js"></script>
  <script src="http://datamaps.github.io/scripts/0.5.4/datamaps.all.min.js"></script>
  <!-- this link to the source code -->
  <!--<p><a href="http://datamaps.github.io/">DataMaps Project Homepage</a></p> -->
  <!-- changing the width in the div below will change the size of the map --> 
  <div id="container" style="position: relative; width: 500px; height: 300px;"></div>
 
     
     <script>
	/*
       //basic map config with custom fills, mercator projection
      var map = new Datamap({
        element: document.getElementById('container'),
	scope:'usa'
	});
	*/

	var map  = new Datamap({
  scope: 'usa',
  element: document.getElementById('container'),
  geographyConfig: {
    highlightBorderColor: '#bada55',
  popupTemplate: function(geography, data) {
      return '<div class="hoverinfo">' + 
'Total:' +  data.Total + '</br>' +  'Coal:' + data.Coal + '</br>' +  'Petroleum:' + data.Pet + '</br>' +  'Gas:' + data.Gas +' '
    },
    highlightBorderWidth: 3
  },

  fills: {
  'Good': '#99FF33',
  'Moderate': '#FFFF00',
  'Unhealthy for Sensitive Groups': '#FF9900',
  'Unhealthy': '#FF0000',
  'Very Unhealthy': '#990099',
  'Hazardous': '#660033',
  defaultFill: '#EDDC4E'
},
data:{
'''
print con
cursor=db.cursor()

cursor.execute("SELECT * FROM `1990`")

def filler(value):
	if value > 300:
		return "Hazardous"
	elif value > 200:
		return "Very Unhealthy"
	elif value > 150:
		return "Unhealthy"
	elif value > 100:
		return "Unhealthy for Sensitive Groups"
	elif value > 50:
		return "Moderate"
	else:
		return "Good"

for row in cursor.fetchall():
	#print(row[0])
	state = row[0]
	coal = row[1]
	pet = row[2]
	gas = row[3]
	total = row[4]
	color = filler(total)  
	print '''
  	"%s": {
      "fillKey": "%s",
	"Coal": %d,
	"Pet": %d,
	"Gas": %d,
      "Total": %d 
  },

	'''%(state, color, coal, pet, gas, total)

footer = '''
}
});
map.legend();
map.labels();
	</script>
<!--<form name="myform" method="GET" action="cgi-bin/access.py">
<input type= "text" id="name" name ="name" >
<input type = "text" id="product"name ="product" >
<input type = "submit"> -->
	</body>

'''
print footer
#prepare SQl query to UPDATE required records
#cursor=db.cursor()
# execute SQL query using execute() method.
#cursor.execute("SELECT * FROM `1990`,`2000`,`2010`,`2013`")
#cursor.execute("SELECT * FROM `1990`")

# Fetch a single row using fetchone() method.
#data = cursor.fetchall()

#print (data)

# disconnect from server
db.close()   
#steps 
# read the databases and color the map based on the dense population
