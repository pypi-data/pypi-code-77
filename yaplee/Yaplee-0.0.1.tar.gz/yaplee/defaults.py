HELLOWORLD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8">
  <title>Hello, World!</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Lato:100,300'>

</head>
<body>
<div id="main">
    	<div class="fof">
        		<h1>Hello, World!</h1>
        		<h4>
        			This is a default page from Yaplee<br>
        			This page is located in the project "pages" folder<br>
        			<a href="#">Click here to view the full Yaplee documents</a>

        		</h4>
    	</div>
</div>
</body>
</html>
'''

HELLOWORLD_CSS = '''
*{
    transition: all 0.6s;
}

html {
    height: 100%;
}

body{
    font-family: 'Lato', sans-serif;
    color: #888;
    margin: 0;
}

#main{
    display: table;
    width: 100%;
    height: 100vh;
    text-align: center;
}

.fof{
	  display: table-cell;
	  vertical-align: middle;
}

.fof h1{
	  font-size: 50px;
	  display: inline-block;
	  padding-right: 12px;
	  animation: type .5s alternate infinite;
}

@keyframes type{
	  from{box-shadow: inset -3px 0px 0px #888;}
	  to{box-shadow: inset -3px 0px 0px transparent;}
}'''