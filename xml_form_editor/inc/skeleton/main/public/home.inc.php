<?php
	require_once $_SESSION['config']['_ROOT_'].'/inc/lib/StringFunctions.php';
?>
<div id="featured-wrapper"><div id="featured">
	<h1>Welcome to the Material Data Curator</h1>
	<p>
		This system allows for the curation of Material Data in a repository using predefined templates and a prototype <a href="" target="blank">ontology</a>.
	</p>
	<p>
		This is a prototype being developed at the National Institute of Standards and Technology and is made available to sollicit comments from the Material Science community.
		Please do not enter any proprietary data into this system.
	</p>
</div></div>

<div id="main">
<div class="separator-vertical">
	<div class="col2 left">
		<h2 class="left">Available options</h2>
		<div class="clearer">&nbsp;</div>
		<div class="content-separator"></div>
		
		<!-- TODO Add it in a future version -->
		<!--img src="resources/img/samples/thumbnail.jpg" width="64" height="64" alt="" class="left bordered" />
		<h3><a href="#">Create your account</a></h3>
		<p>In nunc et nibh rutrum volutpat. Sed tempus interdum ligula adipiscing blandit. Aliquam tempor, elit ac rhoncus lacinia, mauris metus suscipit sem.</p>
		
		<div class="clearer">&nbsp;</div>
		<div class="content-separator"></div-->
		
		<img src="resources/img/edit-big.png" alt="" class="left bordered" />
		<h3><a href="register">Curate your Material Data</a></h3>
		<p>Click here to select a form template and then, fill out the corresponding form.</p>
		
		<div class="clearer">&nbsp;</div>
		<div class="content-separator"></div>
		
		<img src="resources/img/search-big.png" width="64" height="64" alt="" class="left bordered" />
		<h3><a href="search">Explore the repository</a></h3>
		<p>Click here to search for Material Data in the repository using flexible queries. <i>Not yet implemented</i>.</p>
		
		<div class="clearer">&nbsp;</div>
		<div class="content-separator"></div>
		
		<img src="resources/img/help-big.png" width="64" height="64" alt="" class="left bordered" />
		<h3><a href="next-features">Want to see more?</a></h3>
		<p>Take a look at the <a href="admin-tour"><b>admin subsystem</b></a> or see what some of our <a href="next-features"><b>future plans</b></a> are.</p>
	
		<div class="clearer">&nbsp;</div>
	</div>
	
	<div class="col2 right">
		<!--h2 class="left">New data sets</h2>
		<div class="pull-right">
			<a href="search" class="btn">Browse Repository<span class="icon-chevron-right"></span></a>
		</div>
		
		<div class="clearer">&nbsp;</div>

		<ul class="nice-list">
			<li><span>2009-06-21 |</span> <a href="#">Data set 0</a></li>
			<li><span>2009-06-21 |</span> <a href="#">Data set 1</a></li>
			<li><span>2009-06-21 |</span> <a href="#">Data set 2</a></li>
			<li><span>2009-06-21 |</span> <a href="#">Data set 3</a></li>
			<li><span>2009-06-21 |</span> <a href="#">Data set 4</a></li>
		</ul-->
		<h2 class="left">Current templates</h2>		
		<div class="clearer">&nbsp;</div>

		<ul class="nice-list">
			<?php
				$schemaFolder = $_SESSION['config']['_XSDFOLDER_'];
				$schemaFolderFiles = scandir($schemaFolder);
				
				$even = true;
				$limit = 5;
				foreach($schemaFolderFiles as $file)
				{					
					if(endsWith($file, '.xsd')) 
					{
						echo '<li>'.$file.'</li>';
					}
					$even = !$even;
					
					if($limit==-1)
						break;
					
					$limit -= 1;
				}
			?>
		</ul>
		<div class="pull-right">
			<a href="register" class="btn">More templates<span class="icon-chevron-right"></span></a>
		</div>					
	</div>

<div class="clearer">&nbsp;</div>
</div>
</div>
